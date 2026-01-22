# EPIC-007: Évaluateur

## Contexte
Correction des examens présentiels et validation certificats.

## Stories
- [ ] STORY-033: Composant GradeInput
- [ ] STORY-034: Composant FeedbackEditor
- [ ] STORY-035: Page file d'attente corrections
- [ ] STORY-036: Page correction détail
- [ ] STORY-037: Validation certificats

## Critères de succès Epic
- [ ] Liste soumissions à corriger
- [ ] Saisie note + feedback
- [ ] Certificat validé après correction

## Écrans concernés

| Écran | Composants | API |
|-------|-----------|-----|
| Mes évaluations | `EvaluationList`, `FilterBar` | `get_my_evaluations()` |
| Correction | `SubmissionViewer`, `GradeInput`, `FeedbackEditor` | `submit_grade()` |
| Certificats | `CertificateQueue`, `ApproveButton` | `approve_certificate()` |

## Dépendances
- Doctypes: Course Evaluator, LMS Certificate
- Rôle: Batch Evaluator

## Notes techniques
- Réutiliser Frappe LMS evaluator system
- Notifications automatiques étudiant
- PDF certificat généré automatiquement
