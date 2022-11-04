from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from users import views as view
from crpyto.views import index


name="register"

urlpatterns = [
    path('admin/', admin.site.urls),
   
    path('', include('crpyto.urls')),
    path('profile/', view.profile, name='profile'),
    path('register/', view.register, name='register'),
    # path('register/', register.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/auth_login2.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('<str:ref_code>/', index, name="index"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings. STATIC_URL, document_root=settings.STATIC_ROOT)