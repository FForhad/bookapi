from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from books.models import Role, Oem, Dealer  # Replace 'your_app' with the actual name of your app

User = get_user_model()

class Command(BaseCommand):
    help = "Create multiple users for each role with predefined account numbers."

    def handle(self, *args, **kwargs):
        # Common password for all accounts
        password = '1'

        # Define lists of emails for each role
        superadmin_emails = ['superadmin1@example.com', 'superadmin2@example.com']
        oem_admin_emails = ['oemadmin1@example.com', 'oemadmin2@example.com']
        oem_user_emails = ['oemuser1@example.com', 'oemuser2@example.com']
        dealer_admin_emails = ['dealeradmin1@example.com', 'dealeradmin2@example.com']
        dealer_user_emails = ['dealeruser1@example.com', 'dealeruser2@example.com']
        customer_emails = ['customer1@example.com', 'customer2@example.com']

        # OEMs for OEM Admin and User (only oem_number required)
        oems = [
            {'oem_name': 'OEM1', 'oem_number': 'OEM123'},
            {'oem_name': 'OEM2', 'oem_number': 'OEM456'}
        ]

        # Dealers for Dealer Admin/User (both dealer_number and oem_number required)
        dealers = [
            {'dealer_name': 'Dealer1', 'dealer_number': 'DEALER123', 'oem_number': 'OEM123'},
            {'dealer_name': 'Dealer2', 'dealer_number': 'DEALER456', 'oem_number': 'OEM456'}
        ]

        # 1. Create multiple SuperAdmins
        for email in superadmin_emails:
            if not User.objects.filter(email=email).exists():
                User.objects.create_user(
                    email=email,
                    password=password,
                    role=Role.SUPERADMIN
                )
                self.stdout.write(self.style.SUCCESS(f'SuperAdmin account created: {email}'))
            else:
                self.stdout.write(self.style.WARNING(f'SuperAdmin account already exists: {email}'))

        # 2. Create multiple OEM Admins and OEM Users
        for i, oem_data in enumerate(oems):
            oem, created = Oem.objects.get_or_create(oem_name=oem_data['oem_name'], oem_number=oem_data['oem_number'])

            # Create OEM Admins
            if not User.objects.filter(email=oem_admin_emails[i]).exists():
                User.objects.create_user(
                    email=oem_admin_emails[i],
                    password=password,
                    role=Role.OEM_ADMIN,
                    oem=oem
                )
                self.stdout.write(self.style.SUCCESS(f'OEM Admin account created: {oem_admin_emails[i]}'))
            else:
                self.stdout.write(self.style.WARNING(f'OEM Admin account already exists: {oem_admin_emails[i]}'))

            # Create OEM Users
            if not User.objects.filter(email=oem_user_emails[i]).exists():
                User.objects.create_user(
                    email=oem_user_emails[i],
                    password=password,
                    role=Role.OEM_USER,
                    oem=oem
                )
                self.stdout.write(self.style.SUCCESS(f'OEM User account created: {oem_user_emails[i]}'))
            else:
                self.stdout.write(self.style.WARNING(f'OEM User account already exists: {oem_user_emails[i]}'))

        # 3. Create multiple Dealer Admins and Dealer Users
        for i, dealer_data in enumerate(dealers):
            dealer, created = Dealer.objects.get_or_create(
                dealer_name=dealer_data['dealer_name'],
                dealer_number=dealer_data['dealer_number'],
                oem=Oem.objects.get(oem_number=dealer_data['oem_number'])
            )

            # Create Dealer Admins
            if not User.objects.filter(email=dealer_admin_emails[i]).exists():
                User.objects.create_user(
                    email=dealer_admin_emails[i],
                    password=password,
                    role=Role.DEALER_ADMIN,
                    dealer=dealer
                )
                self.stdout.write(self.style.SUCCESS(f'Dealer Admin account created: {dealer_admin_emails[i]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Dealer Admin account already exists: {dealer_admin_emails[i]}'))

            # Create Dealer Users
            if not User.objects.filter(email=dealer_user_emails[i]).exists():
                User.objects.create_user(
                    email=dealer_user_emails[i],
                    password=password,
                    role=Role.DEALER_USER,
                    dealer=dealer
                )
                self.stdout.write(self.style.SUCCESS(f'Dealer User account created: {dealer_user_emails[i]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Dealer User account already exists: {dealer_user_emails[i]}'))

        # 4. Create multiple Customers
        for i, email in enumerate(customer_emails):
            dealer = Dealer.objects.get(dealer_number=dealers[i]['dealer_number'])
            if not User.objects.filter(email=email).exists():
                User.objects.create_user(
                    email=email,
                    password=password,
                    role=Role.CUSTOMER,
                    dealer=dealer,
                    oem=dealer.oem
                )
                self.stdout.write(self.style.SUCCESS(f'Customer account created: {email}'))
            else:
                self.stdout.write(self.style.WARNING(f'Customer account already exists: {email}'))

        self.stdout.write(self.style.SUCCESS('All accounts processed.'))
