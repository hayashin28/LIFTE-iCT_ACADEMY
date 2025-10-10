# LIFTE-iCT ACADEMY DX — MVP Skeleton (v0.1, 2025-08-14)

このリポジトリは **Django 5 + PostgreSQL + Docker Compose** を前提とした最小構成です。  
「5分で動く」を目標に、まず雛形を起動 → 主要モデルを追加 → QR出欠のPoCを確認する流れです。

## 0) 事前準備
- Docker / Docker Compose が動作する環境
- `.env` を `.env.template` からコピーして値を調整

```bash
cp .env.template .env
```

## 1) 起動（初回）
```bash
docker compose -f infra/compose.yaml up --build
```
- DB起動 → Webビルド → `makemigrations` & `migrate` 実行後に `http://localhost:8000/` で確認できます。
- 管理画面: `http://localhost:8000/admin/` （初回は superuser 作成が必要）

```bash
docker compose -f infra/compose.yaml exec web python manage.py createsuperuser
```

## 2) 主要モデル
- Student, Classroom, Enrollment, Lesson, Attendance (+ QrTicket)
  - `app/modules/*/models.py` をご覧ください。

## 3) QR出欠PoC（超簡易）
- `GET /api/attendance/mark/<uuid:token>/` にアクセスすると、トークンを検証して出席に打刻します。
- トークンは `QrTicket` モデル（lesson×student×有効期限）で管理します。

※ 生成は管理画面から直接レコード追加（PoC）。運用時は管理コマンド/画面を追加予定。

## 4) Docs
- `docs/architecture/` に Mermaid/PlantUML の雛形と ADR テンプレートがあります。

---
Happy hacking! (✿´ ꒳ ` )ノ
