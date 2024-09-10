from django.urls import path
from . import views

urlpatterns = [
    path('', views.Homepage, name='home'),
    path('aboutus/', views.aboutUs, name='about_us'),
    path('login/', views.loginUser, name='login_user'),
    path('logout/', views.logoutUser, name='logout_user'),
    path('updateprofile/', views.updateUserprofile, name='update_userprofile' ),
    path('updatepassword/', views.updatePassword, name='update_password' ),
    path('updateuserinfo/', views.updateUserinfo, name='update_userinfo' ),
    path('signup/', views.signupUser, name='signup_user'),
    path('viewproduct/<int:pk>', views.viewProduct, name='view_product'),
    path('category/<str:cat_name>', views.categoricalProduct, name='categorical_product'),
    path('categories/', views.categorySummery, name='categories_summery'),
     path('searchproduct/', views.searchProduct, name='search_product'),
]
