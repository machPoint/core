#!/bin/bash

# Digital Ocean Deployment Script for CORE-SE
# Run this on your droplet after cloning the repo

echo "🚀 CORE-SE Digital Ocean Deployment"
echo "===================================="

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Node.js 18+
echo "📦 Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Python 3.11+
echo "📦 Installing Python..."
sudo apt install -y python3 python3-pip python3-venv

# Install PM2 for process management
echo "📦 Installing PM2..."
sudo npm install -g pm2

# Navigate to project directory
cd /var/www/CORE_SE || exit

# Setup Backend
echo "🐍 Setting up Python backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..

# Setup Frontend
echo "⚛️ Setting up Next.js frontend..."
cd frontend
npm install
npm run build
cd ..

# Create .env file
echo "🔑 Creating .env file..."
cat > .env << EOL
# OpenAI Configuration
MODEL=gpt-4o
OPENAI_API_KEY=your_key_here
EOL

echo "⚠️  IMPORTANT: Edit .env file and add your OpenAI API key!"

# Setup PM2 ecosystem
echo "📝 Creating PM2 ecosystem file..."
cat > ecosystem.config.js << EOL
module.exports = {
  apps: [
    {
      name: 'core-se-frontend',
      cwd: './frontend',
      script: 'npm',
      args: 'start',
      env: {
        NODE_ENV: 'production',
        PORT: 3000
      }
    },
    {
      name: 'core-se-backend',
      cwd: './backend',
      script: './venv/bin/python',
      args: 'main.py',
      env: {
        PYTHONUNBUFFERED: 1,
        PORT: 8000
      }
    }
  ]
};
EOL

# Setup Nginx reverse proxy
echo "🌐 Setting up Nginx..."
sudo apt install -y nginx

sudo cat > /etc/nginx/sites-available/core-se << EOL
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOL

sudo ln -s /etc/nginx/sites-available/core-se /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Setup firewall
echo "🔥 Configuring firewall..."
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw --force enable

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit .env file: nano .env"
echo "2. Add your OpenAI API key"
echo "3. Start services: pm2 start ecosystem.config.js"
echo "4. Save PM2 config: pm2 save"
echo "5. Setup PM2 startup: pm2 startup"
echo ""
echo "🌐 Your app will be available at: http://your-droplet-ip"
echo ""
echo "📊 Useful commands:"
echo "  pm2 status          - Check app status"
echo "  pm2 logs            - View logs"
echo "  pm2 restart all     - Restart all services"
echo "  pm2 stop all        - Stop all services"
EOL
