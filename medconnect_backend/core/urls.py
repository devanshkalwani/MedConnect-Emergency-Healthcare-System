from django.urls import path
from .views import *
from .views import get_hospitals

urlpatterns = [
    path('', api_home),

    path('user/register/', register_user),
    path('user/login/', login_user),

    path('hospital/register/', register_hospital),
    path('hospital/login/', login_hospital),

    path('sos/', create_sos),

    path('hospital/sos/', get_hospital_sos),
    path('hospital/sos/<int:request_id>/', get_sos_details),
    path('hospitals/', get_hospitals),
    path('hospital/accept/<int:request_id>/', accept_request),
    path('sos/resolve/<int:request_id>/', resolve_sos),

    path('status/<int:user_id>/', check_status),
    path('history/<int:user_id>/', get_history),
    path('user/<int:user_id>/', get_user_profile),
    path('user/update/', update_user_profile),
    path('user/change-password/', change_password),
    path('user/preferences/', save_preferences),
    path('contacts/<int:user_id>/', get_contacts),
    path('contacts/add/', add_contact),
    path('contact/', contact_message),
]