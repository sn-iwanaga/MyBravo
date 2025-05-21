from django.urls import path
from .views import (
    action_create_view,
    action_detail_view,
    action_record_view,
    action_update_view,
    action_delete_confirm_view,
)

urlpatterns = [
    path('create/', action_create_view, name='action_create'),
    path('<int:action_id>/', action_detail_view, name='action_detail'),
    path('<int:action_id>/record/', action_record_view, name='action_record'),
    path('<int:action_id>/edit/', action_update_view, name='action_update'),
    path('<int:action_id>/delete/', action_delete_confirm_view, name='action_delete'),
]