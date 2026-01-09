# 🍺 Ice Cold Beer Scorekeeper

A mobile-first web application for tracking performance in the arcade game *Ice Cold Beer*. Built with Django REST Framework, React, and PostgreSQL.

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### One-Command Startup

```bash
git clone https://github.com/roddy-devs/hey-ya.git
cd hey-ya
./start.sh
```

That's it! The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **Default credentials**: `admin` / `admin`

## 📋 Features

### Core Functionality
- **Session Tracking**: Start and end play sessions with automatic timing
- **Hole Management**: Track progress through holes 1-10 with automatic loop counting
- **Score Calculation**: Time-based score decay for each hole
- **Ball Drop Recording**: Track ball drops per hole and per session
- **Session History**: View past sessions with detailed statistics
- **Mobile-First UI**: Arcade-style LED scoreboard optimized for touch controls

### Technical Features
- Django REST Framework backend with PostgreSQL
- React frontend with modern hooks
- Docker containerization for easy deployment
- Poetry for Python dependency management
- Session-based authentication
- CORS-enabled API

## 🏗️ Architecture

### Tech Stack
- **Backend**: Django 6.0 + Django REST Framework 3.16
- **Frontend**: React 18
- **Database**: PostgreSQL 16
- **Container**: Docker + Docker Compose
- **Python**: Poetry (no virtualenv)
- **Node**: npm

### Project Structure
```
.
├── backend/              # Django backend
│   ├── config/          # Django settings
│   ├── scorekeeper/     # Main app (models, views, serializers)
│   ├── manage.py
│   └── pyproject.toml   # Poetry dependencies
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── App.js
│   │   └── api.js       # API client
│   └── package.json
├── docker/              # Dockerfiles
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
├── docker.compose.yml   # Docker Compose configuration
└── start.sh             # One-command startup script
```

## 🛠️ Local Development

### Backend Development

```bash
cd backend

# Install dependencies
poetry install

# Run migrations
poetry run python manage.py migrate

# Create superuser
poetry run python manage.py createsuperuser

# Run development server
poetry run python manage.py runserver
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm start

# Build for production
npm run build
```

## 🐳 Docker Commands

```bash
# Start all services
docker compose up

# Build and start
docker compose up --build

# Run in background
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down

# Run migrations
docker compose exec backend poetry run python manage.py migrate

# Create superuser
docker compose exec backend poetry run python manage.py createsuperuser
```

## 📊 API Endpoints

### Authentication
- `POST /api-auth/login/` - Login
- `POST /api-auth/logout/` - Logout

### Sessions
- `GET /api/sessions/` - List all sessions
- `POST /api/sessions/` - Create new session
- `GET /api/sessions/{id}/` - Get session details
- `POST /api/sessions/{id}/end_session/` - End session
- `POST /api/sessions/{id}/advance_hole/` - Complete current hole and advance
- `POST /api/sessions/{id}/record_ball_drop/` - Record ball drop
- `GET /api/sessions/stats/` - Get user statistics

### Holes
- `GET /api/holes/` - List all holes
- `GET /api/holes/{id}/` - Get hole details

## 🚢 Deployment (AWS EC2)

### EC2 Setup

1. Launch an EC2 instance (Ubuntu 22.04 LTS recommended)
2. Install Docker and Docker Compose:

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt-get update
sudo apt-get install docker-compose-plugin
```

3. Clone and deploy:

```bash
git clone https://github.com/roddy-devs/hey-ya.git
cd hey-ya

# Create .env file
cp .env.example .env
# Edit .env with production values

# Start application
./start.sh
```

### Environment Variables

Create a `.env` file in the root directory:

```env
# Django
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,your-ec2-ip

# Database
POSTGRES_DB=icecold
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-secure-password

# CORS
CORS_ALLOWED_ORIGINS=https://your-domain.com

# Frontend
REACT_APP_API_URL=https://your-domain.com
```

### HTTPS Configuration

For production, set up a reverse proxy with SSL:

```bash
# Install Nginx
sudo apt-get install nginx certbot python3-certbot-nginx

# Configure Nginx
sudo nano /etc/nginx/sites-available/icecold

# Get SSL certificate
sudo certbot --nginx -d your-domain.com
```

Sample Nginx configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /admin/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Auto-start on Reboot

```bash
# Enable Docker to start on boot
sudo systemctl enable docker

# Create systemd service
sudo nano /etc/systemd/system/icecold.service
```

Service file content:

```ini
[Unit]
Description=Ice Cold Beer Scorekeeper
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ubuntu/hey-ya
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Enable the service:

```bash
sudo systemctl enable icecold
sudo systemctl start icecold
```

## 🎮 Usage

### Starting a Session
1. Login with your credentials
2. Click "Start Session" on the Play screen
3. The first hole (Hole 1, Loop 0) will begin automatically

### During Play
- **Ball Drop Button**: Record when the ball drops
- **Next Hole Button**: Complete the current hole and advance to the next
- **End Session Button**: End the session (requires confirmation)

### Viewing History
1. Click "History" in the navigation
2. View all past sessions with scores, loops, and duration
3. Click any session to see detailed hole-by-hole breakdown

### Scoring Logic
- Each hole has a base score (100-1000 points)
- Score decays 1 point per second after the first 10 seconds
- Final score cannot go below zero
- Completing Hole 10 increments the loop counter and resets to Hole 1

## 🔧 Troubleshooting

### Docker Issues
```bash
# Check if containers are running
docker compose ps

# View logs
docker compose logs backend
docker compose logs frontend

# Restart services
docker compose restart
```

### Database Issues
```bash
# Reset database
docker compose down -v
docker compose up -d
docker compose exec backend poetry run python manage.py migrate
```

### CORS Issues
- Ensure `CORS_ALLOWED_ORIGINS` includes your frontend URL
- Check that `withCredentials: true` is set in API requests

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

