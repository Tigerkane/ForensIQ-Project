# ForensIQ Data Model

## Relational Database (SQLite)

### `Cases`
- `case_id` (PK)
- `title` (String)
- `created_at` (DateTime)
- `status` (String)

### `Events`
- `event_id` (PK)
- `case_id` (FK -> Cases)
- `event` (String)
- `time` (DateTime)
- `location` (String)
- `description` (Text)

### `People`
- `person_id` (PK)
- `case_id` (FK -> Cases)
- `name` (String)
- `role` (String - Suspect, Witness, Officer, Victim)

### `Organizations`
- `organization_id` (PK)
- `case_id` (FK -> Cases)
- `name` (String)

### `Vehicles`
- `vehicle_id` (PK)
- `case_id` (FK -> Cases)
- `registration` (String)
- `model` (String)

### `Evidence`
- `evidence_id` (PK)
- `case_id` (FK -> Cases)
- `type` (String)
- `source_document` (String)

### `Relationships`
- `relationship_id` (PK)
- `entity1` (String/ID)
- `relation` (String - e.g., "Transferred Money To", "Seen At")
- `entity2` (String/ID)

### `Documents`
- `document_id` (PK)
- `case_id` (FK -> Cases)
- `filename` (String)
- `type` (String - PDF, Image, Audio)
- `processed_at` (DateTime)
