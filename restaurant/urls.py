from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('create-table', views.create_table, name="create-table"),
    path('create-order/<str:pk>/', views.create_order, name="create-order"),
    path('update-table/<str:pk>/', views.update_table, name="update-table"),

    path('view-order/<str:pk>/', views.view_order, name="view-order"),
    path('view-table/<str:pk>/', views.view_table, name="view-table"),

    path('delete-order/<str:pk>/', views.delete_order, name="delete-order"),
    path('delete-table/<str:pk>/', views.delete_table, name="delete-table"),

    path('login/', views.login_view, name="login-view"),
    path('logout/', views.logout_view, name="logout-view"),

    path('create-basic-menu/', views.create_basic_menu, name="create-basic-menu"),
    path('history-view/<str:action>/', views.history_view, name="history-view"),
]