# Correction de l'affichage du drapeau du pays - 2026-01-03

## Problème identifié

Le drapeau du pays ne s'affichait pas à côté du logo utilisateur malgré les modifications précédentes.

### Cause racine

L'ordre des opérations dans `DataInitializer.java` causait la perte de l'association pays-utilisateur :

1. L'utilisateur était créé
2. Le pays était associé avec `setCountry()` et `save()`
3. **PUIS** `updateAdminFlag()` ou `updatePublicFlag()` étaient appelés
4. Ces méthodes rechargeaient l'utilisateur depuis la base avec `findById()`, perdant l'association au pays
5. Seul le flag admin/public était sauvegardé

## Solution appliquée

### Fichier modifié : `DataInitializer.java`

**Changement 1 - Utilisateur Admin :**
- ✅ Marquer comme admin EN PREMIER avec `updateAdminFlag()`
- ✅ PUIS associer le pays avec `setCountry()` et `save()`

**Changement 2 - Utilisateurs Publics :**
- ✅ Marquer comme public EN PREMIER avec `updatePublicFlag()`
- ✅ PUIS associer le pays avec `setCountry()` et `save()`

**Changement 3 - Affichage du SVG dans `QuizListView.java` :**
- ✅ Utilisation de `StreamResource` au lieu de `innerHTML` pour afficher le SVG
- ✅ Ajout de logs détaillés pour diagnostiquer les problèmes

## Comment tester

### Étape 1 : Redémarrer l'application
```
⚠️ IMPORTANT : Vous devez redémarrer l'application pour recréer la base de données H2 en mémoire
```

### Étape 2 : Vérifier les logs
Après redémarrage, vérifiez dans `logs/application.log` :

```
✅ "Admin user linked to France" - L'admin est bien lié à la France
✅ "Linked <nom> to <pays>" - Les utilisateurs publics sont liés à leurs pays
✅ "User has country: France" - L'utilisateur a un pays lors de l'affichage
✅ "Creating flag display for country: France" - Le drapeau est créé
```

### Étape 3 : Vérifier visuellement
1. Se connecter avec : `administrateur@quiz.admin` / `quizz2025!!`
2. Le drapeau français (🇫🇷) doit apparaître à côté du logo utilisateur
3. Se connecter avec un autre utilisateur (ex: Barack Obama)
4. Le drapeau américain (🇺🇸) doit apparaître

## Logs de diagnostic

Les logs suivants ont été ajoutés dans `QuizListView.java` :

```java
logger.info("Checking country flag for user: {}", currentUser.getName());
logger.info("User has country: {}", currentUser.getCountry().getCountryName());
logger.info("Flag SVG length: {}", flagSvg.length());
logger.info("Creating flag display for country: {}", currentUser.getCountry().getCountryName());
logger.info("Flag container added to layout");
```

Si le drapeau ne s'affiche toujours pas, ces logs indiqueront exactement où le problème se situe.

## Fichiers modifiés

1. ✅ `src/main/java/com/quizz/core/DataInitializer.java`
   - Inversion de l'ordre des opérations pour admin et utilisateurs publics
   
2. ✅ `src/main/java/com/quizz/core/service/UserService.java`
   - Ajout de la méthode `save(User user)`

3. ✅ `src/main/java/com/quizz/core/ui/QuizListView.java`
   - Affichage du SVG via `StreamResource`
   - Ajout de logs détaillés

## Prochaines étapes

Si le problème persiste après redémarrage :
1. Vérifier les logs pour voir où ça bloque
2. Vérifier que `countryService.findBySigle("FRA")` trouve bien la France
3. Vérifier que le SVG est bien présent en base de données

