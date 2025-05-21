from django.urls import path
from . import views

urlpatterns = [
    path('', views.history_list_view, name='history_list'),
    path('<int:history_id>/', views.history_detail_view, name='history_detail'),
    path('<int:history_id>/delete/', views.history_delete_confirm_view, name='history_delete_confirm'),
    path('<int:history_id>/update/', views.history_update_view, name='history_update'),
]