from rest_framework import serializers
from .models import Product, Review, Wishlist
from django.contrib.auth.models import User


class ProductSerailizers(serializers.ModelSerializer):
    class Meta :
        model = Product
        fields = '__all__'
        
        
class ReviewSerializers(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    class Meta :
        model = Review
        fields = '__all__'
        
        
class WishlistSerializers(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    products = serializers.StringRelatedField(many = True)
    class Meta :
        model = Wishlist
        fields = '__all__'
        
        
# user authenticated part 


class RegistrationSerialization(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required = True)
    class Meta:
        model = User   
        fields = ['username' , 'first_name' ,'last_name' , 'email' , 'password' , 'confirm_password']
        
    
    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
       
        if password != password2:
            raise serializers.ValidationError({'error' : "Password Doesn't Match"})
        
        if User.objects.filter(email = email).exists():
            raise serializers.ValidationError({'error' : "Email Already Exists."})      
        
        account = User(username = username , email = email , first_name = first_name , last_name = last_name)
        account.set_password(password)
        account.is_active = False
        account.save()
        return account
    
    


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)        