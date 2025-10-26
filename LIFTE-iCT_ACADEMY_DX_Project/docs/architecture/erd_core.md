```mermaid
erDiagram
  STUDENT ||--o{ ENROLLMENT : enrolls
  CLASSROOM ||--o{ ENROLLMENT : has
  CLASSROOM ||--o{ LESSON : schedules
  STUDENT ||--o{ ATTENDANCE : marks
  LESSON ||--o{ ATTENDANCE : records
```
