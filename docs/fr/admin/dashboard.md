# Dashboard Administrateur

Guide d'utilisation du tableau de bord pour les administrateurs de centres régionaux et nationaux.

## Accès au Dashboard

1. Connectez-vous avec vos identifiants administrateur
2. Le dashboard s'affiche automatiquement après connexion
3. Utilisez le menu latéral pour naviguer

## Vue d'ensemble

### Admin Centre Régional

```
┌─────────────────────────────────────────────────────────────┐
│  DASHBOARD - Centre [Nom du Centre]                         │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ Étudiants│ │ Paiements│ │ Inscrits │ │ Taux     │       │
│  │   342    │ │ 15.2M Ar │ │ ce mois  │ │ réussite │       │
│  │ actifs   │ │ ce mois  │ │   +28    │ │   78%    │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
├─────────────────────────────────────────────────────────────┤
│  Activité récente          │  Paiements en attente          │
│  • Rakoto J. inscrit (2h)  │  • Rasoa M. - 45,000 Ar        │
│  • Rabe P. a payé (3h)     │  • Randria K. - 30,000 Ar      │
│  • Quiz validé par 12 (4h) │  • Total: 3 en attente         │
└─────────────────────────────────────────────────────────────┘
```

### Admin National

Le dashboard national agrège les données des 34 centres :

| Widget | Description |
|--------|-------------|
| **Carte interactive** | Répartition des étudiants par centre |
| **KPIs nationaux** | Total étudiants, revenus, taux réussite |
| **Comparatif centres** | Classement des centres par performance |
| **Alertes** | Problèmes nécessitant attention |

## Widgets disponibles

### Statistiques étudiants

- **Total étudiants** : Actifs dans votre centre
- **Nouveaux ce mois** : Inscriptions récentes
- **Par filière** : Répartition Informatique, Droit, etc.
- **Par niveau** : L1, L2, L3, M1, M2

### Statistiques financières

- **Revenus du mois** : Total des paiements confirmés
- **Paiements en attente** : À valider manuellement si nécessaire
- **Comparaison N-1** : Évolution vs année précédente
- **Prévisions** : Estimation fin de mois

### Progression académique

- **Taux de réussite** : % d'EC validés / total
- **Étudiants en difficulté** : <50% progression
- **Top performers** : Meilleurs étudiants

## Gestion des étudiants

### Rechercher un étudiant

1. **Menu** > **Étudiants** > **Rechercher**
2. Recherchez par : Nom, email, numéro étudiant
3. Cliquez sur un résultat pour voir le profil

### Profil étudiant

Le profil affiche :
- Informations personnelles
- Historique des paiements
- Progression dans les cours
- EC validés / en cours

### Actions disponibles

| Action | Description |
|--------|-------------|
| **Modifier profil** | Corriger informations |
| **Réinitialiser mot de passe** | Envoyer un lien de reset |
| **Suspendre compte** | Bloquer temporairement |
| **Exporter données** | PDF du dossier étudiant |

### Inscription manuelle

Pour les cas spéciaux (problème technique, transfert...) :

1. **Étudiants** > **Nouvelle inscription**
2. Remplissez le formulaire
3. Cochez **Inscription manuelle - justification obligatoire**
4. Expliquez la raison
5. Validez

## Gestion des paiements

### Paiements automatiques

95% des paiements sont validés automatiquement. Vous voyez uniquement les cas particuliers.

### Paiements en attente

Cas nécessitant validation manuelle :
- Montant ne correspond pas exactement
- Doublons détectés
- Paiement partiel

#### Valider un paiement

1. **Paiements** > **En attente**
2. Cliquez sur le paiement
3. Vérifiez les informations (référence transaction)
4. **Valider** ou **Rejeter** avec motif

### Remboursements

1. Trouvez le paiement dans **Historique**
2. Cliquez sur **Demander remboursement**
3. Entrez le motif et le montant
4. La demande est envoyée à l'admin national

## Notifications et alertes

### Types d'alertes

| Priorité | Type | Exemple |
|----------|------|---------|
| 🔴 Haute | Paiement échoué en boucle | Étudiant bloqué |
| 🟠 Moyenne | Étudiants inactifs >30j | Relance nécessaire |
| 🟢 Basse | Nouveau rapport disponible | Information |

### Configurer les notifications

1. **Paramètres** > **Notifications**
2. Activez/désactivez par type
3. Choisissez : Email, Push, Tableau de bord
4. Sauvegardez

## Personnaliser le dashboard

### Ajouter/Supprimer des widgets

1. Cliquez sur **⚙️ Personnaliser** en haut à droite
2. Glissez-déposez les widgets
3. Redimensionnez si nécessaire
4. **Enregistrer la disposition**

### Widgets disponibles

- Statistiques étudiants
- Revenus
- Graphique inscriptions
- Calendrier examens
- Alertes récentes
- Top cours
- Étudiants en difficulté

## Raccourcis clavier

| Raccourci | Action |
|-----------|--------|
| `G + D` | Aller au Dashboard |
| `G + E` | Aller aux Étudiants |
| `G + P` | Aller aux Paiements |
| `G + R` | Aller aux Rapports |
| `/` | Recherche globale |

---

Voir aussi : [Rapports](/fr/admin/rapports)
