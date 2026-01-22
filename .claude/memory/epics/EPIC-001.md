# EPIC-001: Dashboard Étudiant

## Contexte
L'étudiant doit voir sa progression, ses EC payés, et accéder rapidement au catalogue.

## Stories
- [ ] STORY-001: Composant ProgressBar
- [ ] STORY-002: Composant ECCard
- [ ] STORY-003: Composable useStudent()
- [ ] STORY-004: Page Dashboard étudiant
- [ ] STORY-005: Page Catalogue EC

## Critères de succès Epic
- [ ] Étudiant voit sa progression globale en %
- [ ] Liste des EC payés vs non payés visible
- [ ] Navigation vers catalogue en 1 clic

## Écrans concernés

| Écran | Composants | API |
|-------|-----------|-----|
| Dashboard | `ProgressCard`, `ECList`, `PaymentHistory` | `get_student_progress()` |
| Catalogue EC | `ECCard`, `FilterBar`, `SearchInput` | `get_available_ecs()` |
| Détail EC | `ECDetail`, `PaymentButton`, `ContentPreview` | `get_ec_detail()` |
| Progression | `YearProgress`, `ECStatusList`, `CertificateButton` | `get_yearly_progress()` |

## Dépendances
- Doctypes CNTEMAD Student, CNTEMAD EC

## Notes techniques
- Mobile-first design
- Frappe UI components (Card, Badge, Button)
- Composable useStudent() pour les données
