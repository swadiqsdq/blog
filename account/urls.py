

from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.user_register,name='register'),
    path('login/',views.userLogin,name='login'),
    path('logout/',views.userLogout,name="logout"),
    # path('changePassword/',views.changePassword,name='changePassword'),
    path('changePassword/<str:username>',views.changePassword,name='changePassword'),
    path('forgotPassword/',views.forgotPassword,name='forgotPassword'),
    path('otp_verify/<str:username>',views.otp_verify,name='otp_verify')
    
]