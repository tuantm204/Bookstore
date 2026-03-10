from django.core.management.base import BaseCommand
from authentication.models import User


class Command(BaseCommand):
    help = 'Seed default staff, manager and admin accounts'

    def handle(self, *args, **options):
        accounts = [
            {
                'username': 'admin',
                'email': 'admin@bookstore.com',
                'password': 'admin123',
                'full_name': 'Admin User',
                'role': 'admin',
            },
            {
                'username': 'staff1',
                'email': 'staff1@bookstore.com',
                'password': 'staff123',
                'full_name': 'Nhân viên 1',
                'role': 'staff',
            },
            {
                'username': 'staff2',
                'email': 'staff2@bookstore.com',
                'password': 'staff123',
                'full_name': 'Nhân viên 2',
                'role': 'staff',
            },
            {
                'username': 'manager1',
                'email': 'manager1@bookstore.com',
                'password': 'manager123',
                'full_name': 'Quản lý 1',
                'role': 'manager',
            },
            {
                'username': 'manager2',
                'email': 'manager2@bookstore.com',
                'password': 'manager123',
                'full_name': 'Quản lý 2',
                'role': 'manager',
            },
        ]

        for acc in accounts:
            if User.objects.filter(username=acc['username']).exists():
                self.stdout.write(self.style.WARNING(
                    f"  ⚠ Account '{acc['username']}' already exists, skipping"
                ))
                continue

            user = User(
                username=acc['username'],
                email=acc['email'],
                full_name=acc['full_name'],
                role=acc['role'],
            )
            user.set_password(acc['password'])
            user.save()
            self.stdout.write(self.style.SUCCESS(
                f"  ✅ Created {acc['role']} account: {acc['username']} / {acc['password']}"
            ))

        self.stdout.write(self.style.SUCCESS('\nSeed accounts complete!'))
