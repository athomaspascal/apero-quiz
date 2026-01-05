package com.quizz.core.service;

import com.quizz.core.entity.DuelMatch;
import com.quizz.core.entity.Quiz;
import com.quizz.core.entity.User;
import com.quizz.core.repository.DuelMatchRepository;
import com.quizz.core.repository.QuizRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.Random;

@Service
public class DuelService {

    private static final Logger logger = LoggerFactory.getLogger(DuelService.class);
    private final DuelMatchRepository duelMatchRepository;
    private final QuizRepository quizRepository;
    private final Random random = new Random();

    public DuelService(DuelMatchRepository duelMatchRepository, QuizRepository quizRepository) {
        this.duelMatchRepository = duelMatchRepository;
        this.quizRepository = quizRepository;
    }

    /**
     * Start searching for a duel opponent
     */
    @Transactional
    public DuelMatch startSearching(User user) {
        logger.info("User {} starting duel search", user.getName());

        // Check if user already has an active duel
        Optional<DuelMatch> existingDuel = duelMatchRepository.findActiveDuelForUser(user.getId());
        if (existingDuel.isPresent()) {
            logger.info("User {} already has an active duel", user.getName());
            return existingDuel.get();
        }

        // Try to find an existing searching match
        Optional<DuelMatch> searchingMatch = duelMatchRepository.findFirstSearchingMatch(user.getId());

        if (searchingMatch.isPresent()) {
            // Match found! Join this duel
            DuelMatch duel = searchingMatch.get();
            duel.setPlayer2(user);
            duel.setStatus(DuelMatch.DuelStatus.MATCHED);

            // Select a random quiz
            Quiz randomQuiz = selectRandomQuiz();
            duel.setQuiz(randomQuiz);

            logger.info("Match found! Player1: {}, Player2: {}, Quiz: {}",
                duel.getPlayer1().getName(), duel.getPlayer2().getName(), randomQuiz.getName());

            return duelMatchRepository.save(duel);
        } else {
            // No match found, create a new searching duel
            DuelMatch newDuel = new DuelMatch(user);
            logger.info("No opponent found, creating new searching duel for {}", user.getName());
            return duelMatchRepository.save(newDuel);
        }
    }

    /**
     * Accept the duel match
     */
    @Transactional
    public DuelMatch acceptMatch(Long duelId, User user) {
        logger.info("User {} accepting duel {}", user.getName(), duelId);

        DuelMatch duel = duelMatchRepository.findById(duelId)
            .orElseThrow(() -> new RuntimeException("Duel not found"));

        logger.info("Duel {} - Quiz before accept: {}", duelId,
            duel.getQuiz() != null ? duel.getQuiz().getName() : "null");

        if (duel.getPlayer1().getId().equals(user.getId())) {
            duel.setPlayer1Ready(true);
        } else if (duel.getPlayer2() != null && duel.getPlayer2().getId().equals(user.getId())) {
            duel.setPlayer2Ready(true);
        }

        // If both players are ready, start countdown
        if (duel.isBothPlayersReady()) {
            duel.setStatus(DuelMatch.DuelStatus.COUNTDOWN);
            duel.setCountdownStartedAt(LocalDateTime.now());
            logger.info("Both players ready, starting countdown for duel {} with quiz: {}",
                duelId, duel.getQuiz() != null ? duel.getQuiz().getName() : "null");
        }

        return duelMatchRepository.save(duel);
    }

    /**
     * Start the quiz after countdown
     */
    @Transactional
    public DuelMatch startQuiz(Long duelId) {
        logger.info("Starting quiz for duel {}", duelId);

        DuelMatch duel = duelMatchRepository.findById(duelId)
            .orElseThrow(() -> new RuntimeException("Duel not found"));

        logger.info("Quiz to start: {}", duel.getQuiz() != null ? duel.getQuiz().getName() : "null");

        duel.setStatus(DuelMatch.DuelStatus.IN_PROGRESS);
        duel.setStartedAt(LocalDateTime.now());

        DuelMatch saved = duelMatchRepository.save(duel);
        logger.info("Duel {} status updated to IN_PROGRESS with quiz: {}",
            saved.getId(), saved.getQuiz() != null ? saved.getQuiz().getName() : "null");

        return saved;
    }

    /**
     * Submit score for a player
     */
    @Transactional
    public DuelMatch submitScore(Long duelId, User user, int score) {
        logger.info("User {} submitting score {} for duel {}", user.getName(), score, duelId);

        DuelMatch duel = duelMatchRepository.findById(duelId)
            .orElseThrow(() -> new RuntimeException("Duel not found"));

        if (duel.getPlayer1().getId().equals(user.getId())) {
            duel.setPlayer1Score(score);
        } else if (duel.getPlayer2() != null && duel.getPlayer2().getId().equals(user.getId())) {
            duel.setPlayer2Score(score);
        }

        // If both players finished, move to rematch pending or finished
        if (duel.getPlayer1Score() != null && duel.getPlayer2Score() != null) {
            duel.setFinishedAt(LocalDateTime.now());
            if (duel.canRematch()) {
                duel.setStatus(DuelMatch.DuelStatus.REMATCH_PENDING);
                logger.info("Both players finished duel {}, waiting for rematch decision", duelId);
            } else {
                duel.setStatus(DuelMatch.DuelStatus.FINISHED);
                logger.info("Duel {} finished, no more rematches available", duelId);
            }
        }

        return duelMatchRepository.save(duel);
    }

    /**
     * Request a rematch
     */
    @Transactional
    public DuelMatch requestRematch(Long duelId, User user) {
        logger.info("User {} requesting rematch for duel {}", user.getName(), duelId);

        DuelMatch duel = duelMatchRepository.findById(duelId)
            .orElseThrow(() -> new RuntimeException("Duel not found"));

        if (!duel.canRematch()) {
            logger.warn("Duel {} has reached maximum rematch count", duelId);
            throw new RuntimeException("Maximum rematch count reached");
        }

        if (duel.getPlayer1().getId().equals(user.getId())) {
            duel.setPlayer1Rematch(true);
        } else if (duel.getPlayer2() != null && duel.getPlayer2().getId().equals(user.getId())) {
            duel.setPlayer2Rematch(true);
        }

        // If both players want rematch, reset the duel
        if (duel.isBothPlayersWantRematch()) {
            Quiz newQuiz = selectRandomQuiz();
            duel.setQuiz(newQuiz);
            duel.resetForRematch();
            logger.info("Both players want rematch, starting new round for duel {}", duelId);
        }

        return duelMatchRepository.save(duel);
    }

    /**
     * Cancel the duel
     */
    @Transactional
    public void cancelDuel(Long duelId) {
        logger.info("Cancelling duel {}", duelId);

        DuelMatch duel = duelMatchRepository.findById(duelId)
            .orElseThrow(() -> new RuntimeException("Duel not found"));

        duel.setStatus(DuelMatch.DuelStatus.CANCELLED);
        duel.setFinishedAt(LocalDateTime.now());
        duelMatchRepository.save(duel);
    }

    /**
     * Get active duel for user
     */
    public Optional<DuelMatch> getActiveDuel(User user) {
        return duelMatchRepository.findActiveDuelForUser(user.getId());
    }

    /**
     * Get duel by ID
     */
    public Optional<DuelMatch> getDuelById(Long duelId) {
        return duelMatchRepository.findById(duelId);
    }

    /**
     * Select a random quiz from the database
     */
    private Quiz selectRandomQuiz() {
        List<Quiz> allQuizzes = quizRepository.findAll();
        if (allQuizzes.isEmpty()) {
            throw new RuntimeException("No quizzes available");
        }
        return allQuizzes.get(random.nextInt(allQuizzes.size()));
    }
}

