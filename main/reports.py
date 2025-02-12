from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from .models import Deposit

@staff_member_required
def deposit_report(request):
    department_totals = (
        Deposit.objects.values("account_number")
        .annotate(total_amount=Sum("amount"), total_transactions=Count("id"))
        .order_by("-total_amount")
    )

    context = {"department_totals": department_totals}
    return render(request, "admin/deposit_report.html", context)
