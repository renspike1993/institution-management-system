from django.shortcuts import render, redirect, get_object_or_404
from ..models import Transaction
from ..forms import TransactionForm
from django.db.models import Q
from django.core.paginator import Paginator

def transaction_list(request):
    status = request.GET.get("status")   # filter
    q = request.GET.get("q")             # search input
    page_number = request.GET.get("page")  # pagination

    transactions = Transaction.objects.select_related(
        "book", "borrower"
    ).order_by("-date_borrowed")

    # ✅ Status filter
    if status:
        transactions = transactions.filter(status=status)

    # ✅ Search filter (book title OR borrower name)
    if q:
        transactions = transactions.filter(
            Q(book__title__icontains=q) |
            Q(borrower__first_name__icontains=q) |
            Q(borrower__last_name__icontains=q)
        )

    # ✅ Pagination: 10 transactions per page
    paginator = Paginator(transactions, 10)
    page_obj = paginator.get_page(page_number)

    return render(request, "app2/transactions/transaction_list.html", {
        "transactions": page_obj.object_list,  # only transactions for this page
        "page_obj": page_obj,                  # page object for pagination controls
        "active_status": status,
        "search_query": q,                     # send back to input
    })

# CREATE
def transaction_create(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("transaction_list")
    else:
        form = TransactionForm()

    return render(request, "app2/transactions/transaction_form.html", {"form": form, "title": "Add Transaction"})


# UPDATE
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect("transaction_list")
    else:
        form = TransactionForm(instance=transaction)

    return render(request, "app2/transactions/transaction_form.html", {"form": form, "title": "Edit Transaction"})


# DELETE
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    if request.method == "POST":
        transaction.delete()
        return redirect("transaction_list")

    return render(request, "app2/transactions/transaction_confirm_delete.html", {"transaction": transaction})


def borrower_transactions(request, borrower_id):
    transactions = Transaction.objects.select_related(
        "book", "borrower"
    ).filter(
        borrower_id=borrower_id
    ).order_by("-date_borrowed")

    return render(
        request,
        "app2/transactions/transaction_list.html",
        {
            "transactions": transactions,
            "borrower_id": borrower_id,
        }
    )
