# STORY-023: Page Paiements Centre

## Epic parent
EPIC-004: Admin Centre Régional

## Description
En tant qu'admin centre, je veux voir et gérer les paiements de mon centre.

## Critères d'acceptation spécifiques
- [ ] Table avec: étudiant, EC, montant, provider, statut, date
- [ ] Filtres: statut, provider, période
- [ ] Actions: voir détail, valider manuellement, rembourser
- [ ] Total paiements filtrés
- [ ] Export CSV

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (aucun paiement)
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé (Table)
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
- `frontend/src/pages/admin/CenterPayments.vue`
- `frontend/src/router.js`
- `cntemad_lms/api/center.py`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.center
npm run build --prefix frontend
```
