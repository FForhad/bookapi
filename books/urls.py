from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import BookListView, UserRegistrationView, BookCreateView, BookUpdateView

from .views import OemCreateView, DealerCreateView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('books/add/', BookCreateView.as_view(), name='book_add'),
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book'),
    path('books/', BookListView.as_view(), name='book_list'),

    path('oems/', OemCreateView.as_view(), name='create_oem'),
    path('dealers/', DealerCreateView.as_view(), name='create_dealer'),
]
