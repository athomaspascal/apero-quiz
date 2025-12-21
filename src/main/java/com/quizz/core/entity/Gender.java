package com.quizz.core.entity;

public enum Gender {
    MALE("♂"),
    FEMALE("♀");

    private final String symbol;

    Gender(String symbol) {
        this.symbol = symbol;
    }

    public String getSymbol() {
        return symbol;
    }
}

