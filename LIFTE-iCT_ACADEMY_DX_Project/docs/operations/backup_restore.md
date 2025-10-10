# Backup & Restore — LIFTE-iCT ACADEMY DX (v0.1 / 2025-08-14)

Status: Draft
Owner: @hayashin
Last-Updated: 2025-08-14

## 方針
- 毎日 03:00 に `pg_dump`（.sql.gz）
- 保持 7 日、週次で Lightsail スナップショット

## 復旧手順（要点）
1) `docker compose up -d` で起動
2) 必要なら DB初期化：`DROP SCHEMA public; CREATE SCHEMA public;`
3) 最新の `.sql.gz` を `scripts/restore_db.sh` で適用
