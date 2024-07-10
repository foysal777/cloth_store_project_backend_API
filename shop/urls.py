from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewset , ReviewViewset , WishListViewset
from . import views

router = DefaultRouter()
router.register('product' , ProductViewset)
router.register('Review' , ReviewViewset)
router.register('wishlist' , WishListViewset)


urlpatterns = [
    path('' , include(router.urls)),
    path('register/' , views.userRegistration.as_view() , name= 'register'),
    path('active/<uid64>/<token>/', views.activate, name = 'activate'),
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]