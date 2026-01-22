# STORY-040: Messagerie Mentor ↔ Étudiant

## Epic parent
EPIC-008: Mentor

## Description
En tant que mentor, je veux communiquer avec mes mentorés via messagerie.

## Critères d'acceptation spécifiques
- [ ] Liste conversations
- [ ] Thread messages par mentoré
- [ ] Envoi message texte
- [ ] Indicateur messages non lus
- [ ] Notification email à l'étudiant

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (message vide)
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
- `frontend/src/components/custom/ChatThread.vue`
- `frontend/src/pages/mentor/Messages.vue`
- `frontend/src/router.js`
- `cntemad_lms/api/messages.py`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.messages
npm run build --prefix frontend
```
