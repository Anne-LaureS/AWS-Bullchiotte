#!/bin/bash

# ============================================
# Setup_Nginx.sh - Installation et configuration Nginx pour GitHub repo
# ============================================

# Variables
REPO_URL="https://github.com/Anne-LaureS/AWS-Bullchiotte.git"
IP_PUBLIQUE="18.212.255.63"
NGINX_ROOT="/usr/share/nginx/html"
REPO_DIR="$NGINX_ROOT/AWS-Bullchiotte"
CONF_FILE="/etc/nginx/conf.d/aws-bullchiotte.conf"

echo "==== Installation et configuration Nginx pour votre repo ===="

# Mise à jour du système
echo "Mise à jour du système..."
sudo dnf update -y

# Installation de Nginx
echo "Installation de Nginx..."
sudo dnf install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx

# Clonage ou mise à jour du repo
if [ -d "$REPO_DIR" ]; then
    echo "Le repo existe déjà, mise à jour..."
    cd "$REPO_DIR" && git pull
else
    echo "Clonage du repo GitHub..."
    git clone "$REPO_URL" "$REPO_DIR"
fi

# Préparation de la configuration Nginx
echo "Préparation du dossier Nginx et configuration..."
sudo tee "$CONF_FILE" > /dev/null <<EOF
server {
    listen 80;
    server_name $IP_PUBLIQUE;

    root $REPO_DIR;
    index index.html;

    location / {
        try_files \$uri \$uri/ =404;
    }
}
EOF

# Test de la configuration Nginx
sudo nginx -t

# Redémarrage de Nginx
sudo systemctl restart nginx

echo "==========================================="
echo "Le site est disponible sur : http://$IP_PUBLIQUE/"
echo "==========================================="
