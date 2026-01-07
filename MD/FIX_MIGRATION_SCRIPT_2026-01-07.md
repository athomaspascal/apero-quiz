# Fix du Script de Migration SQL - 2026-01-07

## 🐛 Problème rencontré

Le script `apply-duel-migration.bat` produisait deux erreurs :

### Erreur 1 : Nom de table incorrect
```
Cannot resolve table 'user_table'
```

**Cause** : Le script référençait `user_table`, mais la vraie table s'appelle `users`.

### Erreur 2 : Nom de colonne ID incorrect
```
Column "ID" not found
```

**Cause** : Le script référençait la colonne `id`, mais la vraie colonne s'appelle `user_id`.

## ✅ Corrections appliquées

### 1. Script SQL corrigé

**Fichier** : `SQL/add_cancelled_by_to_duel_match.sql`

**AVANT** (incorrect) :
```sql
ALTER TABLE duel_match 
ADD CONSTRAINT IF NOT EXISTS fk_duel_match_cancelled_by 
FOREIGN KEY (cancelled_by_user_id) REFERENCES user_table(id);
                                               ^^^^^^^^^^  ^^
                                               Mauvais nom table et colonne
```

**APRÈS** (correct) :
```sql
ALTER TABLE duel_match 
ADD CONSTRAINT IF NOT EXISTS fk_duel_match_cancelled_by 
FOREIGN KEY (cancelled_by_user_id) REFERENCES users(user_id);
                                               ^^^^^  ^^^^^^^
                                               Bon nom table et colonne
```

### 2. Script batch automatique créé

**Fichier** : `apply-duel-migration-auto.bat`

Nouveau script sans `pause` pour une exécution automatique :
- ✅ Pas de confirmation manuelle requise
- ✅ Code de sortie approprié pour l'automatisation
- ✅ Messages d'erreur clairs

## 🎯 Résultat

```
================================================
Migration appliquee avec succes !
================================================

Vous pouvez maintenant demarrer l'application.
```

### Structure de la table après migration

```sql
duel_match
├── duel_id (PRIMARY KEY)
├── player1_id (FOREIGN KEY → users.user_id)
├── player2_id (FOREIGN KEY → users.user_id)
├── cancelled_by_user_id (FOREIGN KEY → users.user_id) ← NOUVEAU
├── quiz_id
├── status
├── player1_score
├── player2_score
├── ...
```

## 📋 Vérification de la structure

Pour vérifier les noms exacts des tables et colonnes :

### Table users
```java
@Entity
@Table(name = "users")  // ← Nom de la table
public class User {
    @Id
    @Column(name = "user_id")  // ← Nom de la colonne ID
    private Long id;
    ...
}
```

### Table duel_match
```java
@Entity
@Table(name = "duel_match")
public class DuelMatch {
    @ManyToOne
    @JoinColumn(name = "cancelled_by_user_id")  // ← Nouvelle colonne
    private User cancelledBy;
}
```

## 🧪 Test de la migration

La migration a été testée et fonctionne correctement :

```bash
cd C:\Users\athom\IdeaProjects\quizz1
apply-duel-migration-auto.bat
```

**Résultat** : ✅ SUCCESS

## 📝 Scripts disponibles

1. **apply-duel-migration.bat** : Version interactive (avec pause pour confirmation)
2. **apply-duel-migration-auto.bat** : Version automatique (sans pause) ← Recommandé

## 🚀 Prochaines étapes

Maintenant que la migration est appliquée, vous pouvez :

1. **Démarrer l'application** :
   ```bash
   rebuild-and-run-duel-fix.bat
   ```

2. **Tester la fonctionnalité** :
   - Démarrer un duel avec 2 joueurs
   - Un joueur quitte le duel
   - Vérifier que l'autre joueur reçoit la notification

---

**Date** : 2026-01-07  
**Status** : ✅ **CORRIGÉ ET TESTÉ**  
**Migration** : ✅ **APPLIQUÉE AVEC SUCCÈS**

