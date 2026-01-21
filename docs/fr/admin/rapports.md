# Rapports

Guide pour générer et analyser les rapports administratifs.

## Types de rapports

### Rapports académiques

| Rapport | Description | Fréquence |
|---------|-------------|-----------|
| **Progression étudiants** | EC validés par étudiant | Hebdomadaire |
| **Résultats examens** | Notes par session | Post-examen |
| **Taux de réussite** | % validation par cours/EC | Mensuel |
| **Abandons** | Étudiants inactifs | Mensuel |

### Rapports financiers

| Rapport | Description | Fréquence |
|---------|-------------|-----------|
| **Recettes** | Paiements par période | Quotidien |
| **Impayés** | Étudiants avec solde | Hebdomadaire |
| **Comparatif** | Évolution N vs N-1 | Mensuel |
| **Prévisions** | Estimations revenus | Trimestriel |

### Rapports opérationnels

| Rapport | Description | Fréquence |
|---------|-------------|-----------|
| **Activité plateforme** | Connexions, usage | Quotidien |
| **Performance cours** | Cours les plus/moins suivis | Mensuel |
| **Support** | Tickets, temps résolution | Hebdomadaire |

## Générer un rapport

### Accès

1. **Menu** > **Rapports**
2. Choisissez la catégorie
3. Sélectionnez le rapport

### Paramètres

Configurez avant génération :

| Paramètre | Options |
|-----------|---------|
| **Période** | Jour, semaine, mois, trimestre, année, personnalisé |
| **Centre** | Votre centre / Tous (admin national) |
| **Filière** | Toutes / Spécifique |
| **Niveau** | Tous / L1-M2 |
| **Format** | Écran, PDF, Excel, CSV |

### Exemple : Rapport mensuel étudiants

1. **Rapports** > **Académiques** > **Progression étudiants**
2. Période : Mois dernier
3. Centre : [Votre centre]
4. Format : PDF
5. **Générer**

## Rapports pré-configurés

### Tableau de bord mensuel

Rapport automatique envoyé le 1er de chaque mois :

```
RAPPORT MENSUEL - Centre [Nom]
Période : [Mois Année]

RÉSUMÉ
├── Étudiants actifs : 342 (+12)
├── Nouvelles inscriptions : 28
├── EC validés : 856
└── Revenus : 15,200,000 Ar

DÉTAIL PAR FILIÈRE
│ Filière      │ Étudiants │ Progression │ Revenus    │
│ Informatique │ 145       │ 72%         │ 6,500,000  │
│ Droit        │ 98        │ 68%         │ 4,200,000  │
│ Économie     │ 99        │ 71%         │ 4,500,000  │

POINTS D'ATTENTION
• 12 étudiants inactifs depuis >30 jours
• Taux d'échec EC "Mathématiques L1" : 35%
```

### Rapport d'activité quotidien

Email automatique chaque matin :

```
ACTIVITÉ - [Date]
• Connexions : 234
• Leçons terminées : 156
• Quiz passés : 45
• Paiements reçus : 8 (360,000 Ar)
• Nouveaux inscrits : 3
```

## Analyses avancées

### Cohortes

Suivez une promotion dans le temps :

1. **Rapports** > **Analyses** > **Cohortes**
2. Sélectionnez l'année d'entrée
3. Visualisez la rétention et progression

```
Cohorte 2023
├── Entrée L1 : 150 étudiants
├── L1 validée : 132 (88%)
├── L2 en cours : 125 (83%)
└── Abandons : 18 (12%)
```

### Comparatif centres (Admin national)

Comparez les performances des 34 centres :

| Centre | Étudiants | Progression | Revenus | Rang |
|--------|-----------|-------------|---------|------|
| Antananarivo | 2,450 | 75% | 110M | 1 |
| Toamasina | 890 | 72% | 40M | 2 |
| Mahajanga | 620 | 69% | 28M | 3 |
| ... | ... | ... | ... | ... |

### Tendances

Visualisez l'évolution sur plusieurs périodes :

```
Inscriptions mensuelles 2024
Jan ████████████████████ 156
Fév █████████████████████████ 198
Mar ██████████████████████████████ 234
Avr ████████████████████████ 189
Mai █████████████████████████████████ 267
```

## Export et partage

### Formats disponibles

| Format | Usage |
|--------|-------|
| **PDF** | Impression, archivage officiel |
| **Excel** | Analyse complémentaire, graphiques |
| **CSV** | Import dans autres systèmes |
| **JSON** | Intégration API |

### Planifier un envoi

Automatisez l'envoi de rapports :

1. Ouvrez le rapport
2. Cliquez sur **⏰ Planifier**
3. Configurez :
   - Fréquence : Quotidien, Hebdomadaire, Mensuel
   - Destinataires : Emails
   - Format : PDF, Excel
4. **Activer**

### Partager un lien

Pour partager un rapport sans l'envoyer :

1. Générez le rapport
2. Cliquez sur **🔗 Partager**
3. Configurez l'expiration (1j, 7j, 30j)
4. Copiez le lien sécurisé

## Tableaux de bord personnalisés

### Créer un tableau de bord

1. **Rapports** > **Mes tableaux de bord** > **Nouveau**
2. Glissez-déposez les widgets :
   - Graphiques
   - KPIs
   - Tableaux
   - Listes
3. Configurez chaque widget
4. Nommez et sauvegardez

### Widgets disponibles

| Widget | Description |
|--------|-------------|
| **Compteur** | Chiffre clé (étudiants, revenus...) |
| **Graphique ligne** | Évolution dans le temps |
| **Graphique barres** | Comparaison catégories |
| **Camembert** | Répartition |
| **Tableau** | Données détaillées |
| **Carte** | Répartition géographique |

### Exemple de tableau de bord personnalisé

```
┌─────────────────────────────────────────────────────────────┐
│  Mon Tableau de Bord - Suivi Hebdomadaire                   │
├──────────────────────┬──────────────────────────────────────┤
│  Étudiants actifs    │  Progression moyenne                 │
│      342             │  [===========     ] 68%              │
├──────────────────────┴──────────────────────────────────────┤
│  Inscriptions cette semaine                                 │
│  L  M  M  J  V  S  D                                        │
│  █  █  █  █  █  ░  ░                                        │
│  5  3  8  4  6  0  0                                        │
├─────────────────────────────────────────────────────────────┤
│  Top 5 cours les plus suivis                                │
│  1. Introduction Python (89 étudiants)                      │
│  2. Droit Civil L1 (76 étudiants)                          │
│  3. Comptabilité (72 étudiants)                            │
└─────────────────────────────────────────────────────────────┘
```

## Archivage

Les rapports sont conservés :
- **Rapports standards** : 2 ans
- **Rapports financiers** : 10 ans (légal)
- **Rapports personnalisés** : 1 an

Accédez aux archives via **Rapports** > **Archives**.

---

Voir aussi : [Dashboard](/fr/admin/dashboard)
