# C4: Container — LIFTE-iCT ACADEMY DX (v0.1 / 2025-08-14)

Status: Draft
Owner: @hayashin
Last-Updated: 2025-08-14

```mermaid
flowchart LR
  user((User)) -->|TLS| Nginx[Nginx]
  Nginx --> Web[Django + Gunicorn]
  Web --> DB[(PostgreSQL)]
```
