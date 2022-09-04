from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserPanelDashboardPage.as_view(), name='user_panel_dashboard'),
    path('change-pass', views.ChangePasswordPage.as_view(), name='change_password_page'),
    path('edit-profile', views.EditUserProfilePage.as_view(), name='edit_profile_page'),
    path('user_orders', views.user_orders, name='user_orders_page'),
    path('user_order_details/<order_id>/', views.user_order_details, name='user_order_details_page')
]
