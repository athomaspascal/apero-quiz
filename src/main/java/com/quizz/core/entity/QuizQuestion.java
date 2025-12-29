package com.quizz.core.entity;

import jakarta.persistence.*;
import org.jspecify.annotations.Nullable;

import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "quiz_question")
public class QuizQuestion {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    @Column(name = "question_id")
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "quiz_id", nullable = false)
    private Quiz quiz;

    @Column(name = "question", nullable = false, length = 500)
    private String question;

    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "quiz_question_options", joinColumns = @JoinColumn(name = "question_id"))
    @Column(name = "option_text", length = 200)
    @OrderColumn(name = "option_order")
    private List<String> options;

    @Column(name = "answer", nullable = false, length = 200)
    private String answer;

    @Column(name = "difficulty_level")
    private Integer difficultyLevel;

    @Column(name = "date_update")
    private LocalDateTime dateUpdate;

    protected QuizQuestion() {
    }

    public QuizQuestion(Quiz quiz, String question, List<String> options, String answer) {
        this.quiz = quiz;
        this.question = question;
        this.options = options;
        this.answer = answer;
        this.difficultyLevel = null; // Default value
        this.dateUpdate = LocalDateTime.now();
    }

    public QuizQuestion(Quiz quiz, String question, List<String> options, String answer, Integer difficultyLevel) {
        this.quiz = quiz;
        this.question = question;
        this.options = options;
        this.answer = answer;
        this.difficultyLevel = difficultyLevel;
        this.dateUpdate = LocalDateTime.now();
    }

    public @Nullable Long getId() {
        return id;
    }

    public Quiz getQuiz() {
        return quiz;
    }

    public void setQuiz(Quiz quiz) {
        this.quiz = quiz;
    }

    public String getQuestion() {
        return question;
    }

    public void setQuestion(String question) {
        this.question = question;
        this.dateUpdate = LocalDateTime.now();
    }

    public List<String> getOptions() {
        return options;
    }

    public void setOptions(List<String> options) {
        this.options = options;
        this.dateUpdate = LocalDateTime.now();
    }

    public String getAnswer() {
        return answer;
    }

    public void setAnswer(String answer) {
        this.answer = answer;
        this.dateUpdate = LocalDateTime.now();
    }

    public Integer getDifficultyLevel() {
        return difficultyLevel;
    }

    public void setDifficultyLevel(Integer difficultyLevel) {
        this.difficultyLevel = difficultyLevel;
        this.dateUpdate = LocalDateTime.now();
    }

    public LocalDateTime getDateUpdate() {
        return dateUpdate;
    }

    public void setDateUpdate(LocalDateTime dateUpdate) {
        this.dateUpdate = dateUpdate;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == null || !getClass().isAssignableFrom(obj.getClass())) {
            return false;
        }
        if (obj == this) {
            return true;
        }

        QuizQuestion other = (QuizQuestion) obj;
        return getId() != null && getId().equals(other.getId());
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }
}

