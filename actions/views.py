from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Action
from .forms import ActionForm


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

    context = {
        'action': action,
    }
    return render(request, 'actions/action_detail.html', context)

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