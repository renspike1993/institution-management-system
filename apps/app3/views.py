from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from django.db.models import Q
from django.core.paginator import Paginator
from django.core.paginator import Paginator



@login_required
def index(request):
    return render(request, 'app3/index.html')



@login_required
def user_list(request):
    search_query = request.GET.get("search", "")

    users = User.objects.all().order_by("username")

    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    paginator = Paginator(users, 10)  # show 10 users per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "app3/users/user_list.html", {
        "users": page_obj,    # important
        "page_obj": page_obj, # for pagination controls
        "search_query": search_query,
    })