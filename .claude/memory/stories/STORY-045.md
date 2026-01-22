# STORY-045: Paiement par parent

## Epic parent
EPIC-009: Parent/Tuteur

## Description
En tant que parent, je veux payer les EC pour mon enfant.

## Critères d'acceptation spécifiques
- [ ] Sélection enfant si plusieurs
- [ ] Liste EC non payés de l'enfant
- [ ] Processus paiement identique étudiant
- [ ] Reçu au nom du parent
- [ ] Notification à l'enfant après paiement

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (enfant a déjà payé)
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé
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
- `frontend/src/pages/parent/PayForChild.vue`
- `frontend/src/router.js`
- `cntemad_lms/api/guardian.py`
- `cntemad_lms/api/payment.py`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.guardian
npm run build --prefix frontend
```
