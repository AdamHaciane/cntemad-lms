# CNTEMAD LMS

## Stack
- Backend: Frappe Framework 15+
- Frontend: Vue 3 + Frappe UI + TailwindCSS
- DB: MariaDB
- Cache: Redis

## RÈGLE PRIORITAIRE
**TOUJOURS utiliser Frappe UI pour le frontend.**
- Ne jamais créer de composants custom si Frappe UI en propose un
- Composants dispo: Button, Input, Select, Card, Dialog, Table, Badge, Avatar, etc.
- Consulter https://ui.frappe.io/ avant de coder un composant
- Pattern data: utiliser `$resources` pour les appels API

## Si Frappe UI ne suffit pas
Frappe UI = Vue 3 + Tailwind, donc on peut :

1. **Créer composants Vue custom** dans `frontend/src/components/custom/`
2. **Utiliser bibliothèques Vue tierces** :
   - Charts: Chart.js, ApexCharts
   - Maps: Leaflet
   - Tables avancées: TanStack Table
   - Drag & Drop: VueDraggable
3. **Étendre avec Tailwind** : classes custom dans `tailwind.config.js`
4. **Headless UI** : composants accessibles sans style (même base que Frappe UI)

Règle : Toujours wrapper les composants tiers dans un composant custom CNTEMAD
pour maintenir la cohérence et faciliter les futures migrations.

## Structure
- `cntemad_lms/doctype/` → Modèles de données
- `cntemad_lms/api/` → Endpoints whitelist
- `cntemad_lms/overrides/` → Extensions LMS core
- `frontend/src/` → Composants Vue/Frappe UI
- `docs/INDEX.md` → Index détaillé du projet

## Commandes
- Tests: `bench run-tests --app cntemad_lms`
- Build: `bench build --app cntemad_lms`
- Lint: `pre-commit run --all-files`

## Conventions
- Doctype naming: `CNTEMAD {Name}`
- API prefix: `cntemad_lms.api.`
- Commits: Conventional Commits (feat/fix/docs)

## Avant de modifier
1. Lire `docs/INDEX.md` pour localiser le code
2. Vérifier les overrides existants dans `overrides/`
3. Tester localement avant PR

## Workflow Story

### Avant de coder
1. Lire `.claude/memory/CURRENT_SPRINT.md`
2. Lire la Story assignée dans `.claude/memory/stories/`
3. Confirmer la compréhension des critères d'acceptation

### Pendant le code
- Référencer la Story dans les commits: `feat(STORY-001): description`
- Mettre à jour les critères cochés au fur et à mesure

### Avant de terminer (OBLIGATOIRE)
1. Relire TOUS les critères d'acceptation
2. Vérifier chaque critère un par un:
   - Exécuter le test correspondant
   - Vérifier le comportement attendu
3. Si un critère échoue → corriger avant de continuer
4. Seulement quand TOUS les critères sont ✓ → marquer terminé

### Template de validation finale
Avant de dire "terminé", répondre à:
- [ ] Tous les critères d'acceptation sont cochés ?
- [ ] Les tests passent (`bench run-tests`) ?
- [ ] Le build passe (`bench build`) ?
- [ ] Les fichiers impactés sont tous modifiés ?
- [ ] La documentation est à jour si nécessaire ?

## Commandes mémoire
- "nouvelle story" → Créer story depuis template
- "status sprint" → Lire CURRENT_SPRINT.md et résumer
- "valider story X" → Exécuter boucle de validation complète
- "archiver story X" → Déplacer vers DONE.md si validée

## Documentation

### Quand documenter ?
- Nouveau endpoint API → Ajouter dans api-reference/
- Nouveau composant Vue → Docstring dans le fichier
- Nouvelle feature visible → Guide utilisateur
- Bug fixé fréquent → Ajouter à la FAQ

### Checklist documentation (Story)
- [ ] Docstrings ajoutés (Python/Vue)
- [ ] INDEX.md mis à jour
- [ ] Guide utilisateur si feature visible
- [ ] FAQ mise à jour si pertinent

## Amélioration continue

Quand tu travailles sur une fonctionnalité, consulte la section
"Idées d'amélioration" du MASTER_SPEC.md et propose des améliorations
qui respectent les 7 principes de design :

1. Mobile-first
2. Onboarding éclair
3. Validation progressive
4. Admin simple & complet
5. UX pensée par rôle
6. Tout connecté
7. Pur & direct

Toute proposition doit :
- Citer le principe respecté
- Être réalisable avec Frappe UI
- Ne pas complexifier l'existant
