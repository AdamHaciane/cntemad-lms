# API Reference

Documentation des endpoints API du CNTEMAD LMS.

## Authentification

### Obtenir un token

```bash
POST /api/method/frappe.auth.get_logged_user
Content-Type: application/json

{
  "usr": "email@example.com",
  "pwd": "password"
}
```

Réponse :
```json
{
  "message": "email@example.com",
  "home_page": "/app",
  "full_name": "Nom Complet"
}
```

### Headers requis

Toutes les requêtes authentifiées doivent inclure :

```
Cookie: sid=<session_id>
X-Frappe-CSRF-Token: <csrf_token>
```

## Endpoints Étudiants

### Récupérer le profil étudiant

```bash
GET /api/method/cntemad_lms.api.student.get_student_profile
```

Réponse :
```json
{
  "message": {
    "name": "STU-00001",
    "student_name": "Rakoto Jean",
    "email": "rakoto@email.com",
    "phone": "0341234567",
    "center": "Antananarivo",
    "program": "Informatique",
    "level": "L2",
    "enrollment_date": "2023-09-01"
  }
}
```

### Récupérer la progression

```bash
GET /api/method/cntemad_lms.api.student.get_student_progress
```

Paramètres optionnels :
| Param | Type | Description |
|-------|------|-------------|
| `student_id` | string | ID étudiant (admin only) |

Réponse :
```json
{
  "message": {
    "total_ec": 12,
    "validated_ec": 8,
    "in_progress_ec": 2,
    "progress_percent": 66.7,
    "current_year": "L2",
    "ec_details": [
      {
        "ec_code": "INFO-L2-PY01",
        "ec_name": "Python Avancé",
        "status": "validated",
        "score": 85,
        "validated_date": "2024-01-15"
      }
    ]
  }
}
```

### Dashboard étudiant

```bash
GET /api/method/cntemad_lms.api.student.get_student_dashboard
```

Réponse :
```json
{
  "message": {
    "student": { /* profil */ },
    "progress": { /* progression */ },
    "recent_activity": [
      {
        "type": "lesson_completed",
        "course": "Python Avancé",
        "lesson": "Décorateurs",
        "date": "2024-01-20T14:30:00"
      }
    ],
    "upcoming": [
      {
        "type": "quiz_deadline",
        "ec": "Bases de données",
        "deadline": "2024-01-25T23:59:00"
      }
    ]
  }
}
```

## Endpoints Cours

### Liste des cours

```bash
GET /api/method/cntemad_lms.api.course.get_courses
```

Paramètres :
| Param | Type | Description |
|-------|------|-------------|
| `program` | string | Filtrer par filière |
| `level` | string | Filtrer par niveau |
| `page` | int | Page (défaut: 1) |
| `limit` | int | Résultats/page (défaut: 20) |

Réponse :
```json
{
  "message": {
    "courses": [
      {
        "name": "CRS-00001",
        "title": "Introduction à Python",
        "code": "INFO-L1-PY01",
        "program": "Informatique",
        "level": "L1",
        "ec_count": 5,
        "image": "/files/python-course.jpg"
      }
    ],
    "total": 45,
    "page": 1,
    "pages": 3
  }
}
```

### Contenu d'un cours

```bash
GET /api/method/cntemad_lms.api.course.get_course_content
```

Paramètres :
| Param | Type | Description |
|-------|------|-------------|
| `course_id` | string | **Requis** - ID du cours |

Réponse :
```json
{
  "message": {
    "course": {
      "name": "CRS-00001",
      "title": "Introduction à Python",
      "description": "Apprenez les bases...",
      "instructor": "Dr. Rabe"
    },
    "ecs": [
      {
        "name": "EC-00001",
        "title": "Variables et types",
        "order": 1,
        "lessons": [
          {
            "name": "LES-00001",
            "title": "Introduction",
            "type": "text",
            "duration_minutes": 15,
            "completed": true
          }
        ],
        "quiz": {
          "name": "QZ-00001",
          "question_count": 10,
          "duration_minutes": 20,
          "attempts_allowed": 3,
          "best_score": 85
        }
      }
    ]
  }
}
```

### Marquer une leçon terminée

```bash
POST /api/method/cntemad_lms.api.course.mark_lesson_complete
Content-Type: application/json

{
  "lesson_id": "LES-00001"
}
```

## Endpoints Paiements

### Initier un paiement

```bash
POST /api/method/cntemad_lms.api.payment.process_payment
Content-Type: application/json

{
  "provider": "mvola",
  "phone": "0341234567",
  "amount": 150000,
  "ec_ids": ["EC-00001", "EC-00002", "EC-00003"]
}
```

Providers supportés : `mvola`, `orange_money`, `airtel_money`

Réponse :
```json
{
  "message": {
    "transaction_id": "TXN-20240120-00001",
    "status": "pending",
    "provider_ref": "MVL-ABC123",
    "amount": 150000,
    "message": "Veuillez confirmer le paiement sur votre téléphone"
  }
}
```

### Vérifier le statut d'un paiement

```bash
GET /api/method/cntemad_lms.api.payment.get_payment_status
```

Paramètres :
| Param | Type | Description |
|-------|------|-------------|
| `transaction_id` | string | **Requis** - ID transaction |

Réponse :
```json
{
  "message": {
    "transaction_id": "TXN-20240120-00001",
    "status": "success",
    "confirmed_at": "2024-01-20T15:30:00",
    "receipt_url": "/files/receipts/TXN-20240120-00001.pdf"
  }
}
```

Statuts possibles : `pending`, `processing`, `success`, `failed`, `refunded`

### Callback webhook (interne)

```bash
POST /api/method/cntemad_lms.api.payment.payment_callback
```

Appelé par les providers de paiement pour confirmer les transactions.

## Endpoints Admin

### Statistiques centre

```bash
GET /api/method/cntemad_lms.api.center.get_center_stats
```

Paramètres :
| Param | Type | Description |
|-------|------|-------------|
| `center_id` | string | ID centre (admin national) |
| `period` | string | `day`, `week`, `month`, `year` |

Réponse :
```json
{
  "message": {
    "center": "Antananarivo",
    "period": "month",
    "stats": {
      "total_students": 2450,
      "active_students": 2180,
      "new_enrollments": 156,
      "total_revenue": 110000000,
      "average_progress": 72.5,
      "completion_rate": 68.3
    }
  }
}
```

### Liste des étudiants (admin)

```bash
GET /api/method/cntemad_lms.api.admin.get_students
```

Paramètres :
| Param | Type | Description |
|-------|------|-------------|
| `center` | string | Filtrer par centre |
| `program` | string | Filtrer par filière |
| `level` | string | Filtrer par niveau |
| `status` | string | `active`, `inactive`, `suspended` |
| `search` | string | Recherche nom/email |
| `page` | int | Page |
| `limit` | int | Résultats/page |

## Codes d'erreur

| Code | Message | Description |
|------|---------|-------------|
| 401 | `Not authenticated` | Session expirée ou invalide |
| 403 | `Permission denied` | Droits insuffisants |
| 404 | `Not found` | Ressource inexistante |
| 422 | `Validation error` | Données invalides |
| 429 | `Rate limited` | Trop de requêtes |
| 500 | `Server error` | Erreur interne |

Format erreur :
```json
{
  "exc_type": "ValidationError",
  "message": "Description de l'erreur",
  "data": {
    "field": "phone",
    "error": "Format invalide"
  }
}
```

## Rate Limiting

| Endpoint | Limite |
|----------|--------|
| Authentification | 5/min |
| Paiements | 10/min |
| Lecture | 100/min |
| Écriture | 30/min |

---

Voir aussi : [Doctypes](/fr/technique/doctypes) | [Contribuer](/fr/technique/contributing)
