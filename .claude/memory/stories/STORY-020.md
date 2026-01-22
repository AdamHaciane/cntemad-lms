# STORY-020: Composant ExportButton

## Epic parent
EPIC-004: Admin Centre Régional

## Description
En tant qu'admin, je veux exporter les données visibles en CSV ou PDF.

## Critères d'acceptation spécifiques
- [ ] Formats: CSV, PDF (optionnel: Excel)
- [ ] Dropdown pour choisir format
- [ ] État loading pendant génération
- [ ] Props: data, filename, formats
- [ ] Téléchargement automatique

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (données vides)
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé (Dropdown, Button)
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
- `frontend/src/components/custom/ExportButton.vue`
- `frontend/src/composables/useExport.js`
- `docs/INDEX.md`

## Commandes de validation
```bash
npm run build --prefix frontend
pre-commit run --all-files
```
