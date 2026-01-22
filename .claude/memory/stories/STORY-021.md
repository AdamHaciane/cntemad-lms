# STORY-021: Page Dashboard Centre

## Epic parent
EPIC-004: Admin Centre Régional

## Description
En tant qu'admin centre, je veux voir le tableau de bord de mon centre.

## Critères d'acceptation spécifiques
- [ ] KPIs: nb étudiants, nb paiements mois, montant total
- [ ] Graphique tendance inscriptions
- [ ] Liste alertes (paiements en attente)
- [ ] Actions rapides (ajouter étudiant, voir paiements)
- [ ] Données filtrées par centre automatiquement

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (nouveau centre vide)
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
- `frontend/src/pages/admin/CenterDashboard.vue`
- `frontend/src/router.js`
- `cntemad_lms/api/center.py`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.center
npm run build --prefix frontend
```
