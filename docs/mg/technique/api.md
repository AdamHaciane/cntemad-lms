# API Reference

Tahirin-kevitra momba ny endpoints API ny CNTEMAD LMS.

## Fanamarinana

### Mahazo token

```bash
POST /api/method/frappe.auth.get_logged_user
Content-Type: application/json

{
  "usr": "email@example.com",
  "pwd": "password"
}
```

Valiny:
```json
{
  "message": "email@example.com",
  "home_page": "/app",
  "full_name": "Anarana Feno"
}
```

### Headers ilaina

Ny fangatahana rehetra mila fanamarinana dia tsy maintsy misy:

```
Cookie: sid=<session_id>
X-Frappe-CSRF-Token: <csrf_token>
```

## Endpoints Mpianatra

### Mahazo profil mpianatra

```bash
GET /api/method/cntemad_lms.api.student.get_student_profile
```

Valiny:
```json
{
  "message": {
    "name": "STU-00001",
    "student_name": "Rakoto Jean",
    "email": "rakoto@email.com",
    "phone": "0341234567",
    "center": "Antananarivo",
    "program": "Informatika",
    "level": "L2",
    "enrollment_date": "2023-09-01"
  }
}
```

### Mahazo fandrosoana

```bash
GET /api/method/cntemad_lms.api.student.get_student_progress
```

Paramètres azo atao:
| Param | Karazana | Famaritana |
|-------|----------|------------|
| `student_id` | string | ID mpianatra (admin ihany) |

Valiny:
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
        "ec_name": "Python Mandroso",
        "status": "validated",
        "score": 85,
        "validated_date": "2024-01-15"
      }
    ]
  }
}
```

## Endpoints Lesona

### Lisitry ny lesona

```bash
GET /api/method/cntemad_lms.api.course.get_courses
```

Paramètres:
| Param | Karazana | Famaritana |
|-------|----------|------------|
| `program` | string | Sivana araka sampana |
| `level` | string | Sivana araka ambaratonga |
| `page` | int | Pejy (défaut: 1) |
| `limit` | int | Valiny/pejy (défaut: 20) |

### Votoatin'ny lesona

```bash
GET /api/method/cntemad_lms.api.course.get_course_content
```

Paramètres:
| Param | Karazana | Famaritana |
|-------|----------|------------|
| `course_id` | string | **Ilaina** - ID ny lesona |

### Marika fampianarana vita

```bash
POST /api/method/cntemad_lms.api.course.mark_lesson_complete
Content-Type: application/json

{
  "lesson_id": "LES-00001"
}
```

## Endpoints Fandoavana

### Manomboka fandoavana

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

Providers ekena: `mvola`, `orange_money`, `airtel_money`

Valiny:
```json
{
  "message": {
    "transaction_id": "TXN-20240120-00001",
    "status": "pending",
    "provider_ref": "MVL-ABC123",
    "amount": 150000,
    "message": "Azafady hamarino ny fandoavana amin'ny findainao"
  }
}
```

### Manamarina toetry ny fandoavana

```bash
GET /api/method/cntemad_lms.api.payment.get_payment_status
```

Paramètres:
| Param | Karazana | Famaritana |
|-------|----------|------------|
| `transaction_id` | string | **Ilaina** - ID transaction |

Valiny:
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

Status azo atao: `pending`, `processing`, `success`, `failed`, `refunded`

## Endpoints Admin

### Statistika foibe

```bash
GET /api/method/cntemad_lms.api.center.get_center_stats
```

Paramètres:
| Param | Karazana | Famaritana |
|-------|----------|------------|
| `center_id` | string | ID foibe (admin nasionaly) |
| `period` | string | `day`, `week`, `month`, `year` |

## Code d'erreur

| Code | Hafatra | Famaritana |
|------|---------|------------|
| 401 | `Not authenticated` | Session lany na tsy mety |
| 403 | `Permission denied` | Tsy ampy zo |
| 404 | `Not found` | Ressource tsy misy |
| 422 | `Validation error` | Data tsy mety |
| 429 | `Rate limited` | Be loatra ny fangatahana |
| 500 | `Server error` | Hadisoana anatiny |

## Rate Limiting

| Endpoint | Fetra |
|----------|-------|
| Fanamarinana | 5/min |
| Fandoavana | 10/min |
| Famakiana | 100/min |
| Fanoratana | 30/min |

---

Jereo koa: [Doctypes](/mg/technique/doctypes) | [Mandray anjara](/mg/technique/contributing)
