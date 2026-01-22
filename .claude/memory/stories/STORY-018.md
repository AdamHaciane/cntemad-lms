# STORY-018: Composant StatsCard

## Epic parent
EPIC-004: Admin Centre Régional

## Description
En tant qu'admin, je veux voir mes KPIs dans des cartes visuelles claires.

## Critères d'acceptation spécifiques
- [ ] Affiche: icône, label, valeur, variation
- [ ] Couleur variation: vert (+), rouge (-)
- [ ] Tailles: sm, md, lg
- [ ] Props: icon, label, value, change, size
- [ ] Lien cliquable optionnel

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (valeur 0, pas de variation)
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé (Card, Badge)
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
- `frontend/src/components/custom/StatsCard.vue`
- `docs/INDEX.md`

## Commandes de validation
```bash
npm run build --prefix frontend
pre-commit run --all-files
```
