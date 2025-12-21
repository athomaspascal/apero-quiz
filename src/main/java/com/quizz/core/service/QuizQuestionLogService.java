package com.quizz.core.service;

import com.quizz.core.entity.Quiz;
import com.quizz.core.entity.QuizQuestion;
import com.quizz.core.entity.QuizQuestionLog;
import com.quizz.core.entity.User;
import com.quizz.core.repository.QuizQuestionLogRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class QuizQuestionLogService {

    private final QuizQuestionLogRepository logRepository;

    public QuizQuestionLogService(QuizQuestionLogRepository logRepository) {
        this.logRepository = logRepository;
    }

    @Transactional
    public void logQuestion(User user, Quiz quiz, QuizQuestion question,
                           String userAnswer, int timeTakenSeconds, String sessionCode) {

        // Extract options from the question
        List<String> options = question.getOptions();
        String option1 = options.size() > 0 ? options.get(0) : null;
        String option2 = options.size() > 1 ? options.get(1) : null;
        String option3 = options.size() > 2 ? options.get(2) : null;
        String option4 = options.size() > 3 ? options.get(3) : null;

        // Check if answer is correct
        boolean isCorrect = question.getAnswer() != null && question.getAnswer().equals(userAnswer);

        QuizQuestionLog log = new QuizQuestionLog(
            user,
            quiz,
            question.getId(), // Use question ID instead of UUID
            question.getQuestion(),
            option1,
            option2,
            option3,
            option4,
            question.getAnswer(),
            userAnswer,
            isCorrect,
            timeTakenSeconds,
            sessionCode
        );

        logRepository.save(log);
    }

    @Transactional(readOnly = true)
    public List<QuizQuestionLog> getUserLogs(User user) {
        return logRepository.findByUserOrderByAskedAtDesc(user);
    }

    @Transactional(readOnly = true)
    public List<QuizQuestionLog> getSessionLogs(String sessionCode) {
        return logRepository.findBySessionCodeOrderByAskedAt(sessionCode);
    }

    @Transactional(readOnly = true)
    public List<QuizQuestionLog> getQuestionLogs(Long questionIdRef) {
        return logRepository.findByQuestionIdRef(questionIdRef);
    }
}

