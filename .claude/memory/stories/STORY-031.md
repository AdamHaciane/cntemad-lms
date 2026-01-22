# STORY-031: Comparaison centres

## Epic parent
EPIC-006: Admin National

## Description
En tant qu'admin national, je veux comparer les performances de plusieurs centres.

## Critères d'acceptation spécifiques
- [ ] Sélection multiple de centres
- [ ] Métriques: inscriptions, revenus, taux réussite
- [ ] Graphique barres comparatif
- [ ] Tableau détaillé
- [ ] Export comparaison

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (1 seul centre)
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
- `frontend/src/pages/admin/CenterCompare.vue`
- `frontend/src/router.js`
- `cntemad_lms/api/national.py`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.national
npm run build --prefix frontend
```
