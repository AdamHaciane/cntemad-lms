# STORY-019: Composant FilterBar

## Epic parent
EPIC-004: Admin Centre Régional

## Description
En tant qu'admin, je veux filtrer les données avec une barre de filtres réutilisable.

## Critères d'acceptation spécifiques
- [ ] Filtres configurables: select, date range, search
- [ ] Bouton reset tous filtres
- [ ] État persistant (URL params)
- [ ] Props: filters (config array)
- [ ] Événement @filter-change(filters)

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (aucun filtre)
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé (Select, Input)
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
- `frontend/src/components/custom/FilterBar.vue`
- `frontend/src/composables/useFilters.js`
- `docs/INDEX.md`

## Commandes de validation
```bash
npm run build --prefix frontend
pre-commit run --all-files
```
