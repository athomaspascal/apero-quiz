# Liaison des utilisateurs aux pays - 2026-01-02

## Objectif
Lier automatiquement l'utilisateur administrateur à la France et tous les utilisateurs célèbres à leurs pays d'origine respectifs lors de l'initialisation de l'application.

## Modifications effectuées

### 1. DataInitializer.java
**Emplacement:** `src/main/java/com/quizz/core/DataInitializer.java`

#### Changements principaux:

1. **Ajout du CountryService**
   - Injection de `CountryService` dans le `CommandLineRunner`
   - Passage du service aux méthodes de création d'utilisateurs

2. **Liaison de l'administrateur**
   - L'utilisateur admin est maintenant lié automatiquement à la France (FRA)
   - Code ajouté:
     ```java
     countryService.findBySigle("FRA").ifPresent(admin::setCountry);
     ```

3. **Ajout des codes pays pour tous les utilisateurs célèbres**
   - Format du tableau modifié: `{Name, Initials, Gender, CountryCode}`
   - Ajout d'un 4ème élément (code pays ISO) pour chaque personne célèbre

4. **Liaison automatique des utilisateurs célèbres**
   - Chaque utilisateur célèbre est lié à son pays lors de la création
   - Code ajouté:
     ```java
     countryService.findBySigle(countryCode).ifPresent(country -> {
         user.setCountry(country);
         logger.debug("Linked {} to {}", name, country.getCountryName());
     });
     ```

## Liste des utilisateurs et leurs pays

### 🇫🇷 France (FRA) - 8 utilisateurs
- **Administrateur** (Admin user)
- Coco Chanel
- Napoleon Bonaparte
- Joan of Arc
- Charles de Gaulle
- Simone de Beauvoir
- Victor Hugo
- Voltaire
- Molière

### 🇺🇸 United States (USA) - 26 utilisateurs
- Barack Obama
- Martin Luther King Jr
- Abraham Lincoln
- Steve Jobs
- Bill Gates
- Mark Zuckerberg
- Oprah Winfrey
- Walt Disney
- Michael Jackson
- Elvis Presley
- Madonna
- Beyoncé
- Muhammad Ali
- Serena Williams
- Michael Jordan
- Tiger Woods
- Neil Armstrong
- Carl Sagan
- Rosa Parks
- Helen Keller
- George Washington
- Thomas Jefferson
- Franklin D Roosevelt
- John F Kennedy
- Mark Twain
- Ernest Hemingway
- Toni Morrison
- Maya Angelou

### 🇬🇧 United Kingdom (GBR) - 13 utilisateurs
- Winston Churchill
- Charles Darwin
- Isaac Newton
- William Shakespeare
- The Beatles
- Stephen Hawking
- Jane Goodall
- Florence Nightingale
- Elizabeth II
- Margaret Thatcher
- Virginia Woolf
- Jane Austen
- J.K. Rowling
- George Orwell
- Agatha Christie

### 🇩🇪 Germany (DEU) - 6 utilisateurs
- Albert Einstein
- Ludwig van Beethoven
- Anne Frank
- Karl Marx
- Friedrich Nietzsche
- Angela Merkel

### 🇮🇹 Italy (ITA) - 3 utilisateurs
- Leonardo da Vinci
- Julius Caesar
- Dante Alighieri

### 🇪🇸 Spain (ESP) - 2 utilisateurs
- Pablo Picasso
- Miguel de Cervantes

### 🇳🇱 Netherlands (NLD) - 1 utilisateur
- Vincent van Gogh

### 🇲🇽 Mexico (MEX) - 1 utilisateur
- Frida Kahlo

### 🇿🇦 South Africa (ZAF) - 2 utilisateurs
- Nelson Mandela
- Elon Musk

### 🇵🇱 Poland (POL) - 1 utilisateur
- Marie Curie

### 🇦🇹 Austria (AUT) - 2 utilisateurs
- Wolfgang Mozart
- Sigmund Freud

### 🇬🇷 Greece (GRC) - 4 utilisateurs
- Socrates
- Plato
- Aristotle
- Alexander the Great

### 🇨🇭 Switzerland (CHE) - 1 utilisateur
- Roger Federer

### 🇵🇹 Portugal (PRT) - 1 utilisateur
- Cristiano Ronaldo

### 🇧🇷 Brasil (BRA) - 1 utilisateur
- Pelé

### 🇦🇷 Argentina (ARG) - 4 utilisateurs
- Lionel Messi
- Pope Francis
- Eva Perón
- Che Guevara

### 🇨🇳 China (CHN) - 2 utilisateurs
- Confucius
- Mao Zedong

### 🇨🇴 Colombia (COL) - 1 utilisateur
- Gabriel García Márquez

### Pays non encore dans le système (NULL)
Les utilisateurs suivants ont des codes pays qui ne sont pas encore dans la base de données. Ils auront `country_id = NULL`:

- **Cleopatra** (EGY - Egypt) - Égypte non ajoutée
- **Mother Teresa** (IND - India) - Inde non ajoutée
- **Mahatma Gandhi** (IND - India)
- **Buddha** (IND - India)
- **Dalai Lama** (IND - India)
- **Indira Gandhi** (IND - India)
- **Usain Bolt** (JAM - Jamaica) - Jamaïque non ajoutée
- **Yuri Gagarin** (RUS - Russia) - Russie non ajoutée
- **Vladimir Lenin** (RUS - Russia)
- **Joseph Stalin** (RUS - Russia)
- **Leo Tolstoy** (RUS - Russia)
- **Fyodor Dostoevsky** (RUS - Russia)
- **Malala Yousafzai** (PAK - Pakistan) - Pakistan non ajouté
- **Jesus Christ** (ISR - Israel) - Israël non ajouté
- **Prophet Muhammad** (SAU - Saudi Arabia) - Arabie Saoudite non ajoutée
- **Genghis Khan** (MNG - Mongolia) - Mongolie non ajoutée

## Statistiques

### Par pays présent dans le système:
- 🇺🇸 **USA**: 26 utilisateurs (28%)
- 🇬🇧 **GBR**: 13 utilisateurs (14%)
- 🇫🇷 **FRA**: 8 utilisateurs + Admin (9%)
- 🇩🇪 **DEU**: 6 utilisateurs (6%)
- 🇬🇷 **GRC**: 4 utilisateurs (4%)
- 🇦🇷 **ARG**: 4 utilisateurs (4%)
- 🇮🇹 **ITA**: 3 utilisateurs (3%)
- 🇦🇹 **AUT**: 2 utilisateurs (2%)
- 🇪🇸 **ESP**: 2 utilisateurs (2%)
- 🇿🇦 **ZAF**: 2 utilisateurs (2%)
- 🇨🇳 **CHN**: 2 utilisateurs (2%)
- Autres (1 utilisateur chacun): 11 pays

### Pays manquants:
- **Inde (IND)**: 5 utilisateurs en attente
- **Russie (RUS)**: 5 utilisateurs en attente
- **Égypte (EGY)**: 1 utilisateur
- **Jamaïque (JAM)**: 1 utilisateur
- **Pakistan (PAK)**: 1 utilisateur
- **Israël (ISR)**: 1 utilisateur
- **Arabie Saoudite (SAU)**: 1 utilisateur
- **Mongolie (MNG)**: 1 utilisateur

**Total: 16 utilisateurs non liés** car leurs pays ne sont pas dans le système.

## Recommandation

Pour lier tous les utilisateurs célèbres, il faudrait ajouter les pays manquants à la table `countries`:
- India (IND)
- Russia (RUS)
- Egypt (EGY)
- Jamaica (JAM)
- Pakistan (PAK)
- Israel (ISR)
- Saudi Arabia (SAU)
- Mongolia (MNG)

## Déploiement

### Au prochain démarrage de l'application:

1. **Si les utilisateurs n'existent pas encore:**
   - Tous les nouveaux utilisateurs seront créés avec leur pays
   - L'admin sera lié à la France
   - 82 utilisateurs célèbres seront créés (98 total si on compte l'admin)
   - 82 liaisons pays seront effectuées (sauf pour les 16 utilisateurs dont le pays n'existe pas)

2. **Si les utilisateurs existent déjà:**
   - Aucune modification (les utilisateurs existants ne sont pas mis à jour)
   - Pour mettre à jour les utilisateurs existants, il faudra exécuter un script SQL ou un script de migration

## Script de migration (optionnel)

Si vous voulez mettre à jour les utilisateurs existants, voici un exemple de script SQL:

```sql
-- Lier l'admin à la France
UPDATE users SET country_id = (SELECT country_id FROM countries WHERE sigle = 'FRA')
WHERE email = 'administrateur@quiz.admin';

-- Lier Barack Obama aux USA
UPDATE users SET country_id = (SELECT country_id FROM countries WHERE sigle = 'USA')
WHERE email = 'barack.obama@public.quiz';

-- ... etc pour chaque utilisateur
```

## Logs

Les logs afficheront :
- `Default admin user created: administrateur@quiz.admin / quizz2025!! (linked to France)`
- `Linked Barack Obama to United States` (en mode DEBUG)
- `Public users initialization complete: X created, Y skipped (already exist)`

## Impact

### Base de données
- Nouvelle colonne `country_id` dans la table `users`
- Contrainte de clé étrangère vers `countries`

### Application
- ✅ Admin lié à la France
- ✅ 82 utilisateurs célèbres liés à leurs pays (sur 98)
- ✅ 16 utilisateurs auront `country_id = NULL` (pays non dans le système)

### Fonctionnalités futures possibles
- Afficher le drapeau du pays à côté du nom d'utilisateur
- Classement par pays
- Statistiques par nationalité
- Filtres par pays dans l'interface admin

---

**Date de modification:** 2026-01-02
**Fichiers modifiés:** 1 (DataInitializer.java)
**Utilisateurs affectés:** 99 (1 admin + 98 publics)
**Pays représentés:** 21 pays différents dans le système

