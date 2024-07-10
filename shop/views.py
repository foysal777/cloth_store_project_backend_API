from django.shortcuts import render,redirect
from rest_framework import viewsets
from rest_framework.views import APIView
from  . import serializers
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives 
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from .models import Product, Review , Wishlist
from .serializers import ProductSerailizers , ReviewSerializers , WishlistSerializers 
 
 
 
class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerailizers
    
    # Filter case sensative 
           
    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        size = self.request.query_params.get('size')
        color = self.request.query_params.get('color')
        if size:
            queryset = queryset.filter(size__icontains=size)
        if color:
            queryset = queryset.filter(color__icontains=color)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
class ReviewViewset(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    
    
class WishListViewset(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializers        
    
    
    
    # Registration Part 
    
class userRegistration(APIView):
        
    serializer_class = serializers.RegistrationSerialization
       
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        
       
        
        if serializer.is_valid():
            user =  serializer.save()
            print(user)
            token = default_token_generator.make_token(user)
            print(token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("uid" , uid)
            confirm_link = f"http://127.0.0.1:8000/shop/active/{uid}/{token}"
            email_subject = "Confirm Your Email Now"
            email_body = render_to_string('confirm_email.html', { 'confirm_link': confirm_link})
            email = EmailMultiAlternatives(email_subject , "" , to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            
            return Response("Check Your E-mail Confirmation..")
        return Response (serializer.errors)
        
def activate(request, uid64, token): 
    print(uid64)
    print(token)
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')
    
    
    
    
# log in part 
class UserLoginApiView(APIView):
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data = self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username= username, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                print(token)
                print(_)
                login(request, user)
                return Response({'token' : token.key, 'user_id' : user.id})
            else:
                return Response({'error' : "Invalid Credential"})
        return Response(serializer.errors)
    
    
    
#  log out part 


class UserLogoutView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
         # return redirect('login')
        return Response({'success' : "logout successful"})   
    
