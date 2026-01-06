package com.quizz.core.repository;

import com.quizz.core.entity.DuelMatch;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface DuelMatchRepository extends JpaRepository<DuelMatch, Long> {

    // Find a duel match that is searching for opponent (not the current player)
    // Only find recent duels (created in the last 2 minutes) to avoid matching with abandoned searches
    @Query("SELECT d FROM DuelMatch d LEFT JOIN FETCH d.quiz WHERE d.status = 'SEARCHING' " +
           "AND d.player1.id <> :userId " +
           "AND d.createdAt > :cutoffTime " +
           "ORDER BY d.createdAt ASC")
    Optional<DuelMatch> findFirstSearchingMatch(@Param("userId") Long userId, @Param("cutoffTime") LocalDateTime cutoffTime);

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

    // Find old incomplete duels (SEARCHING, MATCHED, COUNTDOWN)
    @Query("SELECT d FROM DuelMatch d WHERE d.status IN ('SEARCHING', 'MATCHED', 'COUNTDOWN') " +
           "AND d.createdAt < :cutoffTime")
    List<DuelMatch> findOldIncompleteDuels(@Param("cutoffTime") LocalDateTime cutoffTime);

    // Find duels for specific user IDs with specific statuses
    @Query("SELECT d FROM DuelMatch d WHERE " +
           "(d.player1.id IN :userIds OR d.player2.id IN :userIds) " +
           "AND d.status IN ('SEARCHING', 'MATCHED', 'COUNTDOWN', 'IN_PROGRESS')")
    List<DuelMatch> findActiveDuelsForUsers(@Param("userIds") List<Long> userIds);
}

