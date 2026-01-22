# STORY-030: Vue carte des 34 centres

## Epic parent
EPIC-006: Admin National

## Description
En tant qu'admin national, je veux voir une carte de Madagascar avec les 34 centres.

## Critères d'acceptation spécifiques
- [ ] Carte Madagascar avec marqueurs
- [ ] Couleur marqueur selon performance
- [ ] Popup avec infos centre au clic
- [ ] Zoom/pan fonctionnel
- [ ] Légende couleurs

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés
- [ ] Happy path fonctionne

### Technique
- [ ] Leaflet pour la carte
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
- `frontend/src/components/custom/CenterMap.vue`
- `frontend/src/pages/admin/NationalDashboard.vue`
- `docs/INDEX.md`

## Commandes de validation
```bash
npm run build --prefix frontend
pre-commit run --all-files
```
