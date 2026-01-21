# Doctypes

Firafitry ny modèles de données CNTEMAD LMS.

## Topimaso

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
│         ▼                   ▼                   ▼           │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   CNTEMAD    │    │   CNTEMAD    │    │   CNTEMAD    │  │
│  │   Payment    │    │    Center    │    │      EC      │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## CNTEMAD Student

Profil mpianatra nitarina.

### Saha

| Saha | Karazana | Famaritana |
|------|----------|------------|
| `name` | Data | ID tokana (auto: STU-XXXXX) |
| `student_name` | Data | Anarana feno |
| `email` | Data | Mailaka (tokana) |
| `phone` | Data | Finday |
| `cin` | Data | Laharana CIN |
| `center` | Link → CNTEMAD Center | Foibe isam-paritra |
| `program` | Select | Sampana |
| `level` | Select | L1, L2, L3, M1, M2 |
| `enrollment_date` | Date | Daty fisoratana |
| `status` | Select | active, inactive, suspended |
| `user` | Link → User | Kaonty Frappe mifandray |

### Ohatra JSON

```json
{
  "doctype": "CNTEMAD Student",
  "name": "STU-00001",
  "student_name": "Rakoto Jean",
  "email": "rakoto@email.com",
  "phone": "0341234567",
  "cin": "101234567890",
  "center": "CTR-TANA",
  "program": "Informatika",
  "level": "L2",
  "enrollment_date": "2023-09-01",
  "status": "active"
}
```

### Fahazoan-dàlana

| Andraikitra | Mamaky | Manoratra | Mamorona | Mamafa |
|-------------|--------|-----------|----------|--------|
| Student | ✓ (tena) | ✓ (voafetra) | ✗ | ✗ |
| Center Admin | ✓ (foibe) | ✓ | ✓ | ✗ |
| National Admin | ✓ | ✓ | ✓ | ✓ |

## CNTEMAD Course

Lesona miaraka amin'ny métadonnées.

### Saha

| Saha | Karazana | Famaritana |
|------|----------|------------|
| `name` | Data | ID tokana (auto: CRS-XXXXX) |
| `title` | Data | Lohateny ny lesona |
| `code` | Data | Code tokana (oh: INFO-L1-PY01) |
| `description` | Text | Famaritana lava |
| `program` | Select | Sampana |
| `level` | Select | Ambaratonga ilaina |
| `instructor` | Link → User | Mpampianatra tompon'andraikitra |
| `image` | Attach Image | Vignette |
| `status` | Select | draft, review, published, archived |
| `ecs` | Table → CNTEMAD EC | Lisitry ny EC |

## CNTEMAD EC

Élément Constitutif (unité d'enseignement).

### Saha

| Saha | Karazana | Famaritana |
|------|----------|------------|
| `name` | Data | ID tokana (auto: EC-XXXXX) |
| `title` | Data | Lohateny ny EC |
| `code` | Data | Code tokana |
| `course` | Link → CNTEMAD Course | Lesona ray aman-dreny |
| `order` | Int | Filaharan'ny fampisehoana |
| `credits` | Int | Crédits ECTS |
| `duration_hours` | Int | Faharetana vinavina |
| `fee` | Currency | Saram-pianarana |
| `passing_score` | Int | Naoty fidirana (%) |

### Toetry ny fanekena

Ny EC dia afaka ao amin'ny toetra manaraka ho an'ny mpianatra:
- `not_started` : Tsy mbola natomboka
- `in_progress` : Eo am-pandehanana
- `completed` : Fampianarana vita, quiz tsy mbola natao
- `validated` : Quiz nahomby
- `failed` : Quiz tsy nahomby (fanandramana lany)

## CNTEMAD Payment

Transaction fandoavana.

### Saha

| Saha | Karazana | Famaritana |
|------|----------|------------|
| `name` | Data | ID transaction |
| `student` | Link → CNTEMAD Student | Mpianatra |
| `amount` | Currency | Vola |
| `provider` | Select | mvola, orange_money, airtel_money |
| `provider_ref` | Data | Référence provider |
| `phone` | Data | Finday nampiasaina |
| `status` | Select | pending, processing, success, failed, refunded |
| `ec_items` | Table | Lisitry ny EC voaloa |
| `created_at` | Datetime | Daty famoronana |
| `confirmed_at` | Datetime | Daty fanamafisana |

## CNTEMAD Center

Foibe isam-paritra.

### Saha

| Saha | Karazana | Famaritana |
|------|----------|------------|
| `name` | Data | ID foibe |
| `center_name` | Data | Anarana feno |
| `region` | Data | Faritra Madagasikara |
| `address` | Text | Adiresy ara-batana |
| `phone` | Data | Finday fifandraisana |
| `email` | Data | Mailaka fifandraisana |
| `manager` | Link → User | Tompon'andraikitra |
| `is_active` | Check | Mavitrika/Tsy mavitrika |

### Lisitry ny foibe 34

Ny foibe dia manarona ny faritra rehetra ao Madagasikara:
- Antananarivo (foibe lehibe)
- Toamasina
- Mahajanga
- Fianarantsoa
- Antsiranana
- Toliara
- ... (28 hafa)

## CNTEMAD Enrollment

Fisoratana mpianatra amin'ny lesona/EC.

### Saha

| Saha | Karazana | Famaritana |
|------|----------|------------|
| `name` | Data | ID fisoratana |
| `student` | Link → CNTEMAD Student | Mpianatra |
| `course` | Link → CNTEMAD Course | Lesona |
| `ec` | Link → CNTEMAD EC | EC manokana |
| `enrolled_date` | Date | Daty fisoratana |
| `status` | Select | enrolled, in_progress, completed, dropped |
| `payment` | Link → CNTEMAD Payment | Fandoavana mifandray |
| `progress` | Percent | Fandrosoana (%) |
| `score` | Int | Naoty azo |
| `validated_date` | Date | Daty fanekena |

## Fifandraisana

### Diagramme ER

```
CNTEMAD Student ─────┬────▶ CNTEMAD Enrollment ◀────┬───── CNTEMAD Course
       │             │              │               │            │
       ▼             │              │               │            ▼
CNTEMAD Payment ─────┘              │               └───── CNTEMAD EC
       │                            │
       └────────────────────────────┘
                    │
                    ▼
            CNTEMAD Center
```

### Fepetra

1. Mpianatra iray dia ao amin'ny foibe iray ihany
2. Lesona iray dia afaka manana EC maromaro
3. Fandoavana iray dia afaka manarona EC maromaro
4. Fisoratana iray dia mampifandray mpianatra amin'ny EC manokana

---

Jereo koa: [API Reference](/mg/technique/api) | [Mandray anjara](/mg/technique/contributing)
