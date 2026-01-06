package com.quizz.core.service;

import com.quizz.core.entity.Country;
import com.quizz.core.repository.CountryRepository;
import jakarta.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
@Order(1) // Execute first, before DataInitializer
public class CountryService {

    private static final Logger logger = LoggerFactory.getLogger(CountryService.class);

    private final CountryRepository countryRepository;

    public CountryService(CountryRepository countryRepository) {
        this.countryRepository = countryRepository;
    }

    // OPTIMIZATION: Countries are now persisted in the database
    // No need to re-initialize on every startup
    /*
    @PostConstruct
    @Transactional
    public void init() {
        logger.info("Initializing countries...");
        initializeCountries();
        logger.info("Countries initialization completed.");
    }
    */

    private void initializeCountries() {
        // Countries with their flags
        List<CountryData> countries = List.of(
            // European countries
            new CountryData("FRA", "France", getFranceFlag()),
            new CountryData("DEU", "Germany", getGermanyFlag()),
            new CountryData("ITA", "Italy", getItalyFlag()),
            new CountryData("ESP", "Spain", getSpainFlag()),
            new CountryData("GBR", "United Kingdom", getUKFlag()),
            new CountryData("PRT", "Portugal", getPortugalFlag()),
            new CountryData("BEL", "Belgium", getBelgiumFlag()),
            new CountryData("NLD", "Netherlands", getNetherlandsFlag()),
            new CountryData("GRC", "Greece", getGreeceFlag()),
            new CountryData("POL", "Poland", getPolandFlag()),
            new CountryData("AUT", "Austria", getAustriaFlag()),
            new CountryData("CHE", "Switzerland", getSwitzerlandFlag()),
            new CountryData("SWE", "Sweden", getSwedenFlag()),
            new CountryData("NOR", "Norway", getNorwayFlag()),
            new CountryData("DNK", "Denmark", getDenmarkFlag()),
            new CountryData("FIN", "Finland", getFinlandFlag()),
            new CountryData("IRL", "Ireland", getIrelandFlag()),
            new CountryData("CZE", "Czech Republic", getCzechFlag()),
            new CountryData("ROU", "Romania", getRomaniaFlag()),
            new CountryData("HUN", "Hungary", getHungaryFlag()),
            new CountryData("BGR", "Bulgaria", getBulgariaFlag()),
            new CountryData("HRV", "Croatia", getCroatiaFlag()),
            new CountryData("SVK", "Slovakia", getSlovakiaFlag()),
            new CountryData("SVN", "Slovenia", getSloveniaFlag()),
            new CountryData("LTU", "Lithuania", getLithuaniaFlag()),
            new CountryData("LVA", "Latvia", getLatviaFlag()),
            new CountryData("EST", "Estonia", getEstoniaFlag()),
            new CountryData("LUX", "Luxembourg", getLuxembourgFlag()),
            new CountryData("MLT", "Malta", getMaltaFlag()),
            new CountryData("CYP", "Cyprus", getCyprusFlag()),
            // Americas
            new CountryData("USA", "United States", getUSAFlag()),
            new CountryData("BRA", "Brasil", getBrasilFlag()),
            new CountryData("ARG", "Argentina", getArgentinaFlag()),
            new CountryData("PER", "Peru", getPeruFlag()),
            new CountryData("COL", "Colombia", getColombiaFlag()),
            new CountryData("MEX", "Mexico", getMexicoFlag()),
            new CountryData("URY", "Uruguay", getUruguayFlag()),
            // Oceania
            new CountryData("AUS", "Australia", getAustraliaFlag()),
            // Africa
            new CountryData("ZAF", "South Africa", getSouthAfricaFlag()),
            new CountryData("DZA", "Algeria", getAlgeriaFlag()),
            new CountryData("TUN", "Tunisia", getTunisiaFlag()),
            new CountryData("MAR", "Morocco", getMoroccoFlag()),
            // Asia
            new CountryData("CHN", "China", getChinaFlag()),
            new CountryData("JPN", "Japan", getJapanFlag()),
            new CountryData("IND", "India", getIndiaFlag()),
            new CountryData("PAK", "Pakistan", getPakistanFlag()),
            new CountryData("ISR", "Israel", getIsraelFlag()),
            new CountryData("SAU", "Saudi Arabia", getSaudiArabiaFlag()),
            new CountryData("MNG", "Mongolia", getMongoliaFlag()),
            // More Africa
            new CountryData("EGY", "Egypt", getEgyptFlag()),
            // Caribbean
            new CountryData("JAM", "Jamaica", getJamaicaFlag()),
            // More Europe
            new CountryData("RUS", "Russia", getRussiaFlag())
        );

        for (CountryData countryData : countries) {
            Optional<Country> existing = countryRepository.findBySigle(countryData.sigle);
            if (existing.isEmpty()) {
                Country country = new Country(countryData.sigle, countryData.name, countryData.flag);
                countryRepository.save(country);
                logger.info("Created country: {} ({})", countryData.name, countryData.sigle);
            }
        }
    }

    // Simple SVG flags (30px x 20px)
    private String getFranceFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='10' height='20' fill='#002395'/>" +
               "<rect x='10' width='10' height='20' fill='#FFFFFF'/>" +
               "<rect x='20' width='10' height='20' fill='#ED2939'/>" +
               "</svg>";
    }

    private String getGermanyFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='6.67' fill='#000000'/>" +
               "<rect y='6.67' width='30' height='6.67' fill='#DD0000'/>" +
               "<rect y='13.34' width='30' height='6.67' fill='#FFCE00'/>" +
               "</svg>";
    }

    private String getItalyFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='10' height='20' fill='#009246'/>" +
               "<rect x='10' width='10' height='20' fill='#FFFFFF'/>" +
               "<rect x='20' width='10' height='20' fill='#CE2B37'/>" +
               "</svg>";
    }

    private String getSpainFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='5' fill='#AA151B'/>" +
               "<rect y='5' width='30' height='10' fill='#F1BF00'/>" +
               "<rect y='15' width='30' height='5' fill='#AA151B'/>" +
               "</svg>";
    }

    private String getUKFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='20' fill='#012169'/>" +
               "<path d='M0,0 L30,20 M30,0 L0,20' stroke='#FFFFFF' stroke-width='3'/>" +
               "<path d='M0,0 L30,20 M30,0 L0,20' stroke='#C8102E' stroke-width='2'/>" +
               "<path d='M15,0 L15,20 M0,10 L30,10' stroke='#FFFFFF' stroke-width='5'/>" +
               "<path d='M15,0 L15,20 M0,10 L30,10' stroke='#C8102E' stroke-width='3'/>" +
               "</svg>";
    }

    private String getPortugalFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='12' height='20' fill='#006600'/>" +
               "<rect x='12' width='18' height='20' fill='#FF0000'/>" +
               "</svg>";
    }

    private String getBelgiumFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='10' height='20' fill='#000000'/>" +
               "<rect x='10' width='10' height='20' fill='#FDDA24'/>" +
               "<rect x='20' width='10' height='20' fill='#EF3340'/>" +
               "</svg>";
    }

    private String getNetherlandsFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='6.67' fill='#AE1C28'/>" +
               "<rect y='6.67' width='30' height='6.67' fill='#FFFFFF'/>" +
               "<rect y='13.34' width='30' height='6.67' fill='#21468B'/>" +
               "</svg>";
    }

    private String getGreeceFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='20' fill='#0D5EAF'/>" +
               "<rect y='2.22' width='30' height='2.22' fill='#FFFFFF'/>" +
               "<rect y='6.67' width='30' height='2.22' fill='#FFFFFF'/>" +
               "<rect y='11.11' width='30' height='2.22' fill='#FFFFFF'/>" +
               "<rect y='15.56' width='30' height='2.22' fill='#FFFFFF'/>" +
               "</svg>";
    }

    private String getPolandFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='10' fill='#FFFFFF'/>" +
               "<rect y='10' width='30' height='10' fill='#DC143C'/>" +
               "</svg>";
    }

    private String getAustriaFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='6.67' fill='#ED2939'/>" +
               "<rect y='6.67' width='30' height='6.67' fill='#FFFFFF'/>" +
               "<rect y='13.34' width='30' height='6.67' fill='#ED2939'/>" +
               "</svg>";
    }

    private String getSwitzerlandFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='20' fill='#FF0000'/>" +
               "<rect x='12' y='6' width='6' height='8' fill='#FFFFFF'/>" +
               "<rect x='9' y='9' width='12' height='2' fill='#FFFFFF'/>" +
               "</svg>";
    }

    private String getSwedenFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='20' fill='#006AA7'/>" +
               "<rect x='9' width='3' height='20' fill='#FECC00'/>" +
               "<rect y='8.5' width='30' height='3' fill='#FECC00'/>" +
               "</svg>";
    }

    private String getNorwayFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='20' fill='#BA0C2F'/>" +
               "<rect x='8' width='5' height='20' fill='#FFFFFF'/>" +
               "<rect y='7.5' width='30' height='5' fill='#FFFFFF'/>" +
               "<rect x='9' width='3' height='20' fill='#00205B'/>" +
               "<rect y='8.5' width='30' height='3' fill='#00205B'/>" +
               "</svg>";
    }

    private String getDenmarkFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='20' fill='#C60C30'/>" +
               "<rect x='9' width='3' height='20' fill='#FFFFFF'/>" +
               "<rect y='8.5' width='30' height='3' fill='#FFFFFF'/>" +
               "</svg>";
    }

    private String getFinlandFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='20' fill='#FFFFFF'/>" +
               "<rect x='9' width='3' height='20' fill='#003580'/>" +
               "<rect y='8.5' width='30' height='3' fill='#003580'/>" +
               "</svg>";
    }

    private String getIrelandFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='10' height='20' fill='#169B62'/>" +
               "<rect x='10' width='10' height='20' fill='#FFFFFF'/>" +
               "<rect x='20' width='10' height='20' fill='#FF883E'/>" +
               "</svg>";
    }

    private String getCzechFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='10' fill='#FFFFFF'/>" +
               "<rect y='10' width='30' height='10' fill='#D7141A'/>" +
               "<path d='M0,0 L15,10 L0,20 Z' fill='#11457E'/>" +
               "</svg>";
    }

    private String getRomaniaFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='10' height='20' fill='#002B7F'/>" +
               "<rect x='10' width='10' height='20' fill='#FCD116'/>" +
               "<rect x='20' width='10' height='20' fill='#CE1126'/>" +
               "</svg>";
    }

    private String getHungaryFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='6.67' fill='#CD2A3E'/>" +
               "<rect y='6.67' width='30' height='6.67' fill='#FFFFFF'/>" +
               "<rect y='13.34' width='30' height='6.67' fill='#436F4D'/>" +
               "</svg>";
    }

    private String getBulgariaFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='6.67' fill='#FFFFFF'/>" +
               "<rect y='6.67' width='30' height='6.67' fill='#00966E'/>" +
               "<rect y='13.34' width='30' height='6.67' fill='#D62612'/>" +
               "</svg>";
    }

    private String getCroatiaFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='6.67' fill='#FF0000'/>" +
               "<rect y='6.67' width='30' height='6.67' fill='#FFFFFF'/>" +
               "<rect y='13.34' width='30' height='6.67' fill='#171796'/>" +
               "</svg>";
    }

    private String getSlovakiaFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='6.67' fill='#FFFFFF'/>" +
               "<rect y='6.67' width='30' height='6.67' fill='#0B4EA2'/>" +
               "<rect y='13.34' width='30' height='6.67' fill='#EE1C25'/>" +
               "</svg>";
    }

    private String getSloveniaFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='6.67' fill='#FFFFFF'/>" +
               "<rect y='6.67' width='30' height='6.67' fill='#0000FF'/>" +
               "<rect y='13.34' width='30' height='6.67' fill='#FF0000'/>" +
               "</svg>";
    }

    private String getLithuaniaFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='6.67' fill='#FDB913'/>" +
               "<rect y='6.67' width='30' height='6.67' fill='#006A44'/>" +
               "<rect y='13.34' width='30' height='6.67' fill='#C1272D'/>" +
               "</svg>";
    }

    private String getLatviaFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='8' fill='#9E3039'/>" +
               "<rect y='8' width='30' height='4' fill='#FFFFFF'/>" +
               "<rect y='12' width='30' height='8' fill='#9E3039'/>" +
               "</svg>";
    }

    private String getEstoniaFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='6.67' fill='#0072CE'/>" +
               "<rect y='6.67' width='30' height='6.67' fill='#000000'/>" +
               "<rect y='13.34' width='30' height='6.67' fill='#FFFFFF'/>" +
               "</svg>";
    }

    private String getLuxembourgFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='6.67' fill='#ED2939'/>" +
               "<rect y='6.67' width='30' height='6.67' fill='#FFFFFF'/>" +
               "<rect y='13.34' width='30' height='6.67' fill='#00A1DE'/>" +
               "</svg>";
    }

    private String getMaltaFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='15' height='20' fill='#FFFFFF'/>" +
               "<rect x='15' width='15' height='20' fill='#CF142B'/>" +
               "</svg>";
    }

    private String getCyprusFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='20' fill='#FFFFFF'/>" +
               "<ellipse cx='15' cy='10' rx='8' ry='5' fill='#D57800'/>" +
               "</svg>";
    }

    // Americas flags
    private String getUSAFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='20' fill='#FFFFFF'/>" +
               "<rect width='30' height='1.54' fill='#B22234'/>" +
               "<rect y='3.08' width='30' height='1.54' fill='#B22234'/>" +
               "<rect y='6.15' width='30' height='1.54' fill='#B22234'/>" +
               "<rect y='9.23' width='30' height='1.54' fill='#B22234'/>" +
               "<rect y='12.31' width='30' height='1.54' fill='#B22234'/>" +
               "<rect y='15.38' width='30' height='1.54' fill='#B22234'/>" +
               "<rect y='18.46' width='30' height='1.54' fill='#B22234'/>" +
               "<rect width='12' height='10.77' fill='#3C3B6E'/>" +
               "</svg>";
    }

    private String getBrasilFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='20' fill='#009C3B'/>" +
               "<path d='M15,3 L27,10 L15,17 L3,10 Z' fill='#FFDF00'/>" +
               "<circle cx='15' cy='10' r='3.5' fill='#002776'/>" +
               "</svg>";
    }

    private String getArgentinaFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='6.67' fill='#75AADB'/>" +
               "<rect y='6.67' width='30' height='6.67' fill='#FFFFFF'/>" +
               "<rect y='13.34' width='30' height='6.67' fill='#75AADB'/>" +
               "<circle cx='15' cy='10' r='2' fill='none' stroke='#F6B40E' stroke-width='0.5'/>" +
               "<path d='M15,8 L15.5,9.5 L16,8.2 L16,9.5 L17,8.5 L16,9.7 L17.5,9.5 L16.2,10 L17.5,10.5 L16,10.3 L17,11.5 L16,10.5 L16,12 L15.5,10.5 L15,12 L15,10.5 L14,11.5 L15,10.3 L13.5,10.5 L14.8,10 L13.5,9.5 L15,9.7 L14,8.5 L15,9.5 Z' fill='#F6B40E'/>" +
               "</svg>";
    }

    private String getPeruFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='10' height='20' fill='#D91023'/>" +
               "<rect x='10' width='10' height='20' fill='#FFFFFF'/>" +
               "<rect x='20' width='10' height='20' fill='#D91023'/>" +
               "</svg>";
    }

    private String getColombiaFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='10' fill='#FCD116'/>" +
               "<rect y='10' width='30' height='5' fill='#003893'/>" +
               "<rect y='15' width='30' height='5' fill='#CE1126'/>" +
               "</svg>";
    }

    private String getMexicoFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='10' height='20' fill='#006847'/>" +
               "<rect x='10' width='10' height='20' fill='#FFFFFF'/>" +
               "<rect x='20' width='10' height='20' fill='#CE1126'/>" +
               "<circle cx='15' cy='10' r='2' fill='#A86829'/>" +
               "</svg>";
    }

    private String getUruguayFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='20' fill='#FFFFFF'/>" +
               "<rect y='2.22' width='30' height='2.22' fill='#0038A8'/>" +
               "<rect y='6.67' width='30' height='2.22' fill='#0038A8'/>" +
               "<rect y='11.11' width='30' height='2.22' fill='#0038A8'/>" +
               "<rect y='15.56' width='30' height='2.22' fill='#0038A8'/>" +
               "<rect width='12' height='11.11' fill='#FFFFFF'/>" +
               "<circle cx='6' cy='5.5' r='2' fill='#FCD116'/>" +
               "</svg>";
    }

    // Oceania flags
    private String getAustraliaFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='20' fill='#00008B'/>" +
               "<rect width='15' height='10' fill='#00008B'/>" +
               "<path d='M0,0 L15,10 M15,0 L0,10' stroke='#FFFFFF' stroke-width='2'/>" +
               "<path d='M0,0 L15,10 M15,0 L0,10' stroke='#FF0000' stroke-width='1'/>" +
               "<path d='M7.5,0 L7.5,10 M0,5 L15,5' stroke='#FFFFFF' stroke-width='3'/>" +
               "<path d='M7.5,0 L7.5,10 M0,5 L15,5' stroke='#FF0000' stroke-width='2'/>" +
               "</svg>";
    }

    // Africa flags
    private String getSouthAfricaFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='20' fill='#FFFFFF'/>" +
               "<rect width='30' height='6' fill='#E03C31'/>" +
               "<rect y='14' width='30' height='6' fill='#001489'/>" +
               "<path d='M0,0 L12,10 L0,20 Z' fill='#000000'/>" +
               "<path d='M0,2 L10,10 L0,18 Z' fill='#FFB81C'/>" +
               "<path d='M0,3 L9,10 L0,17 Z' fill='#007749'/>" +
               "</svg>";
    }

    private String getAlgeriaFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='15' height='20' fill='#006233'/>" +
               "<rect x='15' width='15' height='20' fill='#FFFFFF'/>" +
               "<circle cx='15' cy='10' r='4' fill='#D21034'/>" +
               "<circle cx='16' cy='10' r='3' fill='#FFFFFF'/>" +
               "<path d='M17,10 L18,9 L17.5,10.5 L19,10 L17.5,10.5 L18,12 Z' fill='#D21034'/>" +
               "</svg>";
    }

    private String getTunisiaFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='20' fill='#E70013'/>" +
               "<circle cx='15' cy='10' r='5' fill='#FFFFFF'/>" +
               "<circle cx='16' cy='10' r='4' fill='#E70013'/>" +
               "<circle cx='17' cy='10' r='3' fill='#FFFFFF'/>" +
               "<path d='M16,10 L17,9 L16.5,10.5 L18,10 L16.5,10.5 L17,12 Z' fill='#E70013'/>" +
               "</svg>";
    }

    private String getMoroccoFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='20' fill='#C1272D'/>" +
               "<path d='M15,6 L16,9 L19,9 L16.5,11 L17.5,14 L15,12 L12.5,14 L13.5,11 L11,9 L14,9 Z' fill='none' stroke='#006233' stroke-width='0.8'/>" +
               "</svg>";
    }

    // Asia flags
    private String getChinaFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='20' fill='#DE2910'/>" +
               "<path d='M5,4 L5.5,5.5 L7,5.5 L5.8,6.3 L6.2,8 L5,7 L3.8,8 L4.2,6.3 L3,5.5 L4.5,5.5 Z' fill='#FFDE00'/>" +
               "<path d='M9,2 L9.2,2.5 L9.7,2.5 L9.3,2.8 L9.5,3.3 L9,3 L8.5,3.3 L8.7,2.8 L8.3,2.5 L8.8,2.5 Z' fill='#FFDE00'/>" +
               "<path d='M10,4 L10.2,4.5 L10.7,4.5 L10.3,4.8 L10.5,5.3 L10,5 L9.5,5.3 L9.7,4.8 L9.3,4.5 L9.8,4.5 Z' fill='#FFDE00'/>" +
               "<path d='M10,7 L10.2,7.5 L10.7,7.5 L10.3,7.8 L10.5,8.3 L10,8 L9.5,8.3 L9.7,7.8 L9.3,7.5 L9.8,7.5 Z' fill='#FFDE00'/>" +
               "<path d='M9,9 L9.2,9.5 L9.7,9.5 L9.3,9.8 L9.5,10.3 L9,10 L8.5,10.3 L8.7,9.8 L8.3,9.5 L8.8,9.5 Z' fill='#FFDE00'/>" +
               "</svg>";
    }

    private String getJapanFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='20' fill='#FFFFFF'/>" +
               "<circle cx='15' cy='10' r='5' fill='#BC002D'/>" +
               "</svg>";
    }

    private String getIndiaFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='6.67' fill='#FF9933'/>" +
               "<rect y='6.67' width='30' height='6.67' fill='#FFFFFF'/>" +
               "<rect y='13.34' width='30' height='6.67' fill='#138808'/>" +
               "<circle cx='15' cy='10' r='3' fill='none' stroke='#000080' stroke-width='0.5'/>" +
               "<circle cx='15' cy='10' r='0.5' fill='#000080'/>" +
               "</svg>";
    }

    private String getPakistanFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='7.5' height='20' fill='#FFFFFF'/>" +
               "<rect x='7.5' width='22.5' height='20' fill='#01411C'/>" +
               "<circle cx='18' cy='10' r='4' fill='#FFFFFF'/>" +
               "<circle cx='19' cy='10' r='3' fill='#01411C'/>" +
               "<path d='M19,10 L20,9 L19.5,10.5 L21,10 L19.5,10.5 L20,12 Z' fill='#FFFFFF'/>" +
               "</svg>";
    }

    private String getIsraelFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='20' fill='#FFFFFF'/>" +
               "<rect y='3' width='30' height='2' fill='#0038B8'/>" +
               "<rect y='15' width='30' height='2' fill='#0038B8'/>" +
               "<path d='M15,7 L18,10 L15,13 L12,10 Z M15,9 L17,10 L15,11 L13,10 Z' fill='#0038B8'/>" +
               "</svg>";
    }

    private String getSaudiArabiaFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='20' fill='#165B33'/>" +
               "<text x='10' y='13' fill='#FFFFFF' font-size='8' font-weight='bold'>SA</text>" +
               "</svg>";
    }

    private String getMongoliaFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='10' height='20' fill='#C4272F'/>" +
               "<rect x='10' width='10' height='20' fill='#015197'/>" +
               "<rect x='20' width='10' height='20' fill='#C4272F'/>" +
               "<circle cx='5' cy='10' r='2' fill='#FFD900'/>" +
               "</svg>";
    }

    private String getEgyptFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='6.67' fill='#CE1126'/>" +
               "<rect y='6.67' width='30' height='6.67' fill='#FFFFFF'/>" +
               "<rect y='13.34' width='30' height='6.67' fill='#000000'/>" +
               "<circle cx='15' cy='10' r='2' fill='#C09300'/>" +
               "</svg>";
    }

    private String getJamaicaFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='20' fill='#000000'/>" +
               "<path d='M0,0 L30,20 M30,0 L0,20' stroke='#FED100' stroke-width='2'/>" +
               "<path d='M0,0 L15,10 L0,20 Z M30,0 L15,10 L30,20 Z' fill='#009B3A'/>" +
               "</svg>";
    }

    private String getRussiaFlag() {
        return "<svg width='30' height='20' xmlns='http://www.w3.org/2000/svg'>" +
               "<rect width='30' height='6.67' fill='#FFFFFF'/>" +
               "<rect y='6.67' width='30' height='6.67' fill='#0039A6'/>" +
               "<rect y='13.34' width='30' height='6.67' fill='#D52B1E'/>" +
               "</svg>";
    }

    public List<Country> findAll() {
        return countryRepository.findAll();
    }

    public Optional<Country> findBySigle(String sigle) {
        return countryRepository.findBySigle(sigle);
    }

    public Optional<Country> findByCountryName(String countryName) {
        return countryRepository.findByCountryName(countryName);
    }

    public Country save(Country country) {
        return countryRepository.save(country);
    }

    private static class CountryData {
        final String sigle;
        final String name;
        final String flag;

        CountryData(String sigle, String name, String flag) {
            this.sigle = sigle;
            this.name = name;
            this.flag = flag;
        }
    }
}

