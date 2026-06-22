import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saas_project.settings')
django.setup()

from django.contrib.auth.models import User
from billing_portal.models import UserProfile

def create_admin():
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        UserProfile.objects.create(user=admin, role='ADMIN')
        print("Admin user created with username 'admin' and password 'admin123'.")
    else:
        print("Admin user already exists.")

if __name__ == '__main__':
    create_admin()
