# AgentCoin AI Economy

Production-grade SaaS infrastructure for a multi-tenant, token-powered AI Agent creation economy.

## 1) Full project folder structure
```text
.
├── backend
│   ├── alembic
│   │   ├── env.py
│   │   └── versions/0001_init.py
│   ├── app
│   │   ├── api/v1/router.py
│   │   ├── core/{config.py,security.py}
│   │   ├── db/session.py
│   │   ├── endpoints/{admin.py,agents.py,health.py,marketplace.py,realtime.py,token.py}
│   │   ├── models/models.py
│   │   ├── schemas/agent.py
│   │   ├── services/{commission_service.py,onchain_sync_service.py,ranking_service.py,token_service.py}
│   │   ├── websocket/manager.py
│   │   ├── workers/{celery_app.py,tasks.py}
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend
│   ├── app/{admin,agents,dashboard,marketplace}/page.tsx
│   ├── components/{metric-card.tsx,nav.tsx,performance-chart.tsx}
│   ├── lib/api.ts
│   ├── store/app-store.ts
│   ├── Dockerfile
│   └── package.json
├── deploy
│   ├── nginx/nginx.conf
│   └── ubuntu-22.04-deployment.md
├── scripts/run-migrations.sh
├── docker-compose.yml
└── .env.example
```

## 2) Backend services
- **FastAPI API** with JWT-ready security helpers and versioned routes.
- **PostgreSQL + SQLAlchemy + Alembic** schema for all required domain models:
  Users, Agents, AgentConfigs, Trades, PerformanceMetrics, EquitySnapshots,
  Stakes, Commissions, Subscriptions, MarketplaceListings, AuditLogs.
- **Celery + Redis** worker lane for async tasks (e.g., on-chain sync placeholders).
- **WebSocket manager** for live channel fanout.
- **Health/ready endpoints** for orchestrator checks.

## 3) Frontend pages
- `Overview`: platform KPIs.
- `Agent Factory`: template-driven multi-agent creation concepts.
- `Marketplace`: listing/subscription workflows.
- `Monitoring`: live feed channels + ROI chart (Recharts).
- `Admin`: safe mode and global risk control interface.

## 4) Token integration layer
- ERC20-ready `TokenService` placeholder methods for:
  - staking to activate agent
  - burn-on-create
  - commission distribution
- Wallet connection placeholder endpoint for future Web3 onboarding.
- Stake-aware ranking score function in ranking service.

## 5) Marketplace system
- Marketplace listing table + retrieval endpoint.
- Revenue-share and token subscription pricing primitives.
- Commission utility service for payout math.

## 6) Docker setup
```bash
docker compose up -d --build
```
Services: `db`, `redis`, `backend`, `worker`, `frontend`, `nginx`.

## 7) Nginx config
- Reverse proxy for:
  - `/api/*` -> FastAPI backend
  - `/ws/*` -> FastAPI WebSocket endpoint
  - `/` -> Next.js frontend

## 8) Deployment guide
See: `deploy/ubuntu-22.04-deployment.md`
- Docker installation
- env bootstrap
- migrations
- health checks
- runtime logging

## 9) README documentation
This document is intentionally structured to map directly to the requested output format.

---

## Quick start
```bash
cp .env.example .env
docker compose up -d --build
docker compose exec backend alembic upgrade head
```

Open `http://localhost`.

## Strategy & Whitepaper Draft
A complete crypto startup blueprint (token design, tokenomics, smart contract architecture, whitepaper draft, landing page copy, marketing/launch/community/fundraising strategy, and 12-month roadmap) is available at:
- `docs/agentcoin-crypto-startup-blueprint.md`
