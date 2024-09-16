from rest_framework import serializers
from .models import Book, CustomUser, Role, Oem, Dealer

class UserRegistrationSerializer(serializers.ModelSerializer):
    oem = serializers.PrimaryKeyRelatedField(queryset=Oem.objects.all(), required=False)  # OemNo (optional)
    dealer = serializers.PrimaryKeyRelatedField(queryset=Dealer.objects.all(), required=False)  # DealerNo (optional)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'role', 'oem', 'dealer')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', Role.CUSTOMER),
            oem=validated_data.get('oem', None),  # OemNo
            dealer=validated_data.get('dealer', None)  # DealerNo
        )
        return user

class OemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oem
        fields = ['id', 'oem_name', 'oem_number']

class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = ['id', 'dealer_name', 'dealer_number', 'oem']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'role')


class BookSerializer(serializers.ModelSerializer):
    dealer_id = serializers.IntegerField(write_only=True)  # Accept dealer ID in the request
    dealer = serializers.SerializerMethodField()  # Show dealer information in the response

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'dealer_id', 'dealer']

    def get_dealer(self, obj):
        # Display dealer information in the response
        if obj.dealer:
            return {
                'dealer_name': obj.dealer.email,  # Assuming the email represents the dealer
                'dealer_id': obj.dealer.id
            }
        return None

    def create(self, validated_data):
        dealer_id = validated_data.pop('dealer_id')
        
        # Fetch the dealer (CustomUser) using the provided dealer_id
        try:
            dealer = CustomUser.objects.get(id=dealer_id, role__in=[Role.DEALER_ADMIN, Role.DEALER_USER])
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Dealer with this account number does not exist.")
        
        # Create the book and assign it to the dealer
        book = Book.objects.create(dealer=dealer, **validated_data)
        return book
