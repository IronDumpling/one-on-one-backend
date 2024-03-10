from django.urls import path
from .views import contact_views, register_view

app_name = 'accounts'

urlpatterns = [
    # path('', ),
    # path('<int:user_id>/', ),
    path('register/', register_view.register_view, name='register'),
    path('contacts/', contact_views.contact_list_view, name="contact_list"),
    path('contacts/<int:contact_id>/', contact_views.contact_view, name="contact"),
]