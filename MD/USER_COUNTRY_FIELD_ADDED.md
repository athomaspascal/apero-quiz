# Ajout du champ Country à l'entité User

## Date
2026-01-02

## Description
Ajout d'une relation ManyToOne entre l'entité `User` et l'entité `Country` pour permettre aux utilisateurs de sélectionner leur pays d'origine.

## Modifications effectuées

### 1. Entity User.java
**Emplacement:** `src/main/java/com/quizz/core/entity/User.java`

#### Champ ajouté:
```java
@ManyToOne(fetch = FetchType.LAZY)
@JoinColumn(name = "country_id")
private Country country;
```

#### Méthodes ajoutées:
```java
public Country getCountry() {
    return country;
}

public void setCountry(Country country) {
    this.country = country;
}
```

### 2. Script SQL
**Emplacement:** `add_country_to_users.sql`

Le script SQL permet d'ajouter la colonne `country_id` à la table `users` avec :
- Une colonne `country_id` de type BIGINT (nullable)
- Une contrainte de clé étrangère vers `countries(country_id)`
- Un index pour améliorer les performances des requêtes

## Caractéristiques de la relation

### Type de relation
- **ManyToOne** : Plusieurs utilisateurs peuvent être associés au même pays
- **FetchType.LAZY** : Le pays n'est chargé que lorsqu'il est explicitement demandé (optimisation des performances)
- **Nullable** : Le champ country_id est optionnel, un utilisateur peut ne pas avoir de pays défini

### Clé étrangère
- **Colonne** : `country_id` dans la table `users`
- **Référence** : `country_id` dans la table `countries`
- **Contrainte** : `fk_users_country`

## Utilisation

### Dans le code Java

```java
// Créer un utilisateur avec un pays
User user = new User("John Doe", "john@example.com", "", "password");
Country france = countryService.findBySigle("FRA").orElse(null);
user.setCountry(france);
userService.save(user);

// Récupérer le pays d'un utilisateur
User user = userService.findById(userId);
Country userCountry = user.getCountry();
if (userCountry != null) {
    String countryName = userCountry.getCountryName();
    String flagSvg = userCountry.getCountryFlag();
}
```

### Dans les formulaires
Le champ pays pourra être ajouté aux formulaires :
- Formulaire d'inscription
- Formulaire de profil utilisateur
- Affichage du drapeau à côté du nom d'utilisateur

## Migration de données

### Pour les utilisateurs existants
Les utilisateurs existants auront `country_id = NULL` par défaut.

Options pour la migration :
1. Laisser le champ vide et demander aux utilisateurs de remplir leur profil
2. Définir un pays par défaut lors de la prochaine connexion
3. Utiliser la localisation IP pour suggérer un pays

## Avantages

1. **Statistiques** : Possibilité de générer des statistiques par pays
2. **Personnalisation** : Affichage du drapeau du pays de l'utilisateur
3. **Filtres** : Filtrer les utilisateurs par pays
4. **Classements** : Créer des classements par pays
5. **Quiz localisés** : Proposer des quiz adaptés au pays de l'utilisateur

## Prochaines étapes possibles

1. Ajouter un sélecteur de pays dans le formulaire d'inscription
2. Ajouter un sélecteur de pays dans le formulaire d'édition de profil
3. Afficher le drapeau du pays à côté du nom d'utilisateur dans les classements
4. Créer des statistiques par pays dans le tableau de bord admin
5. Implémenter la détection automatique du pays via l'adresse IP

## Configuration base de données

Si vous utilisez JPA avec `spring.jpa.hibernate.ddl-auto=update`, la colonne sera créée automatiquement au prochain démarrage.

Sinon, exécutez le script SQL `add_country_to_users.sql` manuellement :

```sql
psql -U username -d database_name -f add_country_to_users.sql
```

ou pour H2/autres bases de données, copiez-collez le contenu du script dans votre outil d'administration de base de données.

## Impact

### Sur les performances
- Impact minimal grâce au `FetchType.LAZY`
- Le pays n'est chargé que si explicitement demandé
- Index ajouté pour optimiser les requêtes de jointure

### Sur l'application existante
- **Aucun impact** sur le code existant
- Le champ est optionnel (nullable)
- Compatibilité totale avec les données existantes

### Sur la base de données
- Ajout d'une colonne : `country_id`
- Ajout d'une contrainte : `fk_users_country`
- Ajout d'un index : `idx_users_country_id`

## Tests recommandés

1. Créer un utilisateur sans pays → OK
2. Créer un utilisateur avec un pays → OK
3. Modifier le pays d'un utilisateur → OK
4. Supprimer le pays d'un utilisateur (set null) → OK
5. Charger un utilisateur et accéder à son pays → OK
6. Lister les utilisateurs d'un pays → OK

## Notes techniques

- La relation est unidirectionnelle (User → Country)
- Country n'a pas de collection d'utilisateurs (pas de bidirectionalité)
- Cela simplifie le code et améliore les performances
- Si besoin de la relation inverse, ajouter `@OneToMany` dans Country

