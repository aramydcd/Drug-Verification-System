# Reset.ps1 - Reset Django DB, migrations, superuser & roles

Write-Host "🚀 Resetting Django project..." -ForegroundColor Cyan

# Delete database
if (Test-Path "db.sqlite3") {
    Remove-Item "db.sqlite3" -Force
    Write-Host "Deleted db.sqlite3" -ForegroundColor Yellow
}

# Delete migration files except __init__.py
Get-ChildItem -Recurse -Filter "migrations" | ForEach-Object {
    Get-ChildItem $_.FullName -Filter "*.py" | Where-Object { $_.Name -ne "__init__.py" } | Remove-Item -Force
    Write-Host "Deleted migration files in $($_.FullName)" -ForegroundColor Yellow
}

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser & roles
$pythonCommand = @"
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drug_verification.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import Role  # make sure Role model exists in accounts/models.py

User = get_user_model()

# Create default superuser
username = "admin"
email = "admin@example.com"
password = "admin123"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Superuser created: {username} / {password}")
else:
    print("⚠️ Superuser already exists")

# Create default roles
for role_name in ["user", "company", "admin"]:
    Role.objects.get_or_create(name=role_name)
    print(f"✅ Role ensured: {role_name}")
"@

python -c $pythonCommand
