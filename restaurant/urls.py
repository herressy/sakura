from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('create-order/<str:pk>/', views.create_order, name="create-order"),
    path('view-order/<str:pk>/', views.view_order, name="view-order"),

    path('view-table/<str:pk>/', views.view_table, name="view-table"),
    path('update-table/<str:pk>/', views.update_table, name="update-table"),
    path('create-basic-menu/', views.create_basic_menu, name="create-basic-menu"),
    path('login/', views.login_page, name="login-page"),
    path('logout/', views.logout_page, name="logout-page"),

]