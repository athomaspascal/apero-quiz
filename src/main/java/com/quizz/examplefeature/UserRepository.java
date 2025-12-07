package com.quizz.examplefeature;

import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Slice;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;

import java.util.Optional;

interface UserRepository extends JpaRepository<User, Long>, JpaSpecificationExecutor<User> {

    // If you don't need a total row count, Slice is better than Page as it only performs a select query.
    // Page performs both a select and a count query.
    Slice<User> findAllBy(Pageable pageable);

    // Find user by email (useful for authentication)
    Optional<User> findByEmail(String email);
}

