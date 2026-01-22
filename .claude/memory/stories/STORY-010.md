# STORY-010: Webhook callback providers

## Epic parent
EPIC-002: Paiement Mobile Money

## Description
En tant que système, je veux recevoir les callbacks des providers pour confirmer les paiements.

## Critères d'acceptation spécifiques
- [ ] Endpoint: POST /api/method/cntemad_lms.api.payment.webhook_callback
- [ ] Supporte 3 formats: MVola, Orange Money, Airtel Money
- [ ] Valide signature/token du provider
- [ ] Met à jour CNTEMAD Payment (success/failed)
- [ ] Crée CNTEMAD Enrollment si success
- [ ] Envoie SMS confirmation à l'étudiant

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (callback dupliqué, transaction inconnue)
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé
- [ ] Code propre, pas de debug
- [ ] Pas de credentials en dur

### Tests
- [ ] Tests unitaires écrits
- [ ] `bench run-tests` passe
- [ ] Test manuel OK (simulation callback)
- [ ] Mobile responsive vérifié

### Intégration
- [ ] `bench build` passe
- [ ] `bench migrate` passe
- [ ] Pas de régression

### Documentation
- [ ] INDEX.md mis à jour

## Fichiers impactés
- `cntemad_lms/api/payment.py`
- `cntemad_lms/api/enrollment.py`
- `docs/api-reference/payment.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.payment
```
