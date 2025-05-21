from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
import json
from datetime import date, timedelta

from .models import Action
from .forms import ActionForm
from histories.models import ActionHistory

@login_required
def action_create_view(request):
    if request.method == 'POST':
        form = ActionForm(request.POST)
        if form.is_valid():
            new_action = form.save(commit=False)
            new_action.user = request.user
            new_action.save()
            messages.success(request, f'{new_action.name}を作成しました！')
            return redirect('mypage')
    else:
        form = ActionForm()

    return render(request, 'actions/action_create.html', {'form': form})


@login_required
def action_detail_view(request, action_id):
    action = get_object_or_404(
        Action,
        pk=action_id,
        user=request.user,
        is_deleted=False
    )

    today = date.today()
    dates = [today - timedelta(days=i) for i in range(6, -1, -1)]  # n-6 ~ n

    labels = [d.strftime('%Y-%m-%d') for d in dates]
    data = []
    cumulative_count = 0

    all_histories = ActionHistory.objects.filter(
        action=action,
        created_at__date__lte=today
    ).order_by('created_at__date')

    for d in dates:
        cumulative_count = all_histories.filter(created_at__date__lte=d).count()
        data.append(cumulative_count)

    labels_json = json.dumps(labels)
    data_json = json.dumps(data)

    context = {
        'action': action,
        'labels_json': labels_json,
        'data_json': data_json,
    }
    return render(request, 'actions/action_detail.html', context)

@login_required
def action_record_view(request, action_id):
    action = get_object_or_404(
        Action,
        pk=action_id,
        user=request.user,
        is_deleted=False
    )
    request.user.point += action.point
    request.user.save()

    ActionHistory.objects.create(
        user=request.user,
        action=action,
        point_change=action.point
    )

    messages.success(request, f'{action.name}を記録しました！')
    
    # リファラーからリダイレクト先を決定
    if 'HTTP_REFERER' in request.META:
        referer_url = request.META['HTTP_REFERER']
        action_detail_url = reverse('action_detail', args=[action_id])
        if action_detail_url in referer_url:
            return redirect('action_detail', action_id=action_id)
        else:
            return redirect('mypage')
    else:
        return redirect('mypage')


@login_required
def action_update_view(request, action_id):
    action = get_object_or_404(
        Action,
        pk=action_id,
        user=request.user,
        is_deleted=False
    )

    if request.method == 'POST':
        form = ActionForm(request.POST, instance=action)
        if form.is_valid():
            form.save()
            messages.success(request, f'{action.name}を更新しました！')
            return redirect('action_detail', action_id=action_id)
    else:
        form = ActionForm(instance=action)

    return render(request, 'actions/action_update.html', {
        'form': form,
        'action': action
    })


@login_required
def action_delete_confirm_view(request, action_id):
    action = get_object_or_404(
        Action,
        pk=action_id,
        user=request.user,
        is_deleted=False
    )
    if request.method == 'POST':
        action.is_deleted = True
        action.save()
        messages.success(request, f'{action.name}を削除しました！')
        return redirect('mypage')

    return render(request, 'actions/action_delete_confirm.html', {'action': action})


@login_required
def action_delete_view(request, action_id):
    """
    ソフトデリート
    is_deletedフラグをTrueにして非表示扱いとし、
    処理後にマイページにリダイレクトする。
    """
    action = get_object_or_404(
        Action,
        pk=action_id,
        user=request.user,
        is_deleted=False
    )
    action.is_deleted = True
    action.save()

    return redirect('mypage')