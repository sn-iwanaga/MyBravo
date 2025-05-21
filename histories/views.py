from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse
from django.http import Http404
from django.utils import timezone

from .models import ActionHistory, RewardHistory
from .forms import ActionHistoryForm, RewardHistoryForm

@login_required
def history_list_view(request):
    user = request.user

    action_qs = ActionHistory.objects.filter(user=user).values(
        'id', 'created_at', 'point_change', 'action__name'
    ).order_by('-created_at')

    reward_qs = RewardHistory.objects.filter(user=user).values(
        'id', 'created_at', 'point_change', 'reward__name'
    ).order_by('-created_at')

    merged = []
    for a in action_qs:
        merged.append({
            'id': a['id'],
            'created_at': a['created_at'],
            'point_change': a['point_change'],
            'item_name': a['action__name'],
            'type': 'action',
        })
    for r in reward_qs:
        merged.append({
            'id': r['id'],
            'created_at': r['created_at'],
            'point_change': r['point_change'],
            'item_name': r['reward__name'],
            'type': 'reward',
        })

    merged = sorted(merged, key=lambda x: x['created_at'], reverse=True)
    paginator = Paginator(merged, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for item in page_obj.object_list:
        item['detail_url'] = reverse('history_detail', args=[item['id']])

    return render(request, 'histories/history_list.html', {
        'page_obj': page_obj,
    })

@login_required
def history_detail_view(request, history_id):
    try:
        action_history = ActionHistory.objects.get(pk=history_id, user=request.user)
        history_type = 'action'
        item = action_history
    except ActionHistory.DoesNotExist:
        try:
            reward_history = RewardHistory.objects.get(pk=history_id, user=request.user)
            history_type = 'reward'
            item = reward_history
        except RewardHistory.DoesNotExist:
            raise Http404("History not found")

    return render(request, 'histories/history_detail.html', {
        'item': item,
        'history_type': history_type,
    })

@login_required
def history_delete_confirm_view(request, history_id):
    try:
        action_history = ActionHistory.objects.get(pk=history_id, user=request.user)
        history_type = 'action'
        item = action_history
    except ActionHistory.DoesNotExist:
        try:
            reward_history = RewardHistory.objects.get(pk=history_id, user=request.user)
            history_type = 'reward'
            item = reward_history
        except RewardHistory.DoesNotExist:
            raise Http404("History not found")

    user = request.user

    if request.method == 'POST':
        # differenceを計算: この履歴のpoint_change を打ち消す
        difference = -item.point_change
        if user.point + difference < 0:
            messages.error(request, '累積資料ポイントが累積取得ポイントを超過するため、削除できません。')
            return redirect('history_list')

        user.point += difference
        user.save()
        item.delete()
        messages.success(request, '履歴を削除しました！')
        return redirect('history_list')

    return render(request, 'histories/history_delete_confirm.html', {
        'item': item,
        'history_type': history_type,
    })

@login_required
def history_update_view(request, history_id):
    try:
        action_history = ActionHistory.objects.get(pk=history_id, user=request.user)
        history_type = 'action'
        item = action_history
        form_class = ActionHistoryForm
    except ActionHistory.DoesNotExist:
        try:
            reward_history = RewardHistory.objects.get(pk=history_id, user=request.user)
            history_type = 'reward'
            item = reward_history
            form_class = RewardHistoryForm
        except RewardHistory.DoesNotExist:
            raise Http404("History not found")

    user = request.user

    if request.method == 'POST':
        old_point_change = item.point_change
        form = form_class(user=user, data=request.POST, instance=item)

        if form.is_valid():
            updated_item = form.save(commit=False)
            # 更新先が Action の場合: +ポイント, Reward の場合: マイナス
            if history_type == 'action':
                updated_item.point_change = updated_item.action.point
            else:
                updated_item.point_change = -updated_item.reward.point

            # 差分計算
            difference = updated_item.point_change - old_point_change
            if user.point + difference < 0:
                messages.error(request, '累積資料ポイントが累積取得ポイントを超過するため、履歴を更新できません。')
                return render(request, 'histories/history_update.html', {
                    'form': form,
                    'item': item,
                    'history_type': history_type,
                })

            # フォームで入力した created_at も保存される
            updated_item.save()
            user.point += difference
            user.save()

            messages.success(request, '履歴を更新しました！')
            return redirect('history_list')
    else:
        form = form_class(user=user, instance=item)

    return render(request, 'histories/history_update.html', {
        'form': form,
        'item': item,
        'history_type': history_type,
    })