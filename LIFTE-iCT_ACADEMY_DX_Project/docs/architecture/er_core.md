# ER (Core) — LIFTE-iCT ACADEMY DX (v0.1 / 2025-08-14)

Status: Draft
Owner: @hayashin
Last-Updated: 2025-08-14

```mermaid
erDiagram
  STUDENT ||--o{ ENROLLMENT : enrolls
  CLASSROOM ||--o{ ENROLLMENT : has
  CLASSROOM ||--o{ LESSON : schedules
  STUDENT ||--o{ ATTENDANCE : marks
  LESSON ||--o{ ATTENDANCE : records
```
