package com.quizz.core.service;

import com.vaadin.flow.component.UI;
import com.vaadin.flow.server.VaadinSession;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.text.MessageFormat;
import java.util.Locale;
import java.util.ResourceBundle;

@Service
public class TranslationService {

    private static final Logger logger = LoggerFactory.getLogger(TranslationService.class);
    private static final String BUNDLE_NAME = "messages";
    private static final String SESSION_LOCALE_KEY = "user.locale";

    public String translate(String key, Locale locale) {
        try {
            ResourceBundle bundle = ResourceBundle.getBundle(BUNDLE_NAME, locale);
            String result = bundle.getString(key);
            logger.debug("Translated '{}' to '{}' for locale {}", key, result, locale);
            return result;
        } catch (Exception e) {
            logger.warn("Translation key '{}' not found for locale {}, falling back to English", key, locale);
            // Fallback to English if key not found
            try {
                ResourceBundle bundle = ResourceBundle.getBundle(BUNDLE_NAME, Locale.ENGLISH);
                return bundle.getString(key);
            } catch (Exception ex) {
                logger.error("Translation key '{}' not found even in English fallback", key);
                return key;
            }
        }
    }

    public String translate(String key) {
        Locale locale = getCurrentLocale();
        return translate(key, locale);
    }

    public String translate(String key, Object... params) {
        Locale locale = getCurrentLocale();
        return translate(key, locale, params);
    }

    public String translate(String key, Locale locale, Object... params) {
        String pattern = translate(key, locale);
        if (params == null || params.length == 0) {
            return pattern;
        }
        try {
            MessageFormat formatter = new MessageFormat(pattern, locale);
            return formatter.format(params);
        } catch (Exception e) {
            logger.error("Error formatting message '{}' with params: {}", pattern, params, e);
            return pattern;
        }
    }

    public void setLocale(Locale locale) {
        logger.info("Setting locale to: {} (language: {}, country: {})",
            locale, locale.getLanguage(), locale.getCountry());
        // Save locale in session
        VaadinSession.getCurrent().setAttribute(SESSION_LOCALE_KEY, locale);
        UI.getCurrent().setLocale(locale);
        logger.info("Locale set in UI and session. Reloading page...");
        UI.getCurrent().getPage().reload();
    }

    public Locale getCurrentLocale() {
        // Try to get locale from session first
        Locale sessionLocale = VaadinSession.getCurrent().getAttribute(Locale.class);
        if (sessionLocale == null) {
            sessionLocale = (Locale) VaadinSession.getCurrent().getAttribute(SESSION_LOCALE_KEY);
        }

        if (sessionLocale != null) {
            logger.debug("Retrieved locale from session: {}", sessionLocale);
            return sessionLocale;
        }

        // Fallback to UI locale or default
        Locale uiLocale = UI.getCurrent().getLocale();
        Locale result = uiLocale != null ? uiLocale : Locale.ENGLISH;
        logger.debug("Using fallback locale: {}", result);
        return result;
    }
}

