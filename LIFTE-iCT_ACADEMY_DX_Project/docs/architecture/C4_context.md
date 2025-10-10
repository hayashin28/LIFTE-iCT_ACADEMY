# C4: Context — LIFTE-iCT ACADEMY DX (v0.1 / 2025-08-14)

Status: Draft
Owner: @hayashin
Last-Updated: 2025-08-14

```mermaid
flowchart TB
  user((生徒/保護者)) -->|学習/提出/出欠| App[Django Webアプリ]
  teacher((講師)) -->|管理/ダッシュボード| App
  App <-->|通知/連携| LINE[LINE Messaging API]
```
