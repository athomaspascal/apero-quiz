package com.quizz.core.service;

import com.quizz.core.repository.QuizRepository;
import com.quizz.core.entity.Quiz;
import org.jspecify.annotations.Nullable;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class QuizService {

    private final QuizRepository quizRepository;

    QuizService(QuizRepository quizRepository) {
        this.quizRepository = quizRepository;
    }

    @Transactional
    public Quiz createQuiz(String name) {
        var quiz = new Quiz(name);
        return quizRepository.saveAndFlush(quiz);
    }

    @Transactional(readOnly = true)
    public List<Quiz> list(Pageable pageable) {
        return quizRepository.findAllBy(pageable).toList();
    }

    @Transactional(readOnly = true)
    public @Nullable Quiz getById(Long id) {
        return quizRepository.findById(id).orElse(null);
    }

}

