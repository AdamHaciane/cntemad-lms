# STORY-008: Composable usePayment()

## Epic parent
EPIC-002: Paiement Mobile Money

## Description
En tant que développeur, je veux un composable pour gérer la logique de paiement mobile money.

## Critères d'acceptation spécifiques
- [ ] Expose: status, transactionId, error
- [ ] Méthodes: initiate(ec_id, provider, phone), checkStatus(transaction_id)
- [ ] États: idle → pending → processing → success/failed
- [ ] Polling automatique du statut
- [ ] Timeout après 5 minutes

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (timeout, annulation)
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé ($resources)
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
- `frontend/src/composables/usePayment.js`
- `cntemad_lms/api/payment.py`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.payment
npm run build --prefix frontend
```
