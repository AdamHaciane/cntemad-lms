# STORY-037: Validation certificats

## Epic parent
EPIC-007: Évaluateur

## Description
En tant qu'évaluateur, je veux approuver les certificats des étudiants éligibles.

## Critères d'acceptation spécifiques
- [ ] Liste étudiants éligibles (année complète validée)
- [ ] Détail progression par étudiant
- [ ] Boutons: Approuver, Rejeter avec motif
- [ ] Génération PDF certificat après approbation
- [ ] Notification étudiant

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés
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
- `frontend/src/pages/evaluator/Certificates.vue`
- `frontend/src/router.js`
- `cntemad_lms/api/certificate.py`
- `cntemad_lms/templates/certificate.html`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.certificate
npm run build --prefix frontend
```
