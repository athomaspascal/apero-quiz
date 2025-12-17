# Guide d'Internationalisation (i18n) - Quizz1

## Vue d'ensemble

L'application Quizz1 prend maintenant en charge trois langues :
- 🇫🇷 Français
- 🇬🇧 Anglais
- 🇮🇹 Italien

## Comment ça marche

### 1. Boutons de Drapeaux dans le Menu Latéral

Dans le menu latéral (drawer), au-dessus de "Logged in as:", vous trouverez trois petits boutons avec des drapeaux emoji :
- 🇫🇷 Français
- 🇬🇧 English
- 🇮🇹 Italiano

Cliquez sur un drapeau pour changer la langue de l'application. La page se rechargera automatiquement avec la nouvelle langue.

### 2. Fichiers de Ressources

Les traductions sont stockées dans les fichiers suivants :
- `messages.properties` - Anglais (langue par défaut)
- `messages_fr.properties` - Français
- `messages_it.properties` - Italien

### 3. Structure des Clés de Traduction

Les clés sont organisées par fonctionnalité :

```properties
# Application
app.title=Quizz1
app.logout=Logout
app.loggedinas=Logged in as:

# Menu
menu.quizlist=Quiz List
menu.users=Users
menu.joinSession=Join Session

# Quiz List
quizlist.title=Quiz List
quizlist.start=Start
quizlist.share=Share

# Quiz Questions
quiz.next=Next
quiz.stop=Stop
quiz.finalscore=Final Score
quiz.correct=Correct!
quiz.incorrect=Incorrect!

# Etc...
```

### 4. Utilisation dans le Code

#### Service de Traduction

Le `TranslationService` fournit les méthodes suivantes :

```java
// Traduire avec la locale actuelle de l'UI
String text = translationService.translate("key");

// Traduire avec une locale spécifique
String text = translationService.translate("key", Locale.FRENCH);

// Changer la langue de l'application
translationService.setLocale(Locale.FRENCH);

// Obtenir la locale actuelle
Locale currentLocale = translationService.getCurrentLocale();
```

#### Exemple d'Utilisation dans une Vue

```java
@Route("example")
public class ExampleView extends VerticalLayout {
    
    private final TranslationService translationService;
    
    public ExampleView(TranslationService translationService) {
        this.translationService = translationService;
        
        // Utiliser les traductions
        Button button = new Button(translationService.translate("button.save"));
        H1 title = new H1(translationService.translate("view.title"));
        
        add(title, button);
    }
}
```

### 5. Ajouter de Nouvelles Traductions

Pour ajouter une nouvelle traduction :

1. Ajoutez la clé dans `messages.properties` (anglais)
2. Ajoutez la même clé avec la traduction française dans `messages_fr.properties`
3. Ajoutez la même clé avec la traduction italienne dans `messages_it.properties`

Exemple :
```properties
# messages.properties
button.submit=Submit

# messages_fr.properties
button.submit=Soumettre

# messages_it.properties
button.submit=Invia
```

### 6. Ajouter une Nouvelle Langue

Pour ajouter une nouvelle langue (par exemple, l'espagnol) :

1. Créez un nouveau fichier `messages_es.properties`
2. Copiez toutes les clés de `messages.properties`
3. Traduisez toutes les valeurs en espagnol
4. Ajoutez un bouton de drapeau dans `MainLayout.createLanguageButtons()` :

```java
// Spanish flag button
Button spanishButton = createFlagButton("🇪🇸", new Locale("es"));
layout.add(frenchButton, englishButton, italianButton, spanishButton);
```

### 7. Configuration Spring

La configuration de l'internationalisation est gérée par `InternationalizationConfig.java` :

- **LocaleResolver** : Utilise `SessionLocaleResolver` pour stocker la locale dans la session
- **MessageSource** : Configure `ResourceBundleMessageSource` pour charger les fichiers de traduction
- **Langue par défaut** : Anglais

### 8. État Actuel de la Traduction

#### ✅ Déjà traduit :
- MainLayout (menu latéral, logout)
- QuizListView (titre, boutons Start/Share)

#### ⏳ À traduire :
- QuizQuestionView
- QuizSessionView
- LoginView
- RegisterView
- ForgotPasswordView
- UserListView
- JoinSessionView

### 9. Prochaines Étapes

Pour compléter l'internationalisation, il faudra :

1. Ajouter le `TranslationService` à toutes les vues
2. Remplacer tous les textes en dur par des appels à `translationService.translate()`
3. Ajouter les clés manquantes dans les fichiers de traduction
4. Tester chaque vue dans les trois langues

### 10. Notes Importantes

- Le changement de langue recharge la page pour appliquer les traductions partout
- La locale est stockée dans la session et persiste pendant toute la session utilisateur
- Les fichiers de traduction utilisent l'encodage UTF-8
- Si une clé n'est pas trouvée, le système retourne la clé elle-même comme fallback

## Exemple Complet

Voici un exemple complet de vue multilingue :

```java
@Route("quiz-example")
@PageTitle("Quiz Example")
@Menu(title = "Quiz Example")
public class QuizExampleView extends VerticalLayout {
    
    private final TranslationService translationService;
    
    public QuizExampleView(TranslationService translationService) {
        this.translationService = translationService;
        
        // Titre traduit
        H1 title = new H1(translationService.translate("quiz.title"));
        
        // Boutons traduits
        Button startButton = new Button(
            translationService.translate("quiz.start"),
            event -> startQuiz()
        );
        
        Button stopButton = new Button(
            translationService.translate("quiz.stop"),
            event -> stopQuiz()
        );
        
        // Notification traduite
        Notification.show(
            translationService.translate("quiz.welcome"),
            3000,
            Notification.Position.MIDDLE
        );
        
        add(title, startButton, stopButton);
    }
    
    private void startQuiz() {
        Notification.show(translationService.translate("quiz.started"));
    }
    
    private void stopQuiz() {
        Notification.show(translationService.translate("quiz.stopped"));
    }
}
```

## Résumé

✅ **Complété** :
- Création des fichiers de traduction (FR, EN, IT)
- Service de traduction `TranslationService`
- Configuration Spring pour l'i18n
- Boutons de drapeaux dans le menu latéral
- Intégration dans MainLayout et QuizListView

🔄 **En cours** :
- Migration progressive des autres vues

📝 **À faire** :
- Traduire toutes les vues restantes
- Ajouter plus de traductions dans les fichiers properties
- Tester l'application dans les trois langues

L'infrastructure d'internationalisation est maintenant en place et fonctionnelle ! 🎉

