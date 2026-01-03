package com.quizz.core.repository;

import com.quizz.core.entity.Country;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;

import java.util.Optional;

public interface CountryRepository extends JpaRepository<Country, Long>, JpaSpecificationExecutor<Country> {

    // Find country by sigle (e.g., "FRA", "USA")
    Optional<Country> findBySigle(String sigle);

    // Find country by name
    Optional<Country> findByCountryName(String countryName);
}

