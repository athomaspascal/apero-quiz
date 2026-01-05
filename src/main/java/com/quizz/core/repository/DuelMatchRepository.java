package com.quizz.core.repository;

import com.quizz.core.entity.DuelMatch;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface DuelMatchRepository extends JpaRepository<DuelMatch, Long> {

    // Find a duel match that is searching for opponent (not the current player)
    @Query("SELECT d FROM DuelMatch d LEFT JOIN FETCH d.quiz WHERE d.status = 'SEARCHING' AND d.player1.id <> :userId ORDER BY d.createdAt ASC")
    Optional<DuelMatch> findFirstSearchingMatch(Long userId);

    // Find active duel for a user
    @Query("SELECT d FROM DuelMatch d LEFT JOIN FETCH d.quiz WHERE (d.player1.id = :userId OR d.player2.id = :userId) " +
           "AND d.status IN ('SEARCHING', 'MATCHED', 'COUNTDOWN', 'IN_PROGRESS', 'REMATCH_PENDING')")
    Optional<DuelMatch> findActiveDuelForUser(Long userId);

    // Find duel by ID with player
    @Query("SELECT d FROM DuelMatch d LEFT JOIN FETCH d.quiz WHERE d.id = :duelId AND (d.player1.id = :userId OR d.player2.id = :userId)")
    Optional<DuelMatch> findByIdAndUser(Long duelId, Long userId);

    // Override findById to include quiz
    @Query("SELECT d FROM DuelMatch d LEFT JOIN FETCH d.quiz WHERE d.id = :id")
    @NonNull
    Optional<DuelMatch> findById(@NonNull Long id);
}

