# Index CNTEMAD LMS

> Ce fichier sert de référence rapide pour Claude Code.
> Mis à jour à chaque nouvelle fonctionnalité.

## Doctypes

| Doctype | Fichier | Description |
|---------|---------|-------------|
| CNTEMAD Student | `cntemad_lms/doctype/cntemad_student/` | Profil étudiant (centre, année, progression) |
| CNTEMAD Course | `cntemad_lms/doctype/cntemad_course/` | Cours avec liste d'EC |
| CNTEMAD EC | `cntemad_lms/doctype/cntemad_ec/` | Élément Constitutif (unité d'enseignement) |
| CNTEMAD Payment | `cntemad_lms/doctype/cntemad_payment/` | Paiements mobile money |
| CNTEMAD Center | `cntemad_lms/doctype/cntemad_center/` | Centre régional (34 total) |
| CNTEMAD Enrollment | `cntemad_lms/doctype/cntemad_enrollment/` | Inscription étudiant à un cours/EC |

## API Endpoints

| Endpoint | Fichier:ligne | Description |
|----------|---------------|-------------|
| `get_student_progress` | `api/student.py:15` | Progression étudiant (EC validés) |
| `get_student_dashboard` | `api/student.py:45` | Données dashboard étudiant |
| `process_payment` | `api/payment.py:20` | Initier paiement mobile money |
| `payment_callback` | `api/payment.py:60` | Webhook callback paiement |
| `get_courses` | `api/course.py:10` | Liste cours disponibles |
| `get_course_content` | `api/course.py:35` | Contenu d'un cours |
| `get_center_stats` | `api/center.py:10` | Stats centre régional |

## Composants Vue

| Composant | Fichier | Frappe UI utilisé |
|-----------|---------|-------------------|
| CourseCard | `frontend/src/components/CourseCard.vue` | Card, Badge, Avatar |
| StudentDashboard | `frontend/src/pages/Dashboard.vue` | Table, Button, Dialog |
| PaymentForm | `frontend/src/components/PaymentForm.vue` | Form, Input, Select, Button |
| ProgressBar | `frontend/src/components/ProgressBar.vue` | Badge |
| ECList | `frontend/src/components/ECList.vue` | Table, Checkbox |

## Overrides LMS

| Original | Override | Raison |
|----------|----------|--------|
| (À définir) | `overrides/` | Extensions futures du LMS core |

## Hooks actifs

Définis dans `cntemad_lms/hooks.py`:
- `doc_events` → Notifications, validations
- `scheduler_events` → Tâches périodiques

## Intégrations paiement

| Provider | Module | Sandbox URL |
|----------|--------|-------------|
| MVola | `api/payment.py` | À configurer |
| Orange Money | `api/payment.py` | À configurer |
| Airtel Money | `api/payment.py` | À configurer |

## Points d'attention
- Ne jamais modifier `/apps/lms/` directement
- Tous les Custom Fields via fixtures
- Tests requis pour tout nouveau endpoint
- Mobile-first: tester sur 375px minimum
