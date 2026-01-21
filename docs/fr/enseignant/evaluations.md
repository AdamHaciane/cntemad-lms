# Évaluations

Guide pour créer et gérer les évaluations de vos cours.

## Types d'évaluations

| Type | Description | Correction |
|------|-------------|------------|
| **Quiz EC** | QCM en fin d'EC | Automatique |
| **Devoir** | Travail à rendre | Manuelle |
| **Examen final** | En présentiel | Manuelle |

## Quiz automatiques

### Créer un quiz

1. Dans votre cours, accédez à l'EC concerné
2. Cliquez sur **Ajouter un quiz**
3. Configurez les paramètres
4. Ajoutez vos questions

### Banque de questions

Créez une banque de questions pour varier les quiz :

```
Banque "Python Bases" (20 questions)
├── Facile (8 questions) - Pondération 30%
├── Moyen (8 questions) - Pondération 50%
└── Difficile (4 questions) - Pondération 20%

Quiz généré : 10 questions aléatoires selon pondération
```

### Paramètres avancés

| Paramètre | Options | Recommandation |
|-----------|---------|----------------|
| **Mélange questions** | Oui/Non | Oui |
| **Mélange réponses** | Oui/Non | Oui |
| **Afficher score** | Immédiat/Différé | Immédiat |
| **Afficher corrections** | Oui/Non/Après deadline | Après deadline |
| **Pénalité tentative** | 0-50% | 10% par tentative |

## Devoirs

### Créer un devoir

1. Dans l'EC, cliquez sur **Ajouter un devoir**
2. Remplissez les informations :

| Champ | Description |
|-------|-------------|
| **Titre** | Nom du devoir |
| **Consignes** | Instructions détaillées |
| **Date limite** | Deadline de rendu |
| **Formats acceptés** | PDF, DOCX, ZIP, etc. |
| **Taille max** | En Mo |
| **Barème** | Points ou /20 |

### Exemple de consignes

```markdown
## Devoir : Projet Python

### Objectif
Créer un programme Python qui...

### Livrables
1. Code source (.py)
2. Rapport explicatif (PDF, 2-3 pages)
3. Captures d'écran du résultat

### Critères d'évaluation
- Fonctionnement du code : 10 pts
- Qualité du code : 5 pts
- Rapport : 5 pts

### Date limite
15 novembre 2024, 23h59 (heure Madagascar)
```

### Gestion des rendus

Accédez à **Mes Cours** > **[Cours]** > **Devoirs** > **Voir les rendus**

Tableau des rendus :
| Étudiant | Date rendu | Fichiers | Note | Statut |
|----------|------------|----------|------|--------|
| Rakoto J. | 14/11 18:30 | 2 fichiers | - | À corriger |
| Rasoa M. | 15/11 22:45 | 1 fichier | 15/20 | Corrigé |
| Rabe P. | - | - | - | Non rendu |

## Corriger les devoirs

### Interface de correction

1. Cliquez sur un rendu
2. Téléchargez/visualisez les fichiers
3. Utilisez la grille d'évaluation
4. Ajoutez des commentaires
5. Attribuez la note
6. **Publier la note**

### Grille d'évaluation

Créez une grille pour standardiser la correction :

```
Critère                  | Excellent | Bien | Moyen | Insuffisant
-------------------------|-----------|------|-------|------------
Code fonctionnel         | 10        | 7    | 4     | 0
Qualité du code          | 5         | 4    | 2     | 0
Documentation            | 5         | 4    | 2     | 0
```

### Commentaires constructifs

::: tip Bonnes pratiques
- Soyez spécifique : "La boucle ligne 15 pourrait être optimisée" plutôt que "Code à améliorer"
- Équilibrez positif et négatif
- Proposez des pistes d'amélioration
:::

## Suivi des résultats

### Tableau de bord évaluations

Accédez à **Mes Cours** > **Statistiques** pour voir :

- Moyenne de la classe par EC
- Distribution des notes
- Taux de réussite
- Étudiants en difficulté

### Exporter les notes

1. **Statistiques** > **Exporter**
2. Choisissez le format : Excel, CSV, PDF
3. Sélectionnez les colonnes à inclure
4. Téléchargez

### Identifier les difficultés

Le système signale automatiquement :
- Étudiants avec <50% de progression
- EC avec taux d'échec >30%
- Questions de quiz souvent ratées

## Examens finaux

### Préparation

Les examens finaux sont organisés par l'administration :

1. Soumettez vos sujets 3 semaines avant
2. Préparez le barème détaillé
3. Prévoyez une version de rattrapage

### Format du sujet

```
CNTEMAD - Examen [Filière] [Niveau]
Session : [Date]
Durée : [X] heures
Documents : [autorisés/non autorisés]

Partie 1 : QCM (30 points)
...

Partie 2 : Exercices (50 points)
...

Partie 3 : Problème (20 points)
...
```

### Correction des copies

1. Les copies scannées sont disponibles dans le système
2. Corrigez via l'interface en ligne
3. Ou téléchargez pour correction hors-ligne
4. Saisissez les notes dans le système
5. Les notes sont validées par l'administration

## Plagiat et fraude

### Détection automatique

Le système vérifie :
- Similarité entre copies
- Copie depuis internet (pour devoirs textuels)

### En cas de plagiat détecté

1. Vous recevez une alerte
2. Vérifiez manuellement
3. Signalez à l'administration si confirmé
4. L'administration prend les mesures disciplinaires

---

Voir aussi : [Créer un cours](/fr/enseignant/creer-cours)
