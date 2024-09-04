# from django.contrib import admin
# from django.urls import path
# from services import views

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', views.home, name='home'),
#     path('register/', views.register_view, name='register'),
#     path('otp_confirmation/', views.otp_confirmation_view, name='otp_confirmation'),
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),
#     path('create_service/', views.create_service, name='create_service'),
#     path('service/<int:id>/', views.service_detail, name='service_detail'),
#     path('service/<int:id>/edit/', views.edit_service, name='edit_service'),
#     path('service/<int:id>/delete/', views.delete_service, name='delete_service'),
#     path('subscribe/<int:id>/', views.subscribe, name='subscribe'),
#     path('subscription_success/', views.subscription_success, name='subscription_success'),
#     path('subscribe/<int:service_id>/', views.subscription_view, name='subscribe'),
#     path('payment/callback/', views.payment_callback, name='payment_callback'),
# ]

from django.contrib import admin
from django.urls import path
from services import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('otp_confirmation/', views.otp_confirmation_view, name='otp_confirmation'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create_service/', views.create_service, name='create_service'),
    path('service/<int:id>/', views.service_detail, name='service_detail'),
    path('service/<int:id>/edit/', views.edit_service, name='edit_service'),
    path('service/<int:id>/delete/', views.delete_service, name='delete_service'),
    path('subscribe/<int:id>/', views.subscribe, name='subscribe'),
    path('subscription_success/', views.subscription_success, name='subscription_success'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)