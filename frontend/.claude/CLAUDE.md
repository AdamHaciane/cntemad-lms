# Frontend CNTEMAD

## Stack
Vue 3 + Frappe UI + TailwindCSS + Vite

## Composants Frappe UI utilisés
Button, Card, Dialog, Input, Select, Badge, Avatar, Table, Dropdown, Tooltip, Spinner, Alert, Breadcrumb, Form, Textarea, Checkbox, Popover

## Patterns
- Composables dans `src/composables/`
- API calls via `$resources` pattern Frappe UI
- Pas de store global (Frappe gère l'état)

## Structure
```
src/
├── components/
│   └── custom/         # Composants custom CNTEMAD
├── pages/              # Pages principales
├── composables/        # Logique réutilisable
└── main.js             # Point d'entrée
```

## Ressources pattern
```javascript
const { $resources } = useResource({
  resources: {
    courses: {
      method: 'cntemad_lms.api.get_courses',
      auto: true
    }
  }
})
// Accès: $resources.courses.data / .loading / .error
```

## Mobile-first
- Toujours coder mobile d'abord
- Ajouter les styles desktop avec préfixes md:, lg:
- Tester sur iPhone SE (375px) minimum

## Build
```bash
npm run dev    # Dev server
npm run build  # Production
npm run lint   # ESLint
```
