from django.shortcuts import render


def post_login_view(request):
    user = request.user

    return render(request, "users/post-login.html", {"user": user})
