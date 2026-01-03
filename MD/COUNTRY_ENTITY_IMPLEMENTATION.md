# Country Entity Implementation

## Description
Cette implémentation ajoute une entité `Country` pour gérer les pays dans l'application.

## Fichiers créés

### 1. Entity - Country.java
**Emplacement:** `src/main/java/com/quizz/core/entity/Country.java`

L'entité contient les champs suivants :
- `id` : Identifiant unique (BIGSERIAL)
- `sigle` : Code pays ISO à 3 caractères (ex: FRA, DEU, ITA) - UNIQUE
- `countryName` : Nom du pays (max 100 caractères)
- `countryFlag` : Contenu SVG du drapeau (30px x 20px) stocké en TEXT/CLOB

### 2. Repository - CountryRepository.java
**Emplacement:** `src/main/java/com/quizz/core/repository/CountryRepository.java`

Interface Spring Data JPA avec les méthodes :
- `findBySigle(String sigle)` : Recherche par code pays
- `findByCountryName(String countryName)` : Recherche par nom

### 3. Service - CountryService.java
**Emplacement:** `src/main/java/com/quizz/core/service/CountryService.java`

Service qui implémente `CommandLineRunner` pour initialiser automatiquement les pays au démarrage de l'application.

**Pays initialisés (44 pays) :**

**Europe (30 pays):**
- France (FRA)
- Germany (DEU)
- Italy (ITA)
- Spain (ESP)
- United Kingdom (GBR)
- Portugal (PRT)
- Belgium (BEL)
- Netherlands (NLD)
- Greece (GRC)
- Poland (POL)
- Austria (AUT)
- Switzerland (CHE)
- Sweden (SWE)
- Norway (NOR)
- Denmark (DNK)
- Finland (FIN)
- Ireland (IRL)
- Czech Republic (CZE)
- Romania (ROU)
- Hungary (HUN)
- Bulgaria (BGR)
- Croatia (HRV)
- Slovakia (SVK)
- Slovenia (SVN)
- Lithuania (LTU)
- Latvia (LVA)
- Estonia (EST)
- Luxembourg (LUX)
- Malta (MLT)
- Cyprus (CYP)

**Americas (7 pays):**
- United States (USA)
- Brasil (BRA)
- Argentina (ARG)
- Peru (PER)
- Colombia (COL)
- Mexico (MEX)
- Uruguay (URY)

**Oceania (1 pays):**
- Australia (AUS)

**Africa (4 pays):**
- South Africa (ZAF)
- Algeria (DZA)
- Tunisia (TUN)
- Morocco (MAR)

**Asia (2 pays):**
- China (CHN)
- Japan (JPN)

Chaque pays est initialisé avec son drapeau SVG (30px x 20px).

### 4. Script SQL - create_countries_table.sql
**Emplacement:** `create_countries_table.sql`

Script pour créer manuellement la table si nécessaire.

## Fonctionnement

1. **Initialisation automatique** : Au démarrage de l'application, le service `CountryService` vérifie si les pays existent dans la base de données. S'ils n'existent pas, ils sont créés automatiquement avec leurs drapeaux SVG.

2. **Drapeaux SVG** : Chaque drapeau est stocké en format SVG (30px x 20px) directement dans la base de données. Les SVG sont simples mais représentatifs des drapeaux réels.

3. **Codes ISO** : Les sigles utilisent les codes ISO 3166-1 alpha-3 (3 lettres) pour une standardisation internationale.

## Utilisation

Pour utiliser l'entité Country dans votre code :

```java
@Autowired
private CountryService countryService;

// Récupérer tous les pays
List<Country> countries = countryService.findAll();

// Rechercher un pays par sigle
Optional<Country> france = countryService.findBySigle("FRA");

// Rechercher un pays par nom
Optional<Country> germany = countryService.findByCountryName("Germany");
```

## Configuration base de données

Si vous utilisez JPA avec `spring.jpa.hibernate.ddl-auto=update` ou `create`, la table sera créée automatiquement.

Sinon, exécutez le script SQL `create_countries_table.sql` manuellement.

## Extension

Pour ajouter d'autres pays :
1. Ajouter une entrée dans la méthode `initializeCountries()` du service
2. Créer une méthode pour générer le SVG du drapeau (ex: `getUSAFlag()`)
3. Redémarrer l'application

## Notes techniques

- Les drapeaux SVG sont optimisés pour une taille de 30x20 pixels
- Le champ `country_flag` utilise `@Lob` avec `FetchType.LAZY` pour optimiser les performances
- Les sigles sont automatiquement convertis en majuscules lors de l'enregistrement
- L'unicité du sigle est garantie au niveau de la base de données

