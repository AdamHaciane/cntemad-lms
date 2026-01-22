# STORY-007: Composant PaymentButton

## Epic parent
EPIC-002: Paiement Mobile Money

## Description
En tant qu'étudiant, je veux un bouton de paiement qui montre le montant et initie le processus.

## Critères d'acceptation spécifiques
- [ ] Affiche montant formaté (ex: "150 000 Ar")
- [ ] État loading pendant traitement
- [ ] État disabled si non prêt
- [ ] Props: amount, provider, loading, disabled
- [ ] Événement @pay

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (montant 0)
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé (Button)
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
- `frontend/src/components/custom/PaymentButton.vue`
- `docs/INDEX.md`

## Commandes de validation
```bash
npm run build --prefix frontend
pre-commit run --all-files
```
