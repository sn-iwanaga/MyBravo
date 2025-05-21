from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Reward
from .forms import RewardForm
from django.contrib import messages
from histories.models import RewardHistory


@login_required
def reward_create_view(request):
    if request.method == 'POST':
        form = RewardForm(request.POST)
        if form.is_valid():
            new_reward = form.save(commit=False)
            new_reward.user = request.user
            new_reward.save()
            messages.success(request, f'{new_reward.name}を作成しました！')
            return redirect('mypage')
    else:
        form = RewardForm()
    return render(request, 'rewards/reward_create.html', {'form': form})

@login_required
def reward_detail_view(request, reward_id):
    reward = get_object_or_404(Reward, pk=reward_id, user=request.user, is_deleted=False)
    context = {
        'reward': reward,
    }
    return render(request, 'rewards/reward_detail.html', context)

@login_required
def reward_exchange_view(request, reward_id):
    reward = get_object_or_404(Reward, pk=reward_id, user=request.user, is_deleted=False)
    if request.user.point < reward.point:
        return render(request, 'rewards/reward_confirm.html', {
            'reward': reward,
            'error': 'ポイントが不足しています。'
        })
    request.user.point -= reward.point
    request.user.save()

    RewardHistory.objects.create(
        user=request.user,
        reward=reward,
        point_change=-reward.point
    )
    messages.success(request, f'{reward.name}と交換しました！')
    
    return redirect('mypage')

@login_required
def reward_confirm_view(request, reward_id):
    reward = get_object_or_404(Reward, pk=reward_id, user=request.user, is_deleted=False)
    return render(request, 'rewards/reward_confirm.html', {'reward': reward})


@login_required
def reward_update_view(request, reward_id):
    reward = get_object_or_404(Reward, pk=reward_id, user=request.user, is_deleted=False)
    if request.method == 'POST':
        form = RewardForm(request.POST, instance=reward)
        if form.is_valid():
            form.save()
            messages.success(request, f'{reward.name}を更新しました！')
            return redirect('reward_detail', reward_id=reward_id)
    else:
        form = RewardForm(instance=reward)
    return render(request, 'rewards/reward_update.html', {'form': form, 'reward': reward})

@login_required
def reward_delete_confirm_view(request, reward_id):
    reward = get_object_or_404(Reward, pk=reward_id, user=request.user, is_deleted=False)
    if request.method == 'POST':
        reward.is_deleted = True
        reward.save()
        messages.success(request, f'{reward.name}を削除しました！')
        return redirect('mypage')

    return render(request, 'rewards/reward_delete_confirm.html', {'reward': reward})

@login_required
def reward_delete_view(request, reward_id):
    """
    ソフトデリート
    """
    reward = get_object_or_404(Reward, pk=reward_id, user=request.user, is_deleted=False)
    reward.is_deleted = True
    reward.save()
    return redirect('mypage')