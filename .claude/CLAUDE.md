# CNTEMAD LMS - Instructions Claude Code

## Contexte projet
- **Organisation**: Centre National de Télé-Enseignement de Madagascar
- **34 centres** régionaux, ~17 000 étudiants/an
- **Objectif**: 1ère université numérique de Madagascar

## Specs & Mémoire projet
- `memory/MASTER_SPEC.md` → Specs complètes du projet
- `memory/CURRENT_SPRINT.md` → Sprint en cours
- `memory/epics/` → Epics actifs
- `memory/stories/` → Stories détaillées
- `memory/DONE.md` → Archive terminée
- `memory/DECISIONS.md` → Décisions architecture

## Concepts clés

| Terme | Définition |
|-------|-----------|
| **EC** | Élément Constitutif (unité d'enseignement) |
| **Centre régional** | Point physique CNTEMAD (34 total) |
| **Année universitaire** | Progression = somme EC validés |
| **Validation** | EC terminé + évaluation réussie |

## Rôles utilisateurs
- **Student** → Étudiant inscrit
- **Teacher** → Enseignant/créateur de cours
- **Center Admin** → Administrateur centre régional
- **National Admin** → Administrateur central CNTEMAD

## Doctypes principaux
- `CNTEMAD Student` → Profil étudiant étendu
- `CNTEMAD Course` → Cours avec EC
- `CNTEMAD EC` → Élément constitutif
- `CNTEMAD Payment` → Paiements mobile money
- `CNTEMAD Center` → Centre régional
- `CNTEMAD Enrollment` → Inscription étudiant/cours

## Paiements supportés
- MVola (Telma)
- Orange Money
- Airtel Money

## Langues
- Français (défaut)
- Malgache
- Anglais

## Mobile-first breakpoints
- sm: 640px (mobile)
- md: 768px (tablette)
- lg: 1024px (desktop)

## Templates dans ce dossier
- `templates/epic.md` → Template Epic
- `templates/story.md` → Template Story
