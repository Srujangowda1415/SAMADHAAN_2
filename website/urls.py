from django.contrib import admin
from django.urls import path, include
from website import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create/', views.create_post, name='create_post'),  # Create Post page
    path('signup/', views.signup_view, name='signup'),   
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('update/<int:post_id>/', views.update_post, name='update_post'),
    # Sign Up page
    path('', include('django.contrib.auth.urls')),  # Authentication URLs (login/logout)
    path('home/', views.home, name='home'),                       # Homepage (keep at the end)
]
if settings.DEBUG:  # serve media only in dev
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)