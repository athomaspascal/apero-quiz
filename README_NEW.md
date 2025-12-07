# 🎓 Quiz Application - Application Interactive de Quiz Multi-Utilisateurs

> Une application moderne de quiz collaborative avec authentification, partage de sessions et leaderboard en temps réel.

[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.5.8-brightgreen.svg)](https://spring.io/projects/spring-boot)
[![Vaadin](https://img.shields.io/badge/Vaadin-24.9.6-blue.svg)](https://vaadin.com/)
[![Java](https://img.shields.io/badge/Java-21-orange.svg)](https://www.oracle.com/java/)

---

## 🌟 Fonctionnalités Principales

### 🔐 Système d'Authentification Complet
- ✅ Connexion sécurisée avec BCrypt
- ✅ Inscription avec validation
- ✅ Récupération de mot de passe
- ✅ Gestion des utilisateurs (CRUD)
- ✅ Sessions sécurisées

### 🎮 Quiz Interactifs
- ✅ Questions à choix multiples
- ✅ Feedback immédiat sur les réponses
- ✅ Calcul automatique du score
- ✅ Interface intuitive et responsive
- ✅ Progression visuelle

### 👥 Sessions Partagées Multi-Utilisateurs
- ✅ **Partage via QR Code** pour rejoindre instantanément
- ✅ **Code de session unique** (8 caractères)
- ✅ **Participants illimités** par session
- ✅ **Leaderboard en temps réel** avec médailles 🏆
- ✅ **3 façons de rejoindre** : QR code, code manuel, ou lien direct
- ✅ **Persistance des sessions** en base de données

### 🏆 Leaderboard et Classement
- 🥇 Médaille d'or pour le 1er
- 🥈 Médaille d'argent pour le 2ème
- 🥉 Médaille de bronze pour le 3ème
- 📊 Affichage des scores en temps réel
- 🔄 Actualisation automatique

---

## 🚀 Démarrage Rapide

### Prérequis
- Java 21+ (configuré automatiquement avec `start-app.bat`)
- Maven (inclus via mvnw)

### Installation et Lancement

```bash
# Cloner le projet
git clone [votre-repo]
cd quizz1

# Lancer l'application (Windows)
start-app.bat

# Ou avec Maven directement
./mvnw spring-boot:run
```

### Accès à l'Application
```
URL: http://localhost:8080
Email: test@example.com
Mot de passe: password123
```

**📖 Voir [QUICK_START.md](QUICK_START.md) pour un guide détaillé**

---

## 📸 Captures d'Écran

### Page de Connexion
- Design moderne avec dégradé violet
- Formulaire intuitif
- Liens vers inscription et récupération de mot de passe

### Dialogue de Partage
```
┌──────────────────────────────┐
│ Share Quiz: General Knowledge│
├──────────────────────────────┤
│ Scan QR Code to Join         │
│                              │
│     [QR CODE IMAGE]          │
│                              │
│  Code: ABC12345              │
│                              │
│ [Go to Session] [Copy Link]  │
└──────────────────────────────┘
```

### Leaderboard
```
🏆 Final Leaderboard

🥇 Alice Smith    Score: 8/10
🥈 Bob Jones      Score: 7/10
🥉 Carol White    Score: 6/10
4  David Brown    Score: 5/10
```

---

## 🏗️ Architecture

### Technologies Utilisées

**Backend**
- Spring Boot 3.5.8
- Spring Data JPA
- Spring Security (crypto)
- H2 Database (en mémoire)

**Frontend**
- Vaadin 24.9.6
- Vaadin Flow
- Components Lumo

**Librairies**
- ZXing 3.5.3 (QR Codes)
- BCrypt (Sécurité)

### Structure du Projet

```
src/main/java/com/quizz/
├── base/
│   └── ui/              # Layout principal
├── examplefeature/
│   ├── *.java           # Entités (Quiz, User, QuizSession, etc.)
│   ├── ui/              # Vues Vaadin
│   ├── security/        # Authentication
│   └── util/            # Utilitaires (QR Code)
└── resources/
    ├── application.properties
    └── quiz-questions.json
```

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [QUICK_START.md](QUICK_START.md) | Guide de démarrage rapide en 3 minutes |
| [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md) | Vue d'ensemble complète du projet |
| [AUTHENTICATION_GUIDE.md](AUTHENTICATION_GUIDE.md) | Guide du système d'authentification |
| [QUIZ_SESSION_SHARING.md](QUIZ_SESSION_SHARING.md) | Documentation technique des sessions |
| [SESSION_SHARING_SUMMARY.md](SESSION_SHARING_SUMMARY.md) | Résumé de la fonctionnalité de partage |

---

## 🎯 Cas d'Usage

### 1. Quiz en Classe
Un professeur crée une session, les élèves scannent le QR code et participent en temps réel. Le leaderboard motive et rend l'apprentissage ludique.

### 2. Team Building
Organisez des quiz d'entreprise. Les équipes rejoignent avec leur smartphone et compétitionnent pour la première place.

### 3. Événements Sociaux
Créez des quiz pour vos soirées. Les invités scannent le code et jouent ensemble. Le leaderboard crée une ambiance festive.

### 4. Formation en Ligne
Évaluez les connaissances des apprenants en temps réel. Les résultats sont instantanés et le classement stimule la participation.

---

## 🔧 Configuration

### Modifier le Port
```properties
# application.properties
server.port=8080
```

### Changer l'URL de Base
```java
// QuizListView.java, ligne 119
String sessionUrl = "http://VOTRE-DOMAINE/quiz-session/" + session.getSessionCode();
```

### Ajouter des Quiz
Éditer `src/main/resources/quiz-questions.json`

---

## 🎓 Utilisation

### Créer une Session

1. Se connecter
2. Cliquer sur **"Share"** à côté d'un quiz
3. Partager le QR code ou le code de session
4. Aller dans la Session Room
5. Démarrer le quiz

### Rejoindre une Session

**3 Options** :
1. Scanner le QR code
2. Entrer le code dans "Join Session"
3. Cliquer sur le lien partagé

### Voir le Leaderboard

1. Terminer le quiz
2. Cliquer sur "View Leaderboard"
3. Voir le classement complet

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment participer :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---

## 📝 Licence

Ce projet est sous licence [LICENSE.md](LICENSE.md)

---

## 👥 Auteurs

- Développement initial : [Votre Nom]
- Contributions : Voir [CONTRIBUTORS.md](CONTRIBUTORS.md)

---

## 🙏 Remerciements

- Vaadin pour le framework UI exceptionnel
- Spring Boot pour la simplicité du backend
- ZXing pour la génération de QR codes
- La communauté open source

---

## 📞 Support

### En cas de problème

1. Consulter [QUICK_START.md](QUICK_START.md) pour le guide de dépannage
2. Vérifier les [Issues](../../issues) existantes
3. Créer une nouvelle issue si nécessaire

### Questions Fréquentes

**Q: Le QR code ne s'affiche pas ?**
R: Les dépendances ZXing seront téléchargées au premier build Maven.

**Q: Comment ajouter plus de questions ?**
R: Éditer `src/main/resources/quiz-questions.json`

**Q: Peut-on utiliser une vraie base de données ?**
R: Oui, remplacer H2 par PostgreSQL/MySQL dans `pom.xml` et `application.properties`

**Q: L'application est-elle sécurisée ?**
R: Oui, les mots de passe sont encodés avec BCrypt et les sessions sont gérées côté serveur.

---

## 🚀 Roadmap

### Fonctionnalités Futures Possibles

- [ ] WebSockets pour mise à jour en temps réel
- [ ] Minuteur pour les questions
- [ ] Mode multijoueur en temps réel
- [ ] Statistiques détaillées
- [ ] Export des résultats en PDF
- [ ] Support multilingue
- [ ] Thèmes personnalisables
- [ ] API REST pour intégration externe
- [ ] Application mobile native

---

## 📊 Statistiques

- **18 fichiers** créés
- **4 fichiers** modifiés
- **8 vues** Vaadin
- **6 entités** JPA
- **5 services** métier
- **100%** fonctionnel

---

## ⭐ Si vous aimez ce projet

N'hésitez pas à donner une ⭐ sur GitHub !

---

**Made with ❤️ and ☕ - Happy Quizzing! 🎉**

