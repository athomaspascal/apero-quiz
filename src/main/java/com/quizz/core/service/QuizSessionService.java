package com.quizz.core.service;

import com.quizz.core.entity.Quiz;
import com.quizz.core.entity.QuizParticipant;
import com.quizz.core.entity.QuizSession;
import com.quizz.core.entity.User;
import com.quizz.core.repository.QuizParticipantRepository;
import com.quizz.core.repository.QuizSessionRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class QuizSessionService {

    private final QuizSessionRepository sessionRepository;
    private final QuizParticipantRepository participantRepository;

    public QuizSessionService(QuizSessionRepository sessionRepository,
                              QuizParticipantRepository participantRepository) {
        this.sessionRepository = sessionRepository;
        this.participantRepository = participantRepository;
    }

    @Transactional
    public QuizSession createSession(Quiz quiz, Long hostUserId) {
        QuizSession session = new QuizSession(quiz, hostUserId);
        return sessionRepository.saveAndFlush(session);
    }

    @Transactional(readOnly = true)
    public QuizSession getSessionByCode(String sessionCode) {
        return sessionRepository.findBySessionCode(sessionCode).orElse(null);
    }

    @Transactional
    public QuizParticipant joinSession(QuizSession session, User user) {
        // Check if user already joined
        var existing = participantRepository.findBySessionAndUser(session, user);
        if (existing.isPresent()) {
            return existing.get();
        }

        QuizParticipant participant = new QuizParticipant(session, user);
        return participantRepository.saveAndFlush(participant);
    }

    @Transactional(readOnly = true)
    public List<QuizParticipant> getParticipants(QuizSession session) {
        return participantRepository.findBySession(session);
    }

    @Transactional
    public void updateParticipantScore(QuizParticipant participant, int score) {
        participant.setScore(score);
        participant.setCompleted(true);
        participantRepository.saveAndFlush(participant);
    }

    @Transactional
    public void updateSessionStatus(QuizSession session, QuizSession.SessionStatus status) {
        session.setStatus(status);
        sessionRepository.saveAndFlush(session);
    }

    @Transactional
    public void updateSession(QuizSession session) {
        sessionRepository.saveAndFlush(session);
    }

    @Transactional
    public void resetParticipants(QuizSession session) {
        List<QuizParticipant> participants = participantRepository.findBySession(session);
        for (QuizParticipant participant : participants) {
            participant.setScore(0);
            participant.setCompleted(false);
        }
        participantRepository.saveAllAndFlush(participants);
    }

    @Transactional
    public void updateParticipantTeam(QuizParticipant participant, String teamName) {
        participant.setTeamName(teamName);
        participantRepository.saveAndFlush(participant);
    }

    @Transactional(readOnly = true)
    public QuizParticipant getParticipant(QuizSession session, User user) {
        return participantRepository.findBySessionAndUser(session, user).orElse(null);
    }
}
