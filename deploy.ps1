# Azure deployment script
# Set these environment variables before running:
# AZURE_STORAGE_ACCOUNT_NAME
# AZURE_STORAGE_ACCOUNT_KEY
# AZURE_STORAGE_CONTAINER_NAME
# DATABASE_URL

# Install requirements
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Apply migrations
python manage.py migrate

# Create superuser (optional)
# python manage.py createsuperuser --noinput
