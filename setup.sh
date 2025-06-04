#!/bin/bash

# Check if .env.local already exists
if [ -f .env.local ]; then
  echo ".env.local already exists. Please remove it first if you want to generate a new one."
  exit 1
fi

# Generate a random secret for NextAuth
NEXTAUTH_SECRET=$(openssl rand -base64 32)

# Create .env.local with the generated secret
cat > .env.local <<EOL
# NextAuth.js
NEXTAUTH_SECRET=$NEXTAUTH_SECRET
NEXTAUTH_URL=http://localhost:3000

# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
EOL

echo ".env.local has been created with a random NEXTAUTH_SECRET"
echo "Please review the configuration and adjust as needed."
