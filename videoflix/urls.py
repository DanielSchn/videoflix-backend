"""
URL configuration for videoflix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.api.views import RegistrationView, UsersView, VerifyEmailView, PasswordResetRequest, PasswordResetConfirm, LoginView, TokenCheckView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('django-rq/', include('django_rq.urls')),
    path('api/', include('videoflix_app.api.urls')),
    path('api/registration/', RegistrationView.as_view(), name='registration'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('api/users/', UsersView.as_view(), name='users'),
    path('api/password-reset/', PasswordResetRequest.as_view(), name='password-reset-request'),
    path('api/password-reset-confirm/', PasswordResetConfirm.as_view(), name='password-reset-confirm'),
    path('api/token-check/', TokenCheckView.as_view(), name='token-check'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)