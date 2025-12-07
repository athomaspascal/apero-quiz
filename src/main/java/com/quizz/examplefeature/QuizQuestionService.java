package com.quizz.examplefeature;

import org.jspecify.annotations.Nullable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class QuizQuestionService {

    private final QuizQuestionRepository quizQuestionRepository;

    public QuizQuestionService(QuizQuestionRepository quizQuestionRepository) {
        this.quizQuestionRepository = quizQuestionRepository;
    }

    @Transactional(readOnly = true)
    public List<QuizQuestion> getQuestionsByQuizId(Long quizId) {
        return quizQuestionRepository.findByQuizId(quizId);
    }

    @Transactional(readOnly = true)
    public @Nullable QuizQuestion getQuestionByQuizIdAndIndex(Long quizId, int index) {
        List<QuizQuestion> questions = getQuestionsByQuizId(quizId);
        if (index >= 0 && index < questions.size()) {
            return questions.get(index);
        }
        return null;
    }

    @Transactional(readOnly = true)
    public int getTotalQuestionsByQuizId(Long quizId) {
        return (int) quizQuestionRepository.countByQuizId(quizId);
    }

    @Transactional
    public void createQuestion(Quiz quiz, String question, List<String> options, String answer) {
        QuizQuestion quizQuestion = new QuizQuestion(quiz, question, options, answer);
        quizQuestionRepository.save(quizQuestion);
    }
}

