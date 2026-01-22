# STORY-041: Alertes mentor

## Epic parent
EPIC-008: Mentor

## Description
En tant que mentor, je veux être alerté quand un mentoré est inactif.

## Critères d'acceptation spécifiques
- [ ] Alerte si inactif >7 jours
- [ ] Badge sur dashboard mentor
- [ ] Email quotidien récapitulatif (configurable)
- [ ] Action rapide: envoyer rappel
- [ ] Historique alertes

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés
- [ ] Happy path fonctionne

### Technique
- [ ] Scheduler Frappe pour vérification
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
- `cntemad_lms/api/mentor.py`
- `cntemad_lms/hooks.py`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module tasks
bench migrate
```
