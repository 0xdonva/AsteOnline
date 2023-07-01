"""
URL configuration for AsteOnline project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from gestione import urls
from . import views

urlpatterns = [
    path('signupV/', views.VenditoreCreate.as_view(), name = 'registrazione-venditore'),
    path('signupA/', views.AcquirenteCreate.as_view(), name = 'registrazione-acquirente'),
    path('signup/', views.UtenteCreate.as_view(), name = 'registrazione'),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),

    path('gestione/', include('gestione.urls')),
    path('admin/', admin.site.urls),

    path('', views.HomeView.as_view(), name="homepage")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
