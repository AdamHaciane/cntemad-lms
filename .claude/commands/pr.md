# Créer une Pull Request

Crée une PR avec template, validation et référence story.

## Pré-requis

- Branche actuelle != `main` et != `develop`
- Tous les commits poussés
- `/validate` exécuté avec succès

## Étapes

1. **Vérifier la branche**
   ```bash
   git branch --show-current
   ```
   Ne pas être sur main/develop

2. **Exécuter /validate**
   Tous les checks doivent passer

3. **Vérifier Story (si applicable)**
   - Lire `.claude/memory/stories/STORY-XXX.md`
   - Tous les critères d'acceptation cochés?
   - Tests écrits?

4. **Pousser la branche**
   ```bash
   git push -u origin $(git branch --show-current)
   ```

5. **Créer la PR**
   ```bash
   gh pr create --title "type(scope): description" --body "$(cat <<'EOF'
   ## Summary
   - Point 1
   - Point 2
   - Point 3

   ## Story
   Closes #STORY-XXX (si applicable)

   ## Test Plan
   - [ ] Tests unitaires passent
   - [ ] Test manuel effectué
   - [ ] Mobile responsive vérifié

   ## Checklist
   - [ ] Code lint OK
   - [ ] Tests ajoutés/modifiés
   - [ ] Documentation mise à jour
   EOF
   )"
   ```

## Format titre PR

Même format que les commits:
```
type(scope): description courte
```

Exemples:
- `feat(payment): add MVola integration`
- `fix(student): correct progress calculation`
- `docs(api): add endpoint documentation`

## Template PR complet

```markdown
## Summary
<!-- 1-3 bullet points décrivant les changements -->

## Story
<!-- Lien vers la story si applicable -->
Closes #STORY-XXX

## Test Plan
- [ ] Tests unitaires passent (`bench run-tests`)
- [ ] Test manuel effectué
- [ ] Mobile responsive vérifié (375px, 768px, 1280px)
- [ ] Pas de régression

## Screenshots
<!-- Si changements UI, ajouter captures d'écran -->

## Checklist
- [ ] Lint passe (`pre-commit run --all-files`)
- [ ] Build réussit (`bench build`)
- [ ] Documentation mise à jour si nécessaire
- [ ] Critères d'acceptation Story tous validés
```

## Commande rapide

```bash
# PR simple
gh pr create --fill

# PR avec template complet
gh pr create --title "feat(scope): description" --body-file .github/PULL_REQUEST_TEMPLATE.md
```
