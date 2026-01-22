# STORY-009: API initiate_payment()

## Epic parent
EPIC-002: Paiement Mobile Money

## Description
En tant que système, je veux une API pour initier un paiement mobile money auprès du provider.

## Critères d'acceptation spécifiques
- [ ] Endpoint: POST /api/method/cntemad_lms.api.payment.initiate_payment
- [ ] Params: ec_id, provider (mvola/orange/airtel), phone_number
- [ ] Validation: EC existe, montant correct, téléphone valide
- [ ] Crée CNTEMAD Payment avec status="pending"
- [ ] Appelle API provider (sandbox pour tests)
- [ ] Retourne: transaction_id, status, provider_ref

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (EC déjà payé, provider down)
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé
- [ ] Code propre, pas de debug
- [ ] Pas de credentials en dur (utiliser site_config)

### Tests
- [ ] Tests unitaires écrits
- [ ] `bench run-tests` passe
- [ ] Test manuel OK (sandbox)
- [ ] Mobile responsive vérifié

### Intégration
- [ ] `bench build` passe
- [ ] `bench migrate` passe
- [ ] Pas de régression

### Documentation
- [ ] INDEX.md mis à jour

## Fichiers impactés
- `cntemad_lms/api/payment.py`
- `cntemad_lms/doctype/cntemad_payment/cntemad_payment.py`
- `docs/api-reference/payment.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.payment
bench migrate
```
