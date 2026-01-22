# STORY-046: Notifications parent

## Epic parent
EPIC-009: Parent/Tuteur

## Description
En tant que parent, je veux recevoir des notifications sur l'activité de mes enfants.

## Critères d'acceptation spécifiques
- [ ] Notification email quand enfant valide EC
- [ ] SMS optionnel (configurable)
- [ ] Alerte si enfant inactif >7j
- [ ] Récapitulatif hebdomadaire (email)
- [ ] Centre de préférences notifications

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (email invalide)
- [ ] Happy path fonctionne

### Technique
- [ ] Scheduler Frappe
- [ ] Code propre, pas de debug
- [ ] Pas de credentials en dur

### Tests
- [ ] Tests unitaires écrits
- [ ] `bench run-tests` passe
- [ ] Test manuel OK
- [ ] Mobile responsive vérifié

### Intégration
- [ ] `bench build` passe
- [ ] `bench migrate` passe
- [ ] Pas de régression

### Documentation
- [ ] INDEX.md mis à jour

## Fichiers impactés
- `cntemad_lms/tasks.py`
- `cntemad_lms/api/notifications.py`
- `cntemad_lms/hooks.py`
- `frontend/src/pages/parent/NotificationSettings.vue`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.notifications
bench migrate
npm run build --prefix frontend
```
