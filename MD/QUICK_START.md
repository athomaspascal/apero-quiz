# 🚀 GUIDE DE DÉMARRAGE RAPIDE

## ⚡ Lancement en 3 Minutes

### Étape 1 : Démarrer l'Application
```bash
start-app.bat
```
**Attendre** que le serveur démarre (environ 30-60 secondes)

### Étape 2 : Ouvrir le Navigateur
Aller sur : **http://localhost:8080**

### Étape 3 : Se Connecter
- **Email** : `test@example.com`
- **Mot de passe** : `password123`

---

## 🎮 Test de la Fonctionnalité de Partage (1 Personne)

1. **Se connecter** avec le compte de test
2. Aller sur **"New Quiz"** (page d'accueil)
3. Cliquer sur **"Share"** à côté d'un quiz
4. Un dialogue s'ouvre avec :
   - Un QR code
   - Un code de session (ex: `ABC12345`)
5. Noter le code de session
6. Cliquer sur **"Go to Session Room"**
7. Cliquer sur **"Start My Quiz"**
8. Faire le quiz
9. Voir votre score !

---

## 👥 Test Multi-Utilisateurs (2+ Personnes)

### Préparation

**Navigateur 1** (Créateur)
1. Se connecter : `test@example.com` / `password123`
2. Cliquer "Share" sur un quiz
3. Noter le **code de session**

**Navigateur 2** (Participant 1)
1. Ouvrir un autre navigateur (ou fenêtre privée)
2. Créer un compte via "Sign up"
   - Nom : Alice
   - Email : alice@test.com
   - Téléphone : +33 6 11 11 11 11
   - Mot de passe : alice123

**Navigateur 3** (Participant 2) - Optionnel
1. Ouvrir un 3ème navigateur
2. Créer un compte via "Sign up"
   - Nom : Bob
   - Email : bob@test.com
   - Téléphone : +33 6 22 22 22 22
   - Mot de passe : bob123

### Rejoindre la Session

**Pour chaque participant** :

**Option A : Via le Menu**
1. Cliquer sur "Join Session" dans le menu
2. Entrer le code de session
3. Cliquer "Join Session"

**Option B : Via l'URL Directe**
1. Copier l'URL : `http://localhost:8080/quiz-session/CODE`
2. Remplacer `CODE` par le code de session
3. Coller dans la barre d'adresse

### Lancer le Quiz

**Chaque participant** :
1. Dans la Session Room, cliquer **"Start My Quiz"**
2. Répondre aux questions
3. À la fin, cliquer **"View Leaderboard"**

### Voir le Classement

Le **leaderboard** s'affiche avec :
- 🥇 1ère place
- 🥈 2ème place  
- 🥉 3ème place
- Scores de tous les participants

---

## 🎯 Scénarios de Test

### Scénario 1 : Créer un Utilisateur
1. Sur la page de connexion, cliquer **"Sign up"**
2. Remplir le formulaire
3. Cliquer **"Create Account"**
4. Se connecter avec les nouveaux identifiants

### Scénario 2 : Mot de Passe Oublié
1. Sur la page de connexion, cliquer **"Forgot password"**
2. Entrer votre email
3. Cliquer **"Send Reset Instructions"**
4. (Simulation - l'email n'est pas vraiment envoyé)

### Scénario 3 : Gérer les Utilisateurs
1. Se connecter en tant qu'admin
2. Aller sur **"Users"** dans le menu
3. Voir la liste des utilisateurs
4. Cliquer **"Create User"** pour ajouter
5. Cliquer **"Edit"** pour modifier
6. Cliquer **"Delete"** pour supprimer

### Scénario 4 : Créer un Quiz
1. Sur la page "New Quiz"
2. Entrer un nom de quiz
3. Cliquer **"Create"**
4. Le quiz apparaît dans la liste

### Scénario 5 : Faire un Quiz Seul
1. Cliquer **"Play"** à côté d'un quiz
2. Sélectionner les réponses
3. Cliquer **"Next"** entre les questions
4. Voir le score final

---

## 📱 Test du QR Code

### Avec un Smartphone

1. **Sur l'ordinateur** :
   - Créer une session et afficher le QR code
   
2. **Sur le smartphone** :
   - Ouvrir l'appareil photo
   - Scanner le QR code
   - Cliquer sur le lien qui apparaît
   - Se connecter ou créer un compte
   - Faire le quiz sur le téléphone !

**Note** : Remplacer `localhost` par l'IP de votre ordinateur si nécessaire
- Exemple : `http://192.168.1.10:8080/quiz-session/ABC12345`

---

## 🔧 Résolution de Problèmes

### Le serveur ne démarre pas
- Vérifier que le port 8080 n'est pas utilisé
- Utiliser `start-app.bat` qui configure Java automatiquement

### Le QR code ne s'affiche pas
- Les dépendances ZXing seront téléchargées au premier build
- Relancer l'application après le premier build Maven

### La session n'est pas trouvée
- Vérifier que le code est correct (8 caractères)
- Les codes sont sensibles à la casse
- La session existe tant que le serveur tourne

### Le leaderboard est vide
- Les participants doivent avoir terminé leur quiz
- Cliquer sur "Refresh" pour actualiser

---

## 💡 Conseils

### Pour une Démo Réussie

1. **Préparer 2-3 navigateurs** à l'avance
2. **Créer les comptes** avant la démo
3. **Utiliser des noms différents** pour identifier les participants
4. **Faire des scores différents** pour voir le classement

### Pour le Développement

1. Consulter `IMPLEMENTATION_COMPLETE.md` pour la vue d'ensemble
2. Lire `QUIZ_SESSION_SHARING.md` pour les détails techniques
3. Voir `AUTHENTICATION_GUIDE.md` pour la sécurité
4. Le code est bien commenté et documenté

---

## 📊 Données de Test

### Compte Administrateur
- Email : `test@example.com`
- Mot de passe : `password123`

### Quiz Disponibles
Voir `quiz-questions.json` pour :
- General Knowledge Quiz
- Second Quiz (Physics)
- Painting Quiz
- Et plus...

### Créer des Comptes Rapidement
```
Alice : alice@test.com / alice123
Bob   : bob@test.com / bob123
Carol : carol@test.com / carol123
```

---

## 🎉 Amusez-vous !

Vous êtes maintenant prêt à tester toutes les fonctionnalités !

**Principales routes** :
- `/` - Liste des quiz
- `/login` - Connexion
- `/register` - Inscription
- `/users` - Gestion utilisateurs
- `/join-session` - Rejoindre une session
- `/quiz-session/:code` - Salle de session

**Bon quiz ! 🚀**

