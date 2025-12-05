from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from datetime import timedelta
from django.utils import timezone

from apps.app1.models import Student,Profile
from ..models import Book,BookBarcode,Collection
from ..forms import BookForm,CollectionForm
from django.contrib import messages
from django.db.models import Prefetch
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q,Count
from django.http import JsonResponse
import json
from django.contrib.auth.models import Group,Permission



# def group_list(request):
#     groups = Group.objects.all()
#     return render(request, "app1/groups/group_list.html", {"groups": groups})



# def group_permissions(request, pk):
#     group = get_object_or_404(Group, id=pk)
#     permissions = Permission.objects.all()

#     return render(request, "app1/groups/group_permissions.html", {
#         "group": group,
#         "permissions": permissions
#     })


from django.contrib.contenttypes.models import ContentType

def group_list(request):
    groups = Group.objects.all()
    return render(request, "app1/groups/group_list.html", {"groups": groups})


def group_permissions(request, pk):
    group = get_object_or_404(Group, id=pk)

    # Get all permissions for app2 only
    app2_content_types = ContentType.objects.filter(app_label='app2')
    permissions = Permission.objects.filter(content_type__in=app2_content_types)

    return render(request, "app1/groups/group_permissions.html", {
        "group": group,
        "permissions": permissions
    })
from django.views.decorators.http import require_POST

@require_POST
def toggle_permission(request):
    group_id = request.POST.get("group_id")
    perm_id = request.POST.get("perm_id")

    group = Group.objects.get(id=group_id)
    permission = Permission.objects.get(id=perm_id)

    if permission in group.permissions.all():
        group.permissions.remove(permission)
        status = "removed"
    else:
        group.permissions.add(permission)
        status = "added"

    return JsonResponse({"status": status})



def ads(request):
    # ✅ 1. Featured books for TV carousel (random with covers)
    featured_books = Book.objects.exclude(
        cover_image=""
    ).order_by("?")[:6]

    # ✅ 2. New Arrivals (latest 10 books)
    new_arrivals = Book.objects.order_by("-created_at")[:10]

    # ✅ 3. Top 10 Most Borrowed Books (based on Transaction history)
    most_borrowed_books = Book.objects.annotate(
        borrow_count=Count(
            "transactions",
            filter=Q(transactions__date_borrowed__isnull=False)
        )
    ).order_by("-borrow_count")[:10]

    # ✅ 4. Top 3 Collections with most books
    top_collections = Collection.objects.annotate(
        book_count=Count("books")
    ).order_by("-book_count")[:3]

    context = {
        "featured_books": featured_books,
        "new_arrivals": new_arrivals,
        "most_borrowed_books": most_borrowed_books,
        "top_collections": top_collections,
    }

    return render(request, "app2/tv.html", context)



def manual(request):
    return render(request, 'app2/manual.html')


def book_views(request):
    return render(request, 'app2/view.html')



# @csrf_exempt   # optional if you use X-CSRFToken (safe to remove once stable)
# def api_reservations(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body.decode("utf-8"))
#             print("📌 Received Reservation:", data)

#             return JsonResponse({
#                 "status": "success",
#                 "received": data
#             })

#         except Exception as e:
#             print("⚠ Error:", e)
#             return JsonResponse({"error": str(e)}, status=400)

#     return JsonResponse({"error": "POST only"}, status=405)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import Transaction, Book, Student
import json
from django.utils.dateparse import parse_datetime
from django.contrib.auth.models import User
@csrf_exempt
def api_reservations(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        print("📌 Received Reservation:", data)

        user_id = data.get("userId")
        books = data.get("books", [])
        reservation_date_str = data.get("reservationDate")

        if not user_id or not books:
            return JsonResponse({"error": "Missing userId or books"}, status=400)

        # Ensure user exists
        try:
            borrower = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        # Parse reservation date if provided
        reservation_date = parse_datetime(reservation_date_str) if reservation_date_str else None

        created_transactions = []

        # Ensure all books exist first
        for book_data in books:
            book_id = book_data.get("id")
            if not book_id:
                return JsonResponse({"error": f"Book id missing in {book_data}"}, status=400)
            try:
                book_obj = Book.objects.get(id=book_id)
            except Book.DoesNotExist:
                return JsonResponse({"error": f"Book id {book_id} not found"}, status=404)

            # Create transaction
            transaction = Transaction.objects.create(
                book=book_obj,
                borrower=borrower,
                date_reserve=reservation_date,
                status="reserved"
            )
            created_transactions.append(transaction.id)

        return JsonResponse({
            "status": "success",
            "created_transactions": created_transactions
        })

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        print("⚠ Error:", e)
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def dashboard(request):
    # Total counts
    total_books = Book.objects.count()
    total_barcodes = BookBarcode.objects.count()
    total_collections = Collection.objects.count()
    total_students = Student.objects.count()

    # Borrowed stats
    borrowed_count = Transaction.objects.filter(status="borrowed").count()
    returned_count = Transaction.objects.filter(status="returned").count()
    overdue_count = Transaction.objects.filter(status="overdue").count()
    damaged_count = Transaction.objects.filter(status="damaged").count()  # New

    # Recently added books
    new_arrivals = Book.objects.order_by('-created_at')[:5]

    # Recently borrowed books
    borrowed_transactions = Transaction.objects.select_related(
        'book', 'borrower', 'barcode'
    ).order_by('-date_borrowed')[:5]

    context = {
        'total_books': total_books,
        'total_barcodes': total_barcodes,
        'total_collections': total_collections,
        'total_students': total_students,
        'borrowed_count': borrowed_count,
        'returned_count': returned_count,
        'overdue_count': overdue_count,
        'damaged_count': damaged_count,  # Include in context
        'new_arrivals': new_arrivals,
        'borrowed_transactions': borrowed_transactions,
    }

    return render(request, 'app2/dashboard.html', context)

@login_required
def book_marc21_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    # Prepare a list of (field name, value) to send to template
    book_fields = []
    for field in book._meta.fields:
        book_fields.append((field.verbose_name, getattr(book, field.name)))
    
    return render(request, 'app2/marc-21-view.html', {
        'book': book,
        'book_fields': book_fields
    })

@login_required
def book_isbd(request, pk):
    book = get_object_or_404(Book, pk=pk)

    # Construct ISBD string
    isbd_parts = []

    # Title / statement of responsibility
    title_part = book.title
    if book.subtitle:
        title_part += f" : {book.subtitle}"
    if book.statement_of_responsibility:
        title_part += f" / {book.statement_of_responsibility}"
    isbd_parts.append(title_part)

    # Author
    if book.author:
        isbd_parts.append(f"{book.author}")

    # Edition
    if book.edition:
        isbd_parts.append(f"{book.edition} edition")

    # Publication
    pub_parts = []
    if book.publication_place:
        pub_parts.append(book.publication_place)
    if book.publisher:
        pub_parts.append(book.publisher)
    if book.publication_year:
        pub_parts.append(book.publication_year)
    if pub_parts:
        isbd_parts.append(" : ".join(pub_parts))

    # Pagination / illustrations / dimensions
    page_parts = []
    if book.pages:
        page_parts.append(f"{book.pages} p.")
    if book.illustrations:
        page_parts.append(f"{book.illustrations}")
    if book.dimensions:
        page_parts.append(f"{book.dimensions}")
    if page_parts:
        isbd_parts.append(" ; ".join(page_parts))

    # Series
    if book.series:
        isbd_parts.append(f"Series: {book.series}")

    # Notes
    if book.notes:
        isbd_parts.append(f"Notes: {book.notes}")

    # Subjects
    if book.subjects:
        isbd_parts.append(f"Subjects: {book.subjects}")

    # Classification
    if book.classification:
        isbd_parts.append(f"Classification: {book.classification}")

    # Language
    if book.language:
        isbd_parts.append(f"Language: {book.language}")

    # Combine into single ISBD string with line breaks
    isbd_string = "\n".join(isbd_parts)

    context = {
        'book': book,
        'book_isbd': isbd_string,
    }

    return render(request, 'app2/book/book_isbd.html', context)


@login_required
def index(request):
    return render(request, 'app2/index.html')

from django.utils.html import escape
import re


def opac(request):
    query = request.GET.get('q', '').strip()
    books_list = Book.objects.all()

    if query:
        # Split the query into words
        terms = query.split()

        # Filter books normally
        for term in terms:
            books_list = books_list.filter(
                Q(title__icontains=term) |
                Q(author__icontains=term) |
                Q(subjects__icontains=term) |
                Q(summary__icontains=term) |
                Q(barcodes__barcode__icontains=term)
            ).distinct()

        # Highlight matched terms in each book (case-insensitive)
        highlighted_books = []
        for book in books_list:
            book.title = escape(book.title)
            book.author = escape(book.author)
            book.summary = escape(book.summary or "")

            for term in terms:
                pattern = re.compile(re.escape(term), re.IGNORECASE)
                highlight_term = r'<span style="background-color: yellow;">\g<0></span>'
                book.title = pattern.sub(highlight_term, book.title)
                book.author = pattern.sub(highlight_term, book.author)
                book.summary = pattern.sub(highlight_term, book.summary)

            highlighted_books.append(book)
        books_list = highlighted_books

    paginator = Paginator(books_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'app2/opac.html', {
        'books': page_obj,
        'page_obj': page_obj,
        'search_query': query
    })
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required

@login_required
def book_list(request):
    search = request.GET.get('search', '').strip()

    books = Book.objects.annotate(
        borrowed_total=Count(
            'transactions',
            filter=Q(transactions__status="borrowed")
        )
    ).prefetch_related("barcodes")

    # ✅ SEARCH FILTER
    if search:
        books = books.filter(
            Q(title__icontains=search) |
            Q(author__icontains=search) |
            Q(control_number__icontains=search) |
            Q(isbn__icontains=search)
        )

    # ✅ PAGINATION (10 per page)
    paginator = Paginator(books, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'app2/book/book_list.html', {
        'books': page_obj,
        'search': search
    })

# View book details
@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    barcodes = book.barcodes.all()
    barcode_data = []

    for bc in barcodes:
        # Get the latest transaction for this barcode that is not returned
        transaction = (
            Transaction.objects.filter(barcode=bc)
            .exclude(status="returned")
            .select_related("borrower")
            .order_by("-id")
            .first()
        )

        if transaction:
            status = transaction.status.capitalize()
            borrower = transaction.borrower  # This is now a User object
        else:
            status = "Available"
            borrower = None

        barcode_data.append({
            "barcode": bc,
            "status": status,
            "borrower": borrower,
            "transaction": transaction,
        })

    context = {
        "book": book,
        "barcode_data": barcode_data,
    }

    return render(request, "app2/book/book_detail.html", context)


@login_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Book has been successfully added!")  # <-- success message
            return redirect('book_list')
        else:
            messages.error(request, "Please correct the errors below.")  # <-- optional error message
    else:
        form = BookForm()
    return render(request, 'app2/book/book_form.html', {'form': form})


@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)  # <-- add request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, "Book has been successfully updated!")  # <-- success message
            return redirect('book_list')
        else:
            messages.error(request, "Please correct the errors below.")  # <-- optional error message
    else:
        form = BookForm(instance=book)
    return render(request, 'app2/book/book_form.html', {'form': form})


# Delete a book
@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    return render(request, 'app2/book/book_confirm_delete.html', {'book': book})


@login_required
def borrow_book_list(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    # Search query
    q = request.GET.get("q", "").strip().upper()

    # Step 1: Get all barcodes that are currently borrowed
    borrowed_barcodes = Transaction.objects.filter(status="borrowed").values_list("barcode_id", flat=True)

    # Step 2: Get books with at least one available barcode
    books = Book.objects.prefetch_related("barcodes").filter(
        barcodes__id__isnull=False  # Make sure book has barcodes
    ).exclude(
        barcodes__id__in=borrowed_barcodes  # Exclude borrowed barcodes
    ).distinct()

    # Step 3: Filter by search query if provided
    if q:
        books = books.filter(barcodes__barcode__iexact=q).distinct()

    # Pagination
    paginator = Paginator(books, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Prepare a set of borrowed barcodes for this student (optional, for UI purposes)
    student_borrowed_barcodes = set(
        Transaction.objects.filter(
            borrower=student,
            status="borrowed"
        ).values_list("barcode_id", flat=True)
    )

    context = {
        "student": student,
        "page_obj": page_obj,
        "borrowed_barcodes": student_borrowed_barcodes,
        "q": q,
    }
    return render(request, "app2/book/borrow_book_list.html", context)


@login_required
def all_books_borrow_history(request):
    status_filter = request.GET.get('status', '')  # 'borrowed', 'returned', 'overdue' or ''
    search_query = request.GET.get('q', '').strip()

    # Base queryset BorrowedBook
    borrow_records = Transaction.objects.select_related(
        'book', 'borrower', 'barcode'
    ).order_by('-date_borrowed')

    # Apply status filter if provided
    if status_filter in ['borrowed', 'returned', 'overdue']:
        borrow_records = borrow_records.filter(status=status_filter)

    # Apply search filter if provided
    if search_query:
        borrow_records = borrow_records.filter(
            Q(book__title__icontains=search_query) |
            Q(book__author__icontains=search_query) |
            Q(barcode__barcode__icontains=search_query) |
            Q(borrower__first_name__icontains=search_query) |
            Q(borrower__last_name__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(borrow_records, 10)  # 15 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'borrow_records': page_obj,
        'status_filter': status_filter,
        'q': search_query,
        'page_obj': page_obj,
    }
    return render(request, 'app2/book/all_books_borrow_history.html', context)


@login_required
def borrow_book(request, student_id, book_id, barcode_id):
    student = get_object_or_404(Student, pk=student_id)
    book = get_object_or_404(Book, pk=book_id)
    barcode = get_object_or_404(BookBarcode, pk=barcode_id)

    # Create BorrowedBook record
    Transaction.objects.create(
        borrower=student,
        book=book,
        barcode=barcode,
        due_date=timezone.now().date() + timedelta(days=3)  # 7-day borrowing period
    )

    messages.success(request, f"{book.title} ({barcode.barcode}) borrowed successfully!")
    return redirect('borrow_book_list', student_id=student.id)


@login_required
def return_book(request, borrowed_id):
    borrowed = get_object_or_404(Transaction, pk=borrowed_id)

    if borrowed.status == 'borrowed':
        borrowed.status = 'returned'
        borrowed.date_returned = timezone.now()
        borrowed.save()
        messages.success(request, f"{borrowed.book.title} has been returned successfully.")
    else:
        messages.warning(request, f"{borrowed.book.title} was already returned.")

    # Redirect back to the previous page, fallback to home if not available
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def bookbarcode_create(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        barcode_value = request.POST.get("barcode")

        if not barcode_value:
            messages.error(request, "Barcode is required.")
            return redirect("bookbarcode_create", pk=pk)

        # Prevent duplicate barcode
        if BookBarcode.objects.filter(barcode=barcode_value).exists():
            messages.error(request, "This barcode already exists!")
            return redirect("bookbarcode_create", pk=pk)

        BookBarcode.objects.create(book=book, barcode=barcode_value)
        messages.success(request, "Barcode added successfully!")
        return redirect("book_detail", pk=pk)

    return render(request, "app2/book/bookbarcode_form.html", {"book": book})



@login_required
def bookbarcode_delete(request, book_id, barcode_id):
    # Get the book and barcode (404 if not found)
    book = get_object_or_404(Book, pk=book_id)
    barcode = get_object_or_404(BookBarcode, pk=barcode_id, book=book)

    # Delete the barcode
    barcode.delete()
    messages.success(request, f"Barcode {barcode.barcode} was deleted successfully.")

    # Return to book detail page
    return redirect("book_detail", pk=book_id)
# ----------------------------------------------------------------------------------

# @login_required
# def security_logs(request):
#     return render(request, 'app2/logs.html')

from apps.controller_gates.models import TurnstileAttendanceLog  # adjust path if needed

@login_required
def security_logs(request):
    logs = TurnstileAttendanceLog.objects.all()[:10]  # last 10 logs
    return render(request, 'app2/logs.html', {'logs': logs})

# -------------------------------

@login_required
def all_borrowed_books(request):
    q = request.GET.get("q", "").strip()

    borrowed = Transaction.objects.select_related("borrower", "book", "barcode")

    if q:
        borrowed = borrowed.filter(
            Q(book__title__icontains=q) |
            Q(book__author__icontains=q) |
            Q(barcode__barcode__icontains=q) |
            Q(borrower__first_name__icontains=q) |
            Q(borrower__last_name__icontains=q)
        )

    paginator = Paginator(borrowed.order_by("-date_borrowed"), 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "q": q}
    return render(request, "app2/book/borrowed_all_list.html", context)


from apps.controller_gates.models import TurnstileAttendanceLog


from apps.app2.models import BookBarcode, Transaction
from apps.app1.models import Profile


@login_required
def api_check_book_status(request, barcode):
    try:
        barcode_obj = BookBarcode.objects.select_related("book").get(barcode=barcode)

        is_user = Profile.objects.filter(barcode=barcode).select_related("user").first()
        is_book = BookBarcode.objects.filter(barcode=barcode).first()

        transaction = (
            Transaction.objects.filter(barcode=barcode_obj)
            .exclude(status="returned")
            .select_related("borrower")
            .order_by("-id")
            .first()
        )

        object_type = ""
        object_name = ""
        object_pic = None

        # ==========================
        # ✅ USER SCAN (TURNSTILE IN)
        # ==========================
        if is_user:
            try:
                object_type = "user"
                object_name = f"{is_user.user.last_name}, {is_user.user.first_name}"
                object_pic = is_user.avatar.url if is_user.avatar else None
                status = "AUTHORIZED"
            except:
                object_pic = None
                status = "UNAUTHORIZED"

            # ✅ SAVE TO TURNSTILE LOGS
            TurnstileAttendanceLog.objects.create(
                person_id=is_user.barcode,
                full_name=object_name,
                gate_name="Library Gate",
                direction="IN",
                status=status,
                timestamp=timezone.now(),
                remarks="RFID User Scan"
            )

            return JsonResponse({
                "identity_type": object_type,
                "status": "none",
                "book_title": object_name,
                "profile_pic": object_pic,
            })

        # ==========================
        # ✅ BOOK SCAN
        # ==========================
        if is_book:
            object_type = "book"
            object_name = barcode_obj.book.title

            can_be_check_out = bool(
                transaction and
                transaction.status.lower() == "borrowed" and
                transaction.date_borrowed
            )

            # ✅ SAVE TO TURNSTILE LOGS (BOOK ACTIVITY)
            TurnstileAttendanceLog.objects.create(
                person_id=barcode,
                full_name=object_name,
                gate_name="Library Gate",
                direction="IN",
                status="AUTHORIZED" if can_be_check_out else "UNAUTHORIZED",
                timestamp=timezone.now(),
                remarks="Book Scan"
            )

            return JsonResponse({
                "identity_type": object_type,
                "status": "available",
                "can_be_check_out": can_be_check_out,
                "book_title": object_name,
                "profile_pic": None,
            })

        # ==========================
        # ❌ NOT FOUND
        # ==========================
        TurnstileAttendanceLog.objects.create(
            person_id=barcode,
            full_name="UNKNOWN",
            gate_name="Main Gate",
            direction="IN",
            status="UNAUTHORIZED",
            timestamp=timezone.now(),
            remarks="Unregistered Barcode"
        )

        return JsonResponse({
            "identity_type": "not_found",
            "status": "not_found",
            "book_title": None,
            "profile_pic": None,
        })

    except BookBarcode.DoesNotExist:

        # ✅ STILL LOG UNKNOWN SCAN
        TurnstileAttendanceLog.objects.create(
            person_id=barcode,
            full_name="UNKNOWN",
            gate_name="Main Gate",
            direction="IN",
            status="UNAUTHORIZED",
            timestamp=timezone.now(),
            remarks="Barcode Not Found in System"
        )

        return JsonResponse({"status": "not_found"})    


# -------------------------------Collection------------------------------------------------

# LIST COLLECTIONS WITH BOOK COUNT
def collection_list(request):
    collections = Collection.objects.annotate(
        book_count=Count('books')  # 'books' is the related_name from Book.collection
    ).order_by('-id')
    
    return render(request, 'app2/collection/collection_list.html', {'collections': collections})

# CREATE COLLECTION
def collection_create(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('collection_list')
    else:
        form = CollectionForm()
    return render(request, 'app2/collection/collection_form.html', {'form': form})

# UPDATE COLLECTION
def collection_update(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    if request.method == 'POST':
        form = CollectionForm(request.POST, instance=collection)
        if form.is_valid():
            form.save()
            return redirect('collection_list')
    else:
        form = CollectionForm(instance=collection)
    return render(request, 'app2/collection/collection_form.html', {'form': form})

# DELETE COLLECTION
def collection_delete(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    if request.method == 'POST':
        collection.delete()
        return redirect('collection_list')
    return render(request, 'app2/collection/collection_confirm_delete.html', {'collection': collection})

# VIEW COLLECTION DETAILS
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    return render(request, 'app2/collection/collection_detail.html', {'collection': collection})

import random
from faker import Faker

from django.http import HttpResponse


@login_required
def generate_fake_books_view(request):
    n = request.GET.get('n', 10)  # default to 10 books
    try:
        n = int(n)
    except ValueError:
        return HttpResponse("Invalid number of books", status=400)

    fake = Faker()

    for _ in range(n):
        title = fake.sentence(nb_words=4)
        author = fake.name()
        publication_year = str(random.randint(1950, 2023))
        isbn = fake.isbn13(separator="-")
        summary = fake.paragraph(nb_sentences=3)
        # Generate a unique control number
        control_number = fake.unique.random_number(digits=8, fix_len=True)

        Book.objects.create(
            control_number=control_number,
            title=title,
            author=author,
            publication_year=publication_year,
            isbn=isbn,
            summary=summary
        )

    return HttpResponse(f"Created {n} fake books successfully!")


def importer(request):
    return render(request, 'app2/importer.html' )

