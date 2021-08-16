root=$(realpath $(pwd)/..)

# Install asdf
asdf install

# Association Frontend

echo "👥 Installing Association frontend dependencies"

cd $root/association-frontend
yarn install

# PyCon Frontend

echo "🐍 Installing PyCon dependencies"

cd $root/frontend
yarn install

# Gateway

echo "🎨 Installing Gateway dependencies"
cd $root/gateway
yarn install

# Association Backend

echo "👥 Installing Association Backend dependencies"

cd $root/association-backend
poetry install

# PyCon Backend

echo "🐍 Installing PyCon Backend dependencies"

cd $root/association-backend
poetry install

# Users Backend

echo "👱‍♀️ Installing Users Backend dependencies"

cd $root/users-backend
poetry install
