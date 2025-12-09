# Solution au problème de démarrage

## Problème identifié
L'application ne peut pas démarrer car:
1. Maven utilise Java 11 (class file version 55.0)
2. Le projet nécessite Java 17+ (Vaadin 24.9.6 est compilé avec Java 17 - class file version 61.0)
3. Le mode développement Vaadin nécessite le serveur de dev qui n'est pas disponible

## Solution : Démarrer via IntelliJ IDEA

### Étape 1: Ouvrir la classe Application
1. Dans IntelliJ, naviguez vers `src/main/java/com/quizz/Application.java`
2. Ou utilisez Ctrl+N et tapez "Application"

### Étape 2: Exécuter l'application
1. Cliquez droit sur la classe `Application`
2. Sélectionnez "Run 'Application.main()'"
   
OU

1. Cliquez sur l'icône verte ▶ à côté de `public class Application` ou de la méthode `main()`

### Étape 3: Configuration Java dans IntelliJ (si nécessaire)
Si vous obtenez toujours une erreur:

1. **File → Project Structure** (Ctrl+Alt+Shift+S)
2. **Project** → Assurez-vous que "SDK" est Java 17 ou supérieur
3. **Modules** → Vérifiez que "Language level" est 21
4. Appliquez et fermez

### Étape 4: Vérifier le démarrage
L'application devrait démarrer et vous verrez dans la console :
```
  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 
 :: Spring Boot ::
```

Puis :
```
INFO  com.quizz.Application  : Started Application in X.XXX seconds
```

### Étape 5: Accéder à l'application
1. Un navigateur devrait s'ouvrir automatiquement sur http://localhost:8080
2. Si ce n'est pas le cas, ouvrez manuellement http://localhost:8080

## Ce qui a été configuré

J'ai ajouté dans `application.properties`:
```properties
vaadin.frontend.hotdeploy=false
vaadin.productionMode=true
```

Ces paramètres désactivent le serveur de développement Vaadin et utilisent le mode production (qui ne nécessite pas de build frontend séparé si les bundles sont présents).

## Fonctionnement de l'application

1. **Page d'accueil** (/) : 
   - Liste des quiz
   - Formulaire pour créer un nouveau quiz
   - Bouton "Play" pour chaque quiz

2. **Vue Quiz** (/quiz-questions/{id}) :
   - Affiche les questions une par une
   - Le bouton "Next" est désactivé jusqu'à ce qu'une réponse soit sélectionnée
   - Feedback immédiat sur la réponse
   - Navigation Previous/Next

3. **Base de données** :
   - H2 en mémoire
   - Les questions du fichier JSON sont automatiquement chargées au démarrage
   - Créées dans un quiz par défaut "General Knowledge Quiz"

## Alternative si IntelliJ ne fonctionne pas

Si vous devez absolument utiliser Maven en ligne de commande:

### Option 1: Configurer JAVA_HOME
```cmd
# Trouver Java 17+
where java

# Définir JAVA_HOME (exemple)
set JAVA_HOME=C:\Program Files\Java\jdk-17
set PATH=%JAVA_HOME%\bin;%PATH%

# Vérifier
java -version
mvn -version

# Démarrer
mvnw.cmd spring-boot:run
```

### Option 2: Utiliser le JDK embarqué IntelliJ
```cmd
set JAVA_HOME=C:\Users\athom\.jdks\azul-23.0.2
set PATH=%JAVA_HOME%\bin;%PATH%
mvnw.cmd spring-boot:run
```

## Vérification

Une fois l'application démarrée, vous devriez pouvoir:
- ✅ Voir la liste des quiz (dont "General Knowledge Quiz")
- ✅ Cliquer sur "Play" pour un quiz
- ✅ Voir les 10 questions chargées depuis le JSON
- ✅ Le bouton "Next" reste grisé jusqu'à sélection d'une réponse
- ✅ Naviguer entre les questions
- ✅ Créer de nouveaux quiz

