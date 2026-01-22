# Workflow Story

Gère le cycle de vie d'une story: start → validate → complete.

## Commandes

### `/story start STORY-XXX`

Démarre le travail sur une story.

1. Lire la story
   ```
   Lire .claude/memory/stories/STORY-XXX.md
   ```

2. Créer branche
   ```bash
   git checkout -b feature/STORY-XXX
   ```

3. Mettre à jour CURRENT_SPRINT.md
   - Marquer la story "in_progress"

4. Afficher les critères d'acceptation pour référence

### `/story validate STORY-XXX`

Valide tous les critères d'une story.

1. Lire la story et ses critères

2. Vérifier chaque critère:

   **Fonctionnel**
   - [ ] Comportement attendu implémenté
   - [ ] Cas limites gérés
   - [ ] Happy path fonctionne

   **Technique**
   - [ ] Frappe UI utilisé
   - [ ] Code propre, pas de debug
   - [ ] Pas de credentials en dur

   **Tests**
   - [ ] Tests unitaires écrits
   - [ ] `bench run-tests` passe
   - [ ] Test manuel OK
   - [ ] Mobile responsive vérifié

   **Intégration**
   - [ ] `bench build` passe
   - [ ] `bench migrate` passe
   - [ ] Pas de régression

   **Documentation**
   - [ ] INDEX.md mis à jour si nouveau fichier

3. Exécuter les commandes de validation
   ```bash
   pre-commit run --all-files
   bench --site lms.local run-tests --app cntemad_lms
   bench build --app cntemad_lms
   bench --site lms.local migrate --dry-run
   ```

4. Reporter le résultat

### `/story complete STORY-XXX`

Termine une story validée.

1. Vérifier que `/story validate` a passé

2. Mettre à jour la story
   - Cocher tous les critères
   - Ajouter date de completion

3. Mettre à jour CURRENT_SPRINT.md
   - Marquer la story "completed"

4. Mettre à jour DONE.md
   - Ajouter la story à l'archive

5. Commit final si nécessaire
   ```bash
   git add .claude/memory/
   git commit -m "chore: complete STORY-XXX"
   ```

## Templates

### Story status dans CURRENT_SPRINT.md

```markdown
| Story | Assigné | Status | Progress |
|-------|---------|--------|----------|
| STORY-001 | Claude | completed | 5/5 critères |
| STORY-002 | Claude | in_progress | 3/5 critères |
| STORY-003 | - | pending | 0/5 critères |
```

### Entrée dans DONE.md

```markdown
## STORY-XXX: Titre
- **Date**: 2024-XX-XX
- **Epic**: EPIC-XXX
- **Durée**: X sessions
- **Commits**: feat(scope): ..., fix(scope): ...
```

## Checklist story

```markdown
## Avant de marquer terminé

- [ ] TOUS les critères d'acceptation cochés
- [ ] Tests passent
- [ ] Build passe
- [ ] Code reviewé (si PR)
- [ ] Documentation à jour
- [ ] CURRENT_SPRINT.md mis à jour
- [ ] DONE.md mis à jour
```

## Règle d'or

> **JAMAIS marquer une Story terminée si un seul critère n'est pas validé.**
