# apps.app3/models.py
from django.db import models
from apps.app1.models import Student   # adjust path if needed
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

class Collection(models.Model):
    name = models.CharField(max_length=100, unique=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    collection = models.ForeignKey(
        Collection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books"
    )

    control_number = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Control Number / 001"
    )

    isbn = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="ISBN / 020"
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Title / 245$a"
    )

    subtitle = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Subtitle / 245$b"
    )

    statement_of_responsibility = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Statement of Responsibility / 245$c"
    )

    author = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Main Author / 100$a"
    )

    added_authors = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Added Authors / 700$a"
    )

    edition = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Edition / 250"
    )

    publisher = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Publisher / 264$b"
    )

    publication_place = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Place / 264$a"
    )

    publication_year = models.CharField(
        max_length=4,
        blank=True,
        null=True,
        verbose_name="Year / 264$c"
    )

    pages = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Pagination / 300$a"
    )

    illustrations = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Illustrations / 300$b"
    )

    dimensions = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Dimensions / 300$c"
    )

    series = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Series / 490$a"
    )

    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="General Notes / 500"
    )

    summary = models.TextField(
        blank=True,
        null=True,
        verbose_name="Summary / 520"
    )

    subjects = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Subjects / 650$a"
    )

    classification = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Dewey / 082 or Local / 090"
    )

    language = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Language / 041$a"
    )

    cover_image = models.ImageField(
        upload_to='book_covers/',
        blank=True,
        null=True,
        verbose_name="Book Cover"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.title or 'Untitled'} by {self.author or 'Unknown'} ({self.publication_year or 'N/A'})"



class BookBarcode(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name="barcodes")
    barcode = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.barcode} - {self.book.title}"



def default_due_date():
    return timezone.now().date() + timedelta(days=3)

class Transaction(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name="transactions")
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    barcode = models.ForeignKey('BookBarcode', on_delete=models.CASCADE, related_name="transactions", null=True, blank=True)

    date_reserve = models.DateTimeField(auto_now_add=True)
    date_borrowed = models.DateTimeField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    date_returned = models.DateField(blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)

    STATUS_CHOICES = [
        ("reserved", "Reserved"),
        ("borrowed", "Borrowed"),
        ("returned", "Returned"),
        ("overdue", "Overdue"),
        ("damaged", "Damaged"),
        ("lost", "Lost"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="reserved")

    def save(self, *args, **kwargs):
        if self.status == "borrowed":
            if not self.date_borrowed:
                self.date_borrowed = timezone.now()
            if not self.due_date:
                self.due_date = timezone.now().date() + timedelta(days=3)
        if self.status == "returned" and not self.date_returned:
            self.date_returned = timezone.now().date()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.borrower.username}"

    class Meta:
        ordering = ['-date_reserve']