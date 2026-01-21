# CNTEMAD LMS - Spécifications Master

## À propos du CNTEMAD
- **Nom complet**: Centre National de Télé-Enseignement de Madagascar
- **Création**: 1992 (décret n°92-953)
- **Statut**: Établissement public scientifique et culturel
- **Couverture**: 34 centres régionaux, ~50 branches
- **Étudiants**: ~17 000/an → objectif 49 000 d'ici 2029
- **Distinction**: Pionnier enseignement à distance en Afrique
- **Formations**: Informatique, Génie Industriel, Télécom, Droit, Économie, Commerce
- **Diplômes**: Licence (L3), Master (M2)

## Décisions techniques
- **Licence**: GPLv3
- **Paiements**: MVola + Orange Money + Airtel Money
- **Langues**: Français + Malgache + Anglais
- **Architecture**: Frappe LMS + extensions custom

## 7 Principes de design
1. **Mobile-first** → Conception mobile d'abord
2. **Onboarding éclair** → Inscription → cours en <5min
3. **Validation progressive** → Chaque EC validé = progression visible
4. **Admin simple & complet** → Moins de clics, plus d'automatisation
5. **UX pensée par rôle** → 1 interface = 1 utilisateur type
6. **Tout connecté** → Actions propagées partout
7. **Pur & direct** → Chaque écran a 1 objectif clair

## Concepts clés

| Terme | Définition |
|-------|-----------|
| **EC** | Élément Constitutif (unité d'enseignement) |
| **Centre régional** | Point physique CNTEMAD (34 total) |
| **Année universitaire** | Progression = somme EC validés |
| **Validation** | EC terminé + évaluation réussie |

## Parcours utilisateurs

### Étudiant
Inscription → Paiement → Choix EC → 1er cours → Progression

### Admin Centre Régional
Dashboard → Étudiants centre → Paiements → Rapports

### Enseignant
Mes cours → Créer contenu → Voir progression → Évaluations

### Admin Central
Vue nationale → 34 centres → Analytics → Config système

## Rôles & Permissions
- **Student**: Voir ses cours, payer, progression
- **Teacher**: Créer cours, voir étudiants de ses cours
- **Center Admin**: Gérer étudiants/paiements de son centre
- **National Admin**: Tout accès

## Contraintes techniques
- **Connectivité**: 3G/4G mobile majoritaire
- **Approche**: Mobile-first, optimisé data faible
- **Examens**: Hybride (QCM en ligne + final présentiel)

## Roadmap

### Phase 1: Foundation
- Setup organisation GitHub
- Structure repo avec CLAUDE.md
- CI/CD basique
- Documentation initiale

### Phase 2: Stabilisation
- Doctypes de base
- Tests automatisés
- Custom Fields CNTEMAD

### Phase 3: UX Frappe UI
- Refonte composants Vue
- Mobile responsive
- Thème CNTEMAD

### Phase 4: Features
- Paiements locaux
- Notifications push
- Analytics dashboard
