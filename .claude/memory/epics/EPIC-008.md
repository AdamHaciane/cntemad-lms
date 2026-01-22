# EPIC-008: Mentor

## Contexte
Accompagnement personnalisé des étudiants.

## Stories
- [ ] STORY-038: Page "Mes mentorés"
- [ ] STORY-039: Vue progression détaillée mentoré
- [ ] STORY-040: Messagerie Mentor ↔ Étudiant
- [ ] STORY-041: Alertes mentor (étudiant inactif)

## Critères de succès Epic
- [ ] Liste mentorés avec progression
- [ ] Chat intégré
- [ ] Notification si inactif 7j+

## Écrans concernés

| Écran | Composants | API |
|-------|-----------|-----|
| Mes étudiants | `MenteeList`, `ProgressOverview` | `get_my_mentees()` |
| Détail étudiant | `StudentProfile`, `ProgressTimeline`, `ECStatus` | `get_mentee_detail()` |
| Messages | `ChatList`, `MessageThread` | `get_messages()` |

## Dépendances
- Doctypes: LMS Course Mentor Mapping, LMS Mentor Request
- Rôle: Mentor

## Notes techniques
- Réutiliser Frappe LMS mentor system
- Messagerie simple (pas temps réel pour v1)
- Scheduler pour alertes inactivité
