# from django.shortcuts import  render, redirect
# from .forms import RegisterForm
# from django.contrib.auth import login
# from django.contrib import messages #import messages
# from django.contrib.auth import login, authenticate


# def register_request(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = RegisterForm()
#     return render(request, 'accounts/register.html', {'form': form})