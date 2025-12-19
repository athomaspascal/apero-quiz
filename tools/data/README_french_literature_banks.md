# French Literature banks (offline)

Ce fichier sert à rendre le quiz **French Literature** plus **véridique**.

## Où sont les données ?
- `tools/data/french_literature_banks.json`

## Schéma (résumé)

### authors[]
- `id`: identifiant stable (string)
- `name`: nom affiché
- `century_primary`: ex `"XVIIe"` (repère)
- `movements`: liste de mouvements (strings)
- `genres`: liste de genres (strings)
- `works`: liste d'IDs d'œuvres

### works[]
- `id`
- `title`
- `author_id`
- `genre`

### definitions[]
- `term`
- `definition`

## Comment augmenter la véracité ET atteindre 1000 questions ?

Actuellement, le pool factuel max est ~586 questions (avec les templates). Pour monter à 1000 sans inventer des réponses, il faut enrichir **surtout**:

1) `works` (le plus efficace)
- Ajouter beaucoup plus d'œuvres par auteur.

2) `definitions`
- Ajouter des termes (narratologie, versification, théâtre, argumentation...).

3) `authors`
- Ajouter plus d'auteurs + leurs œuvres (liens `author_id`).

Après enrichissement, relance le générateur.


