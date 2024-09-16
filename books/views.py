from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Book, Role
from .serializers import BookSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserRegistrationSerializer
from rest_framework.exceptions import PermissionDenied

ROLE_HIERARCHY = {
    'SuperAdmin': ['SuperAdmin', 'OemAdmin', 'OemUser', 'DealerAdmin', 'DealerUser', 'Customer'],
    'OemAdmin': ['DealerAdmin', 'DealerUser'],
    'OemUser': ['DealerAdmin', 'DealerUser'],
    'DealerAdmin': ['Customer'],
    'DealerUser': ['Customer'],
    'Customer': []  
}

from rest_framework import generics
from .models import Oem, Dealer
from .serializers import OemSerializer, DealerSerializer

class OemCreateView(generics.CreateAPIView):
    queryset = Oem.objects.all()
    serializer_class = OemSerializer
    permission_classes = [permissions.IsAuthenticated]

class DealerCreateView(generics.CreateAPIView):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        requesting_user_role = self.request.user.role
        
        new_user_role = self.request.data.get('role')
        
        if new_user_role not in ROLE_HIERARCHY[requesting_user_role]:
            raise PermissionDenied("You do not have permission to create this type of user.")
        serializer.save()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['role'] = user.role
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # SuperAdmin can view all books
        if user.role == Role.SUPERADMIN:
            return Book.objects.all()

        # OEM Admin/User can see books assigned to dealers under their OEM
        elif user.role in [Role.OEM_ADMIN, Role.OEM_USER]:
            return Book.objects.filter(dealer__oem=user.oem)

        # Dealer Admin/User can see only the books assigned to them
        elif user.role in [Role.DEALER_ADMIN, Role.DEALER_USER]:
            return Book.objects.filter(dealer=user)

        return Book.objects.none()
