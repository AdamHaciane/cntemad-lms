# Doctypes

Architecture des modèles de données CNTEMAD LMS.

## Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────┐
│                     CNTEMAD Doctypes                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   CNTEMAD    │    │   CNTEMAD    │    │   CNTEMAD    │  │
│  │   Student    │───▶│  Enrollment  │◀───│    Course    │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                   │                   │           │
│         │                   │                   │           │
│         ▼                   ▼                   ▼           │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   CNTEMAD    │    │   CNTEMAD    │    │   CNTEMAD    │  │
│  │   Payment    │    │    Center    │    │      EC      │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## CNTEMAD Student

Profil étudiant étendu.

### Champs

| Champ | Type | Description |
|-------|------|-------------|
| `name` | Data | ID unique (auto: STU-XXXXX) |
| `student_name` | Data | Nom complet |
| `email` | Data | Email (unique) |
| `phone` | Data | Téléphone |
| `cin` | Data | Numéro CIN |
| `center` | Link → CNTEMAD Center | Centre régional |
| `program` | Select | Filière |
| `level` | Select | L1, L2, L3, M1, M2 |
| `enrollment_date` | Date | Date d'inscription |
| `status` | Select | active, inactive, suspended |
| `user` | Link → User | Compte Frappe associé |

### Exemple JSON

```json
{
  "doctype": "CNTEMAD Student",
  "name": "STU-00001",
  "student_name": "Rakoto Jean",
  "email": "rakoto@email.com",
  "phone": "0341234567",
  "cin": "101234567890",
  "center": "CTR-TANA",
  "program": "Informatique",
  "level": "L2",
  "enrollment_date": "2023-09-01",
  "status": "active",
  "user": "rakoto@email.com"
}
```

### Permissions

| Rôle | Lire | Écrire | Créer | Supprimer |
|------|------|--------|-------|-----------|
| Student | ✓ (self) | ✓ (limité) | ✗ | ✗ |
| Center Admin | ✓ (center) | ✓ | ✓ | ✗ |
| National Admin | ✓ | ✓ | ✓ | ✓ |

## CNTEMAD Course

Cours avec métadonnées.

### Champs

| Champ | Type | Description |
|-------|------|-------------|
| `name` | Data | ID unique (auto: CRS-XXXXX) |
| `title` | Data | Titre du cours |
| `code` | Data | Code unique (ex: INFO-L1-PY01) |
| `description` | Text | Description longue |
| `program` | Select | Filière |
| `level` | Select | Niveau requis |
| `instructor` | Link → User | Enseignant responsable |
| `image` | Attach Image | Vignette |
| `status` | Select | draft, review, published, archived |
| `ecs` | Table → CNTEMAD EC | Liste des EC |

### Exemple JSON

```json
{
  "doctype": "CNTEMAD Course",
  "name": "CRS-00001",
  "title": "Introduction à Python",
  "code": "INFO-L1-PY01",
  "description": "Apprenez les bases de la programmation...",
  "program": "Informatique",
  "level": "L1",
  "instructor": "dr.rabe@cntemad.mg",
  "status": "published",
  "ecs": [
    {"ec": "EC-00001"},
    {"ec": "EC-00002"}
  ]
}
```

## CNTEMAD EC

Élément Constitutif (unité d'enseignement).

### Champs

| Champ | Type | Description |
|-------|------|-------------|
| `name` | Data | ID unique (auto: EC-XXXXX) |
| `title` | Data | Titre de l'EC |
| `code` | Data | Code unique |
| `course` | Link → CNTEMAD Course | Cours parent |
| `order` | Int | Ordre d'affichage |
| `credits` | Int | Crédits ECTS |
| `duration_hours` | Int | Durée estimée |
| `fee` | Currency | Tarif |
| `passing_score` | Int | Note de passage (%) |

### États de validation

Un EC peut être dans l'état suivant pour un étudiant :
- `not_started` : Non commencé
- `in_progress` : En cours
- `completed` : Leçons terminées, quiz non passé
- `validated` : Quiz réussi
- `failed` : Quiz échoué (tentatives épuisées)

## CNTEMAD Payment

Transactions de paiement.

### Champs

| Champ | Type | Description |
|-------|------|-------------|
| `name` | Data | ID transaction |
| `student` | Link → CNTEMAD Student | Étudiant |
| `amount` | Currency | Montant |
| `provider` | Select | mvola, orange_money, airtel_money |
| `provider_ref` | Data | Référence provider |
| `phone` | Data | Téléphone utilisé |
| `status` | Select | pending, processing, success, failed, refunded |
| `ec_items` | Table | Liste des EC payés |
| `created_at` | Datetime | Date création |
| `confirmed_at` | Datetime | Date confirmation |

### Exemple JSON

```json
{
  "doctype": "CNTEMAD Payment",
  "name": "TXN-20240120-00001",
  "student": "STU-00001",
  "amount": 150000,
  "provider": "mvola",
  "provider_ref": "MVL-ABC123",
  "phone": "0341234567",
  "status": "success",
  "ec_items": [
    {"ec": "EC-00001", "amount": 50000},
    {"ec": "EC-00002", "amount": 50000},
    {"ec": "EC-00003", "amount": 50000}
  ],
  "created_at": "2024-01-20 14:30:00",
  "confirmed_at": "2024-01-20 14:32:15"
}
```

## CNTEMAD Center

Centres régionaux.

### Champs

| Champ | Type | Description |
|-------|------|-------------|
| `name` | Data | ID centre |
| `center_name` | Data | Nom complet |
| `region` | Data | Région Madagascar |
| `address` | Text | Adresse physique |
| `phone` | Data | Téléphone contact |
| `email` | Data | Email contact |
| `manager` | Link → User | Responsable |
| `is_active` | Check | Actif/Inactif |

### Liste des 34 centres

Les centres couvrent toutes les régions de Madagascar :
- Antananarivo (siège)
- Toamasina
- Mahajanga
- Fianarantsoa
- Antsiranana
- Toliara
- ... (28 autres)

## CNTEMAD Enrollment

Inscriptions étudiants aux cours/EC.

### Champs

| Champ | Type | Description |
|-------|------|-------------|
| `name` | Data | ID inscription |
| `student` | Link → CNTEMAD Student | Étudiant |
| `course` | Link → CNTEMAD Course | Cours |
| `ec` | Link → CNTEMAD EC | EC spécifique |
| `enrolled_date` | Date | Date inscription |
| `status` | Select | enrolled, in_progress, completed, dropped |
| `payment` | Link → CNTEMAD Payment | Paiement associé |
| `progress` | Percent | Progression (%) |
| `score` | Int | Note obtenue |
| `validated_date` | Date | Date validation |

## Relations

### Diagramme ER

```
CNTEMAD Student ─────┬────▶ CNTEMAD Enrollment ◀────┬───── CNTEMAD Course
       │             │              │               │            │
       │             │              │               │            │
       ▼             │              │               │            ▼
CNTEMAD Payment ─────┘              │               └───── CNTEMAD EC
       │                            │
       │                            │
       └────────────────────────────┘
                    │
                    ▼
            CNTEMAD Center
```

### Contraintes

1. Un étudiant appartient à un seul centre
2. Un cours peut avoir plusieurs EC
3. Un paiement peut couvrir plusieurs EC
4. Une inscription lie un étudiant à un EC spécifique

## Hooks et Events

### Document Events

```python
# cntemad_lms/hooks.py

doc_events = {
    "CNTEMAD Student": {
        "after_insert": "cntemad_lms.events.student.after_insert",
        "on_update": "cntemad_lms.events.student.on_update"
    },
    "CNTEMAD Payment": {
        "on_submit": "cntemad_lms.events.payment.on_submit"
    }
}
```

### Exemple : Après inscription

```python
# cntemad_lms/events/student.py

def after_insert(doc, method):
    # Envoyer email de bienvenue
    frappe.sendmail(
        recipients=[doc.email],
        subject="Bienvenue au CNTEMAD",
        template="welcome_student",
        args={"student_name": doc.student_name}
    )

    # Notifier le centre
    frappe.publish_realtime(
        "new_student",
        {"student": doc.name, "center": doc.center}
    )
```

---

Voir aussi : [API Reference](/fr/technique/api) | [Contribuer](/fr/technique/contributing)
