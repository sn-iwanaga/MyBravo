from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
import json

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('mypage')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('mypage')
        else:
            return render(request, 'accounts/login.html', {'error': 'ログインに失敗しました'})
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def mypage_view(request):
    user = request.user
    total_points = 0
    if hasattr(user, 'actionhistory_set'):
        total_points = sum(h.point_change for h in user.actionhistory_set.all())
    actions = user.action_set.filter(is_deleted=False)
    rewards = user.reward_set.filter(is_deleted=False)

    today = timezone.now().date()
    start_date = today - timedelta(days=6)  # 7日前

    all_histories = user.actionhistory_set.order_by('created_at')

    # 日付ごとの累積ポイントをメモしておく
    cumulative_points = 0
    date_to_cumulative = {}
    for history in all_histories:
        cumulative_points += history.point_change
        # history.created_at は datetime型 なので .date() で日付型に変換
        date_key = history.created_at.date()
        date_to_cumulative[date_key] = cumulative_points

    labels = []
    data = []
    for i in range(7):
        current_day = start_date + timedelta(days=i)
        labels.append(current_day.strftime("%Y-%m-%d"))
        
        closest_cumulative = 0
        for date_key, cum_val in date_to_cumulative.items():
            if date_key <= current_day and cum_val > closest_cumulative:
                closest_cumulative = cum_val
        data.append(closest_cumulative)

    labels_json = json.dumps(labels)
    data_json = json.dumps(data)

    context = {
        'user': user,
        'total_points': total_points,
        'actions': actions,
        'rewards': rewards,
        'labels_json': labels_json,
        'data_json': data_json,
    }
    return render(request, 'accounts/mypage.html', context)