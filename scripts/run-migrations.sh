#!/usr/bin/env bash
set -euo pipefail

docker compose exec backend alembic upgrade head
