from django.urls import path
from .views import (
    reward_create_view,
    reward_detail_view,
    reward_update_view,
    reward_delete_confirm_view,
)

urlpatterns = [
    path('create/', reward_create_view, name='reward_create'),
    path('<int:reward_id>/', reward_detail_view, name='reward_detail'),
    path('<int:reward_id>/edit/', reward_update_view, name='reward_update'),
    path('<int:reward_id>/delete/', reward_delete_confirm_view, name='reward_delete'),
]