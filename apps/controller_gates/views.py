from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from .models import TurnstileAttendanceLog


def attendance_logs(request):
    search = request.GET.get("search", "").strip()

    logs = TurnstileAttendanceLog.objects.all().order_by("-timestamp")

    # ✅ SEARCH FILTER
    if search:
        logs = logs.filter(
            Q(full_name__icontains=search) |
            Q(person_id__icontains=search) |
            Q(gate_name__icontains=search)
        )

    # ✅ PAGINATION
    paginator = Paginator(logs, 10)  # 10 logs per page
    page_number = request.GET.get("page")
    logs_page = paginator.get_page(page_number)

    context = {
        "logs": logs_page,
        "search": search,
    }

    return render(request, "controller_gates/attendance_logs.html", context)
