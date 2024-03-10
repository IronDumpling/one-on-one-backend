from django.urls import path
from .views import contact_views, admin_views

app_name = 'accounts'

urlpatterns = [
    # path('<int:user_id>/', ),
    path('', admin_views.users_view, name='users'),
    path('register/', admin_views.register_view, name='register'),
    path('profile/', admin_views.profile_view, name='profile'),
    path('contacts/', contact_views.contact_list_view, name="contact_list"),
    path('contacts/<int:contact_id>/', contact_views.contact_view, name="contact"),
]