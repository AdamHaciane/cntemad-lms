# STORY-006: Composant ProviderSelector

## Epic parent
EPIC-002: Paiement Mobile Money

## Description
En tant qu'étudiant, je veux choisir mon opérateur mobile pour payer (MVola/Orange/Airtel).

## Critères d'acceptation spécifiques
- [ ] 3 options: MVola (Telma), Orange Money, Airtel Money
- [ ] Logo + nom de chaque provider
- [ ] Sélection visuelle claire (border/highlight)
- [ ] Props: selected, disabled
- [ ] Événement @select(provider)

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (provider indisponible)
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
- `frontend/src/components/custom/ProviderSelector.vue`
- `frontend/public/images/providers/` (logos)
- `docs/INDEX.md`

## Commandes de validation
```bash
npm run build --prefix frontend
pre-commit run --all-files
```
