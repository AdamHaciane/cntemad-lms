# Créer un cours

Guide pour les enseignants souhaitant créer et publier des cours sur CNTEMAD LMS.

## Prérequis

- Compte enseignant validé par l'administration
- Accès au module de création de cours

## Structure d'un cours

Un cours CNTEMAD suit cette hiérarchie :

```
Cours
├── Informations générales
│   ├── Titre
│   ├── Description
│   ├── Filière
│   └── Niveau
├── EC 1 (Élément Constitutif)
│   ├── Leçon 1
│   ├── Leçon 2
│   └── Quiz EC
├── EC 2
│   └── ...
└── Examen final
```

## Créer un nouveau cours

### 1. Accéder à la création

1. Connectez-vous en tant qu'enseignant
2. Allez dans **Mes Cours** > **Créer un cours**
3. Remplissez les informations de base

### 2. Informations générales

| Champ | Description | Exemple |
|-------|-------------|---------|
| **Titre** | Nom du cours | "Introduction à Python" |
| **Code** | Identifiant unique | "INFO-L1-PY01" |
| **Description** | Résumé du cours | "Apprenez les bases..." |
| **Filière** | Département | Informatique |
| **Niveau** | L1, L2, L3, M1, M2 | L1 |
| **Image** | Vignette du cours | 800x450px recommandé |

### 3. Ajouter des EC

Cliquez sur **+ Ajouter un EC** pour chaque élément constitutif :

```
EC: Bases de Python
├── Objectifs: "À la fin de cet EC, l'étudiant saura..."
├── Durée estimée: 10 heures
├── Crédits: 3 ECTS
└── Ordre: 1
```

## Créer une leçon

### Types de contenu

#### Texte riche

L'éditeur supporte :
- **Gras**, *italique*, ~~barré~~
- Listes à puces et numérotées
- Tableaux
- Blocs de code avec coloration syntaxique
- Images et liens
- Formules mathématiques (LaTeX)

```python
# Exemple de code affiché dans une leçon
def bonjour():
    print("Bonjour, CNTEMAD!")
```

#### Vidéo

1. Cliquez sur **Ajouter une vidéo**
2. Uploadez votre fichier (MP4 recommandé)
3. Ou collez un lien YouTube/Vimeo

::: tip Conseil vidéo
- Durée optimale : 5-15 minutes par vidéo
- Qualité : 720p minimum
- Parlez clairement et à un rythme modéré
:::

#### Documents PDF

1. Cliquez sur **Ajouter un document**
2. Uploadez votre PDF
3. Ajoutez une description

#### Fichiers téléchargeables

Pour les exercices, datasets, etc. :
1. **Ajouter un fichier**
2. Uploadez (ZIP, PDF, XLSX, etc.)
3. Indiquez les instructions

## Créer un Quiz

### Configuration du quiz

| Paramètre | Description | Recommandation |
|-----------|-------------|----------------|
| **Durée** | Temps limite | 20-30 min par EC |
| **Tentatives** | Nombre d'essais | 2-3 |
| **Note de passage** | Minimum pour valider | 60% |
| **Ordre aléatoire** | Mélanger les questions | Oui |

### Types de questions

#### QCM (choix unique)

```
Question: Quelle est la capitale de Madagascar ?
○ Tananarive
○ Toamasina
○ Antananarivo ✓
○ Fianarantsoa

Feedback: Antananarivo, aussi appelée Tana, est la capitale.
```

#### QCM (choix multiples)

```
Question: Lesquels sont des langages de programmation ?
☑ Python
☑ Java
☐ HTML
☑ JavaScript

Note: HTML est un langage de balisage, pas de programmation.
```

#### Vrai/Faux

```
Question: Python est un langage compilé.
○ Vrai
○ Faux ✓

Feedback: Python est interprété, pas compilé.
```

### Bonnes pratiques quiz

1. **Clarté** : Une seule bonne réponse évidente par question
2. **Feedback** : Expliquez pourquoi la réponse est correcte/incorrecte
3. **Équilibre** : Mélangez questions faciles et difficiles
4. **Pertinence** : Liez les questions au contenu des leçons

## Publier le cours

### Vérification avant publication

- [ ] Tous les EC ont au moins une leçon
- [ ] Chaque EC a un quiz de validation
- [ ] Les vidéos sont accessibles
- [ ] Les documents s'ouvrent correctement
- [ ] L'ordre des leçons est logique

### États du cours

| État | Description |
|------|-------------|
| **Brouillon** | Visible uniquement par vous |
| **En révision** | Soumis pour validation admin |
| **Publié** | Visible par les étudiants inscrits |
| **Archivé** | Caché mais conservé |

### Soumettre pour publication

1. Cliquez sur **Soumettre pour révision**
2. L'administration vérifie le contenu
3. Vous recevez un email de validation ou de commentaires
4. Une fois approuvé, le cours passe en **Publié**

## Modifier un cours publié

::: warning Attention
Les modifications sur un cours publié affectent les étudiants en cours.
:::

- **Corrections mineures** : Appliquées immédiatement
- **Ajout de contenu** : OK, n'affecte pas la progression
- **Suppression de contenu** : Demandez l'approbation admin

---

Voir aussi : [Évaluations](/fr/enseignant/evaluations)
