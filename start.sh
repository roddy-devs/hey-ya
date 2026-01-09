#!/bin/bash
set -e

echo "🚀 Starting Ice Cold Beer Scorekeeper..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed"
    exit 1
fi

# Check if Docker Compose is available
if ! docker compose version &> /dev/null; then
    echo "❌ Error: Docker Compose is not available"
    exit 1
fi

# Stop any running containers
echo "🛑 Stopping existing containers..."
docker compose down || true

# Build images
echo "🏗️  Building Docker images..."
docker compose build

# Start services
echo "▶️  Starting services..."
docker compose up -d

# Wait for database to be ready
echo "⏳ Waiting for database..."
sleep 5

# Run migrations
echo "🔄 Running database migrations..."
docker compose exec backend poetry run python manage.py migrate

# Create superuser if needed (optional)
echo "👤 Creating superuser (if needed)..."
docker compose exec backend poetry run python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Superuser created: admin/admin')
else:
    print('Superuser already exists')
" || echo "Note: Superuser creation skipped"

echo "✅ Application is ready!"
echo ""
echo "📍 Access points:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000/api/"
echo "   Admin Panel: http://localhost:8000/admin/"
echo "   Admin credentials: admin/admin"
echo ""
echo "📋 Useful commands:"
echo "   View logs: docker compose logs -f"
echo "   Stop: docker compose down"
echo "   Restart: docker compose restart"
