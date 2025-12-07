package com.quizz.core.service;

import com.quizz.core.entity.QuizAnswer;
import com.quizz.core.entity.QuizParticipant;
import com.quizz.core.entity.QuizQuestion;
import com.quizz.core.repository.QuizAnswerRepository;
import org.jspecify.annotations.Nullable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

/**
 * Service for managing quiz answers
 */
@Service
public class QuizAnswerService {

    private final QuizAnswerRepository quizAnswerRepository;

    public QuizAnswerService(QuizAnswerRepository quizAnswerRepository) {
        this.quizAnswerRepository = quizAnswerRepository;
    }

    /**
     * Record a participant's answer to a question
     */
    @Transactional
    public QuizAnswer recordAnswer(QuizParticipant participant, QuizQuestion question, String userAnswer) {
        // Check if answer already exists (prevent duplicate answers)
        Optional<QuizAnswer> existingAnswer = quizAnswerRepository.findByParticipantAndQuestion(participant, question);

        if (existingAnswer.isPresent()) {
            // Update existing answer
            QuizAnswer answer = existingAnswer.get();
            answer.setUserAnswer(userAnswer);
            return quizAnswerRepository.save(answer);
        } else {
            // Create new answer
            QuizAnswer answer = new QuizAnswer(participant, question, userAnswer);
            return quizAnswerRepository.save(answer);
        }
    }

    /**
     * Record a participant's answer with time taken
     */
    @Transactional
    public QuizAnswer recordAnswer(QuizParticipant participant, QuizQuestion question, String userAnswer, int timeTakenSeconds) {
        Optional<QuizAnswer> existingAnswer = quizAnswerRepository.findByParticipantAndQuestion(participant, question);

        if (existingAnswer.isPresent()) {
            QuizAnswer answer = existingAnswer.get();
            answer.setUserAnswer(userAnswer);
            answer.setTimeTakenSeconds(timeTakenSeconds);
            return quizAnswerRepository.save(answer);
        } else {
            QuizAnswer answer = new QuizAnswer(participant, question, userAnswer, timeTakenSeconds);
            return quizAnswerRepository.save(answer);
        }
    }

    /**
     * Get all answers for a participant
     */
    @Transactional(readOnly = true)
    public List<QuizAnswer> getParticipantAnswers(QuizParticipant participant) {
        return quizAnswerRepository.findByParticipant(participant);
    }

    /**
     * Get all answers for a specific question
     */
    @Transactional(readOnly = true)
    public List<QuizAnswer> getQuestionAnswers(QuizQuestion question) {
        return quizAnswerRepository.findByQuestion(question);
    }

    /**
     * Get a specific answer
     */
    @Transactional(readOnly = true)
    public @Nullable QuizAnswer getAnswer(QuizParticipant participant, QuizQuestion question) {
        return quizAnswerRepository.findByParticipantAndQuestion(participant, question).orElse(null);
    }

    /**
     * Count correct answers for a participant
     */
    @Transactional(readOnly = true)
    public long countCorrectAnswers(QuizParticipant participant) {
        return quizAnswerRepository.countCorrectAnswersByParticipant(participant);
    }

    /**
     * Count total answers for a participant
     */
    @Transactional(readOnly = true)
    public long countTotalAnswers(QuizParticipant participant) {
        return quizAnswerRepository.countByParticipant(participant);
    }

    /**
     * Calculate score percentage for a participant
     */
    @Transactional(readOnly = true)
    public double calculateScorePercentage(QuizParticipant participant) {
        long total = countTotalAnswers(participant);
        if (total == 0) {
            return 0.0;
        }
        long correct = countCorrectAnswers(participant);
        return (correct * 100.0) / total;
    }

    /**
     * Get all correct answers for a participant
     */
    @Transactional(readOnly = true)
    public List<QuizAnswer> getCorrectAnswers(QuizParticipant participant) {
        return quizAnswerRepository.findByParticipantAndCorrect(participant, true);
    }

    /**
     * Get all incorrect answers for a participant
     */
    @Transactional(readOnly = true)
    public List<QuizAnswer> getIncorrectAnswers(QuizParticipant participant) {
        return quizAnswerRepository.findByParticipantAndCorrect(participant, false);
    }

    /**
     * Get average time taken per question for a participant
     */
    @Transactional(readOnly = true)
    public @Nullable Double getAverageTimeTaken(QuizParticipant participant) {
        return quizAnswerRepository.getAverageTimeTakenByParticipant(participant);
    }

    /**
     * Delete all answers for a participant (useful for retry)
     */
    @Transactional
    public void deleteParticipantAnswers(QuizParticipant participant) {
        List<QuizAnswer> answers = quizAnswerRepository.findByParticipant(participant);
        quizAnswerRepository.deleteAll(answers);
    }

    /**
     * Get detailed statistics for a participant
     */
    @Transactional(readOnly = true)
    public com.quizz.core.dto.ParticipantAnswerStats getParticipantStats(QuizParticipant participant) {
        long total = countTotalAnswers(participant);
        long correct = countCorrectAnswers(participant);
        double percentage = calculateScorePercentage(participant);
        Double avgTime = getAverageTimeTaken(participant);

        com.quizz.core.dto.ParticipantAnswerStats stats = new com.quizz.core.dto.ParticipantAnswerStats(
            participant.getId(),
            participant.getUser().getName(),
            total,
            correct,
            percentage,
            avgTime
        );

        // Add detailed answers
        List<QuizAnswer> answers = getParticipantAnswers(participant);
        List<com.quizz.core.dto.ParticipantAnswerStats.QuestionAnswerDetail> details = answers.stream()
            .map(answer -> new com.quizz.core.dto.ParticipantAnswerStats.QuestionAnswerDetail(
                answer.getQuestion().getId(),
                answer.getQuestion().getQuestion(),
                answer.getUserAnswer(),
                answer.getQuestion().getAnswer(),
                answer.isCorrect(),
                answer.getTimeTakenSeconds()
            ))
            .toList();

        stats.setAnswerDetails(details);

        return stats;
    }
}

