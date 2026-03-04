# Ubuntu 22.04 Deployment Guide

## 1) Provision server
- Ubuntu 22.04 LTS, 2+ vCPU, 4GB+ RAM.
- Open ports 22, 80, 443.

## 2) Install Docker + Compose
```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## 3) Configure environment
```bash
cp .env.example .env
# edit .env with production values
```

## 4) Launch stack
```bash
docker compose up -d --build
```

## 5) Run migrations
```bash
docker compose exec backend alembic upgrade head
```

## 6) Health checks
```bash
curl http://localhost/api/v1/health
curl http://localhost/api/v1/ready
```

## 7) Logging
```bash
docker compose logs -f nginx backend worker frontend
```
