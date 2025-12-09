# 🚀 Guide de démarrage rapide

## Problème rencontré
L'erreur `no DevModeHandlerManager implementation found` signifie que Vaadin ne peut pas démarrer en mode développement.

## ✅ SOLUTION SIMPLE : Démarrer depuis IntelliJ IDEA

### Étapes à suivre :

1. **Ouvrir IntelliJ IDEA** avec ce projet

2. **Trouver la classe Application** :
   - Naviguez vers : `src/main/java/com/quizz/Application.java`
   - OU pressez `Ctrl+N` et tapez "Application"

3. **Lancer l'application** :
   - Cliquez droit sur le fichier `Application.java`
   - Sélectionnez **"Run 'Application.main()'"**
   
   OU
   
   - Cliquez sur l'icône verte **▶** à côté de `public class Application`

4. **Attendre le démarrage** :
   - La console affichera le logo Spring Boot
   - Attendez le message : `Started Application in X.XXX seconds`

5. **Accéder à l'application** :
   - Un navigateur devrait s'ouvrir automatiquement
   - Sinon, ouvrez manuellement : **http://localhost:8080**

## 🎮 Utilisation de l'application

### Page d'accueil (/)
- Vous verrez la liste des quiz
- Un quiz "General Knowledge Quiz" avec 10 questions est déjà créé
- Vous pouvez créer de nouveaux quiz avec le formulaire en haut

### Jouer à un quiz
1. Cliquez sur le bouton **"Play"** à côté d'un quiz
2. Les questions s'affichent une par une
3. **Sélectionnez une réponse** - le bouton "Next" s'active automatiquement
4. Cliquez sur "Next" pour passer à la question suivante
5. Vous verrez un feedback (✓ ou ✗) sur votre réponse
6. Utilisez "Previous" pour revenir en arrière

## 🔧 Si IntelliJ affiche des erreurs

### Vérifier le SDK Java :
1. **File → Project Structure** (Ctrl+Alt+Shift+S)
2. Onglet **Project** :
   - SDK : Sélectionnez Java 17 ou supérieur (Java 21 ou 23 recommandé)
   - Language level : 21
3. **Apply** puis **OK**

### Recharger le projet Maven :
1. Cliquez droit sur `pom.xml`
2. **Maven → Reload Project**

## 📝 Fonctionnalités implémentées

✅ Entité Quiz avec propriété nom  
✅ Vue pour créer des quiz  
✅ Questions liées aux quiz (relation ManyToOne)  
✅ Vue pour afficher les questions une par une  
✅ Bouton "Next" activé uniquement quand une réponse est sélectionnée  
✅ 10 questions chargées automatiquement au démarrage  
✅ Sélection du quiz avant de voir les questions  

## ❌ Pourquoi Maven ne fonctionne pas ?

Le problème vient de la version de Java utilisée par Maven :
- **Maven utilise** : Java 11 (class version 55.0)
- **Projet nécessite** : Java 17+ (class version 61.0)
- **IntelliJ utilise** : Java 23 (correct)

C'est pourquoi il faut démarrer depuis IntelliJ qui utilise le bon JDK.

## 💡 Alternative : Corriger Maven (optionnel)

Si vous voulez vraiment utiliser Maven en ligne de commande :

```cmd
# Trouver Java 17+
where java

# Configurer JAVA_HOME
set JAVA_HOME=C:\Users\athom\.jdks\azul-23.0.2
set PATH=%JAVA_HOME%\bin;%PATH%

# Vérifier
java -version

# Démarrer
cd C:\Users\athom\IdeaProjects\quizz1
mvnw.cmd spring-boot:run
```

## 🆘 Besoin d'aide ?

Si l'application ne démarre toujours pas :
1. Vérifiez que le port 8080 n'est pas déjà utilisé
2. Vérifiez les logs dans la console IntelliJ
3. Assurez-vous que Java 17+ est installé

## 🎉 Succès !

Quand l'application démarre, vous verrez :
- Le logo Spring Boot dans la console
- Le message : `Tomcat started on port 8080`
- Le navigateur s'ouvre sur http://localhost:8080
- La page d'accueil avec la liste des quiz

Amusez-vous bien ! 🚀

