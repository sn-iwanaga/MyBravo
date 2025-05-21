from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.shortcuts import render

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
    actions = user.action_set.filter(is_deleted=False)
    rewards = user.reward_set.filter(is_deleted=False)
    context = {
        'user': user,
        'actions': actions,
        'rewards': rewards,
        
    }
    return render(request, 'accounts/mypage.html', context)