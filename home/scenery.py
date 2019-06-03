from django.shortcuts import render
from home.models import CodeRelay
from home.views import panel_page


def relay_shutdown(request):
    try:
        if request.method == "POST":
            current_user = request.user
            home = request.POST.get("home", "")

            return panel_page(request)
        else:
            return render(request, '505.html', )
    except CodeRelay.DoesNotExist:
        return render(request, "505.html", )
