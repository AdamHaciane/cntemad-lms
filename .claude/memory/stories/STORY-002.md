# STORY-002: Composant ECCard

## Epic parent
EPIC-001: Dashboard Étudiant

## Description
En tant qu'étudiant, je veux voir une carte EC avec toutes les infos essentielles pour choisir quel EC suivre.

## Critères d'acceptation spécifiques
- [ ] Affiche: titre, description courte, prix, durée estimée
- [ ] Badge statut: payé/non payé/validé
- [ ] Image de couverture optionnelle
- [ ] Bouton action contextuel (Payer/Continuer/Voir)
- [ ] Props: ec (object), compact (boolean)
- [ ] Événement @click émis

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (données manquantes)
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé (Card, Badge, Button)
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
- `frontend/src/components/custom/ECCard.vue`
- `docs/INDEX.md`

## Commandes de validation
```bash
npm run build --prefix frontend
pre-commit run --all-files
```
