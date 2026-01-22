# STORY-005: Page Catalogue EC

## Epic parent
EPIC-001: Dashboard Étudiant

## Description
En tant qu'étudiant, je veux parcourir tous les EC disponibles pour choisir ceux à acheter.

## Critères d'acceptation spécifiques
- [ ] Liste EC avec ECCard
- [ ] Filtres: année (L1-M2), cours, prix
- [ ] Recherche par titre/description
- [ ] Tri: prix, popularité, récent
- [ ] Pagination ou scroll infini

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (aucun résultat)
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé (Input, Select, Card)
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
- `frontend/src/pages/Catalog.vue`
- `frontend/src/router.js`
- `cntemad_lms/api/ec.py`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.ec
npm run build --prefix frontend
```
