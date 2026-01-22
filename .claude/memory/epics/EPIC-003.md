# EPIC-003: Apprentissage & Quiz

## Contexte
L'étudiant accède au contenu d'un EC payé et passe le quiz de validation.

## Stories
- [ ] STORY-012: Composant LessonViewer (texte, PDF, vidéo)
- [ ] STORY-013: Composant QuizPlayer (QCM)
- [ ] STORY-014: Page détail EC
- [ ] STORY-015: Page Quiz
- [ ] STORY-016: API submit_quiz() + validation EC
- [ ] STORY-017: Logique progression (EC validé)

## Critères de succès Epic
- [ ] Contenu accessible après paiement
- [ ] Quiz auto-corrigé instantanément
- [ ] EC marqué "validé" si quiz réussi

## Écrans concernés

| Écran | Composants | API |
|-------|-----------|-----|
| Apprentissage | `LessonViewer`, `VideoPlayer`, `PDFViewer` | `get_ec_content()` |
| Quiz | `QuizPlayer`, `QuestionCard`, `ProgressBar` | `submit_quiz()` |

## Dépendances
- EPIC-002 (Paiement validé)
- Doctypes: CNTEMAD EC, LMS Quiz (Frappe LMS)

## Notes techniques
- Réutiliser Course Lesson de Frappe LMS
- QCM uniquement (auto-correction)
- Progression trackée dans CNTEMAD Enrollment
