# ADR-0001: Use Django + DRF + PostgreSQL + Docker Compose

- Status: Accepted
- Date: 2025-08-14

## Context
MVPを迅速に立ち上げ、管理画面/認証/ORM/マイグレーションを最小実装で得たい。講師個人〜小規模運用を想定し、保守コストを抑える。

## Decision
- Backend: Django 5 + DRF
- DB: PostgreSQL 16
- Infra: Docker Compose（開発/検証）、本番は Lightsail + Nginx
- Docs: Mermaid/PlantUML + ADR

## Consequences
- 学習コストは低いが、超高スループット要件にはチューニングが必要
- モノリス構成で最初は運用容易。将来的にAPI分離も可能
