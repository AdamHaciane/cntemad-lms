# EPIC-005: Enseignant & Création Contenu

## Contexte
L'enseignant crée et édite le contenu des EC.

## Stories
- [ ] STORY-024: Éditeur contenu (Markdown/WYSIWYG)
- [ ] STORY-025: Upload média (PDF, vidéo)
- [ ] STORY-026: Quiz Builder (questions QCM)
- [ ] STORY-027: Page "Mes Cours"
- [ ] STORY-028: Stats par EC (nb étudiants, taux réussite)

## Critères de succès Epic
- [ ] Enseignant crée EC complet sans code
- [ ] Preview contenu avant publication
- [ ] Stats visibles par EC

## Écrans concernés

| Écran | Composants | API |
|-------|-----------|-----|
| Dashboard | `StatsCards`, `RecentActivity`, `CourseList` | `get_instructor_stats()` |
| Mes Cours | `CourseCard`, `CreateButton` | `get_my_courses()` |
| Éditeur EC | `ContentEditor`, `QuizBuilder`, `MediaUpload` | `save_ec()` |
| Stats | `EnrollmentChart`, `ProgressTable`, `QuizResults` | `get_ec_stats()` |

## Dépendances
- Doctypes: CNTEMAD Course, CNTEMAD EC, LMS Quiz
- Rôle: Course Creator

## Notes techniques
- TipTap (Frappe UI) pour éditeur rich text
- Upload fichiers via Frappe Files
- Quiz Builder réutilise LMS Quiz
