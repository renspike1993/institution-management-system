# apps.app3/admin.py
from django.contrib import admin
from .models import Collection, Book, BookBarcode, Transaction
from django.contrib.auth.models import Permission

# ✅ Collection Admin
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('name',)

# ✅ Book Admin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'publication_year', 'classification', 'collection')
    search_fields = ('title', 'author', 'isbn', 'subjects')
    list_filter = ('publication_year', 'language', 'classification', 'collection')
    ordering = ('title',)

# ✅ BookBarcode Admin
@admin.register(BookBarcode)
class BookBarcodeAdmin(admin.ModelAdmin):
    list_display = ('barcode', 'book', 'created_at')
    search_fields = ('barcode', 'book__title')
    list_filter = ('book',)
    ordering = ('book', 'barcode')

# ✅ Transaction Admin
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('book', 'borrower', 'barcode', 'status', 'date_reserve', 'date_borrowed', 'due_date', 'date_returned')
    search_fields = ('book__title', 'borrower__username', 'barcode__barcode')
    list_filter = ('status', 'due_date', 'date_returned')
    ordering = ('-date_reserve',)

# ✅ Permission Admin (optional, if you want to manage permissions)
@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("name", "codename", "content_type")
    search_fields = ("name", "codename")
    list_filter = ("content_type",)
    
    
admin.site.index_title = "Welcome Administrator's Page"
# Change the main header
admin.site.site_header = "Administrator"

# Change the title shown in the browser tab
admin.site.site_title = "Library Admin Portal"