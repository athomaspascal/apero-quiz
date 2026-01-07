package com.quizz.core.service;

import com.quizz.core.entity.DuelMatch;
import com.quizz.core.entity.Quiz;
import com.quizz.core.entity.User;
import com.quizz.core.repository.DuelMatchRepository;
import com.quizz.core.repository.QuizRepository;
import jakarta.annotation.PostConstruct;
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
    private final UserActivityService userActivityService;
    private final Random random = new Random();

    public DuelService(DuelMatchRepository duelMatchRepository, QuizRepository quizRepository,
                      UserActivityService userActivityService) {
        this.duelMatchRepository = duelMatchRepository;
        this.quizRepository = quizRepository;
        this.userActivityService = userActivityService;
    }

    /**
     * Clean up all pending duels and waiting users at application startup
     */
    @PostConstruct
    @Transactional
    public void initializeCleanup() {
        logger.info("=== DuelService: Starting cleanup at application startup ===");

        // Cancel all duels that are not finished or cancelled
        List<DuelMatch> pendingDuels = duelMatchRepository.findAll().stream()
            .filter(duel -> duel.getStatus() != DuelMatch.DuelStatus.FINISHED &&
                           duel.getStatus() != DuelMatch.DuelStatus.CANCELLED)
            .toList();

        if (!pendingDuels.isEmpty()) {
            logger.info("Cancelling {} pending duels at startup", pendingDuels.size());
            for (DuelMatch duel : pendingDuels) {
                logger.info("Cancelling duel {} - Status: {}, Player1: {}, Player2: {}",
                    duel.getId(),
                    duel.getStatus(),
                    duel.getPlayer1() != null ? duel.getPlayer1().getName() : "null",
                    duel.getPlayer2() != null ? duel.getPlayer2().getName() : "null");
                duel.setStatus(DuelMatch.DuelStatus.CANCELLED);
                duel.setFinishedAt(LocalDateTime.now());
            }
            duelMatchRepository.saveAll(pendingDuels);
        } else {
            logger.info("No pending duels to cancel at startup");
        }

        logger.info("=== DuelService: Cleanup completed ===");
    }

    /**
     * Start searching for a duel opponent
     */
    @Transactional
    public DuelMatch startSearching(User user) {
        logger.info("User {} starting duel search", user.getName());

        // First, clean up any old inactive duels for this user
        cleanupInactiveDuels(user);

        // Check if user already has an active duel
        Optional<DuelMatch> existingDuel = duelMatchRepository.findActiveDuelForUser(user.getId());
        if (existingDuel.isPresent()) {
            logger.info("User {} already has an active duel", user.getName());
            return existingDuel.get();
        }

        // Clean up all old searching/matched duels (older than 2 minutes)
        cleanupOldSearchingDuels();

        // Try to find an existing searching match (only recent ones - last 2 minutes)
        LocalDateTime cutoffTime = LocalDateTime.now().minusMinutes(2);
        Optional<DuelMatch> searchingMatch = duelMatchRepository.findFirstSearchingMatch(user.getId(), cutoffTime);

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
     * Clean up inactive duels for a specific user
     */
    private void cleanupInactiveDuels(User user) {
        logger.info("Cleaning up inactive duels for user {}", user.getName());
        Optional<DuelMatch> existingDuel = duelMatchRepository.findActiveDuelForUser(user.getId());
        if (existingDuel.isPresent()) {
            DuelMatch duel = existingDuel.get();
            // Cancel any duel that is in SEARCHING, MATCHED, or COUNTDOWN for more than 5 minutes
            if (duel.getCreatedAt().isBefore(LocalDateTime.now().minusMinutes(5)) &&
                (duel.getStatus() == DuelMatch.DuelStatus.SEARCHING ||
                 duel.getStatus() == DuelMatch.DuelStatus.MATCHED ||
                 duel.getStatus() == DuelMatch.DuelStatus.COUNTDOWN)) {
                logger.info("Cancelling old inactive duel {} for user {}", duel.getId(), user.getName());
                duel.setStatus(DuelMatch.DuelStatus.CANCELLED);
                duel.setFinishedAt(LocalDateTime.now());
                duelMatchRepository.save(duel);
            }
        }
    }

    /**
     * Clean up all old searching/matched duels system-wide
     */
    private void cleanupOldSearchingDuels() {
        LocalDateTime cutoffTime = LocalDateTime.now().minusMinutes(5);
        List<DuelMatch> oldDuels = duelMatchRepository.findOldIncompleteDuels(cutoffTime);
        if (!oldDuels.isEmpty()) {
            logger.info("Cleaning up {} old incomplete duels", oldDuels.size());
            for (DuelMatch duel : oldDuels) {
                duel.setStatus(DuelMatch.DuelStatus.CANCELLED);
                duel.setFinishedAt(LocalDateTime.now());
            }
            duelMatchRepository.saveAll(oldDuels);
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
    public void cancelDuel(Long duelId, User cancelledByUser) {
        logger.info("Cancelling duel {} by user {}", duelId,
            cancelledByUser != null ? cancelledByUser.getName() : "system");

        DuelMatch duel = duelMatchRepository.findById(duelId)
            .orElseThrow(() -> new RuntimeException("Duel not found"));

        duel.setStatus(DuelMatch.DuelStatus.CANCELLED);
        duel.setFinishedAt(LocalDateTime.now());
        duel.setCancelledBy(cancelledByUser);
        duelMatchRepository.save(duel);

        logger.info("Duel {} cancelled successfully. Status changed to CANCELLED", duelId);
    }

    /**
     * Cancel the duel (without user - for system cleanup)
     */
    @Transactional
    public void cancelDuel(Long duelId) {
        cancelDuel(duelId, null);
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

    /**
     * Cancel duels for inactive users (no activity for more than specified seconds)
     */
    @Transactional
    public int cancelDuelsForInactiveUsers(int inactiveSeconds) {
        // Get all inactive user IDs
        List<Long> inactiveUserIds = userActivityService.getInactiveUserIds(inactiveSeconds);

        if (inactiveUserIds.isEmpty()) {
            return 0;
        }

        logger.info("Found {} inactive users, checking for active duels", inactiveUserIds.size());

        // Find all active duels for these users
        List<DuelMatch> activeDuels = duelMatchRepository.findActiveDuelsForUsers(inactiveUserIds);

        int cancelledCount = 0;
        for (DuelMatch duel : activeDuels) {
            // Check if any player in the duel is inactive
            boolean player1Inactive = duel.getPlayer1() != null &&
                                     inactiveUserIds.contains(duel.getPlayer1().getId());
            boolean player2Inactive = duel.getPlayer2() != null &&
                                     inactiveUserIds.contains(duel.getPlayer2().getId());

            if (player1Inactive || player2Inactive) {
                String inactivePlayers = "";
                if (player1Inactive && player2Inactive) {
                    inactivePlayers = "both players";
                } else if (player1Inactive) {
                    inactivePlayers = duel.getPlayer1().getName();
                } else {
                    inactivePlayers = duel.getPlayer2().getName();
                }

                logger.info("Cancelling duel {} due to inactivity of: {}", duel.getId(), inactivePlayers);
                duel.setStatus(DuelMatch.DuelStatus.CANCELLED);
                duel.setFinishedAt(LocalDateTime.now());
                duelMatchRepository.save(duel);
                cancelledCount++;
            }
        }

        if (cancelledCount > 0) {
            logger.info("Cancelled {} duels due to user inactivity", cancelledCount);
        }

        return cancelledCount;
    }
}

