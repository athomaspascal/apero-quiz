package com.quizz.core.entity;

import jakarta.persistence.*;
import org.jspecify.annotations.Nullable;

@Entity
@Table(name = "countries")
public class Country {

    public static final int SIGLE_LENGTH = 3;
    public static final int COUNTRY_NAME_MAX_LENGTH = 100;

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    @Column(name = "country_id")
    private Long id;

    @Column(name = "sigle", nullable = false, unique = true, length = SIGLE_LENGTH)
    private String sigle = "";

    @Column(name = "country_name", nullable = false, length = COUNTRY_NAME_MAX_LENGTH)
    private String countryName = "";

    @Lob
    @Basic(fetch = FetchType.EAGER)
    @Column(name = "country_flag", columnDefinition = "TEXT")
    private String countryFlag;

    public Country() {
        // To keep Hibernate happy
    }

    public Country(String sigle, String countryName) {
        setSigle(sigle);
        setCountryName(countryName);
    }

    public Country(String sigle, String countryName, String countryFlag) {
        setSigle(sigle);
        setCountryName(countryName);
        setCountryFlag(countryFlag);
    }

    public @Nullable Long getId() {
        return id;
    }

    public String getSigle() {
        return sigle;
    }

    public void setSigle(String sigle) {
        if (sigle != null && sigle.length() > SIGLE_LENGTH) {
            throw new IllegalArgumentException("Sigle length must be exactly " + SIGLE_LENGTH + " characters");
        }
        this.sigle = sigle != null ? sigle.toUpperCase() : "";
    }

    public String getCountryName() {
        return countryName;
    }

    public void setCountryName(String countryName) {
        if (countryName != null && countryName.length() > COUNTRY_NAME_MAX_LENGTH) {
            throw new IllegalArgumentException("Country name length exceeds " + COUNTRY_NAME_MAX_LENGTH);
        }
        this.countryName = countryName;
    }

    public String getCountryFlag() {
        return countryFlag;
    }

    public void setCountryFlag(String countryFlag) {
        this.countryFlag = countryFlag;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == null || !getClass().isAssignableFrom(obj.getClass())) {
            return false;
        }
        if (obj == this) {
            return true;
        }

        Country other = (Country) obj;

        return id != null && id.equals(other.getId());
    }

    @Override
    public int hashCode() {
        return id != null ? id.hashCode() : super.hashCode();
    }

    @Override
    public String toString() {
        return "Country{" +
                "id=" + id +
                ", sigle='" + sigle + '\'' +
                ", countryName='" + countryName + '\'' +
                '}';
    }
}

