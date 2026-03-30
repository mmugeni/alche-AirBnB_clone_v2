#!/usr/bin/env bash
# Sets up web servers for deployment of web_static

# Install Nginx
apt-get update
apt-get install -y nginx

# Create directories
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create test HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Create/Update symbolic link
rm -rf /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current

# Set ownership
chown -R ubuntu:ubuntu /data/

# Configure Nginx
sed -i '/server_name _;/a \
    location /hbnb_static/ {\n\
        alias /data/web_static/current/;\n\
    }' /etc/nginx/sites-available/default

# Restart Nginx
service nginx restart
