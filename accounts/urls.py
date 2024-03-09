from django.urls import path
from .views import contact_views

app_name = 'accounts'

urlpatterns = [
    # path('', ),
    # path('<int:user_id>/', ),

    path('<int:user_id>/contacts/', contact_views.contact_list_view, name="contact_list"),
    path('<int:user_id>/contacts/<int:contact_id>/', contact_views.contact_view, name="contact"),
]