# STORY-011: Page Paiement complète

## Epic parent
EPIC-002: Paiement Mobile Money

## Description
En tant qu'étudiant, je veux une page de paiement complète pour acheter un EC.

## Critères d'acceptation spécifiques
- [ ] Récapitulatif EC (titre, prix)
- [ ] Sélection provider (ProviderSelector)
- [ ] Saisie numéro téléphone avec validation
- [ ] Bouton payer (PaymentButton)
- [ ] Affichage statut temps réel
- [ ] Message succès/échec avec actions

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (annulation, timeout)
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé (Dialog, Input, Button)
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
- `frontend/src/pages/Payment.vue`
- `frontend/src/router.js`
- `docs/INDEX.md`

## Commandes de validation
```bash
npm run build --prefix frontend
pre-commit run --all-files
```
