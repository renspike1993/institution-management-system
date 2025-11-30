# apps.app3/forms.py
from django import forms
from .models import Book,Collection,Transaction,BookBarcode

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'control_number': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Control Number'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'ISBN'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Title'
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Subtitle'
            }),
            'statement_of_responsibility': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Statement of Responsibility'
            }),
            'author': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Main Author'
            }),
            'added_authors': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Added Authors'
            }),
            'edition': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Edition'
            }),
            'publisher': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Publisher'
            }),
            'publication_place': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Place of Publication'
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Year',
                'min': 1000,
                'max': 9999
            }),
            'pages': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Pages'
            }),
            'illustrations': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Illustrations'
            }),
            'dimensions': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Dimensions'
            }),
            'series': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Series'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 resize-none',
                'placeholder': 'General Notes',
                'rows': 2
            }),
            'summary': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 resize-none',
                'placeholder': 'Summary',
                'rows': 2
            }),
            'subjects': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Subjects'
            }),
            'classification': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Dewey / Local'
            }),
            'language': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Language'
            }),
            'cover': forms.ClearableFileInput(attrs={
                'class': 'w-full text-sm text-gray-700 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500'
            }),
        }


        
class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500 text-sm',
                'placeholder': 'Collection Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500 text-sm',
                'placeholder': 'Collection Description',
                'rows': 3
            }),
        }



class TransactionForm(forms.ModelForm):

    barcode = forms.ModelChoiceField(
        queryset=BookBarcode.objects.none(),  # set dynamically
        required=False,
        widget=forms.Select(attrs={
            'class': 'border rounded px-2 py-1 w-full',
        })
    )

    class Meta:
        model = Transaction
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ Get barcodes that are currently borrowed
        borrowed_barcodes = Transaction.objects.filter(
            status="borrowed"
        ).values_list("barcode_id", flat=True)

        # ✅ Display "(Not available)" text
        self.fields["barcode"].label_from_instance = lambda obj: (
            f"{obj} (Not available)" if obj.id in borrowed_barcodes else str(obj)
        )

        # ✅ ADD MODE → Show only AVAILABLE barcodes
        if not self.instance.pk:
            self.fields["barcode"].queryset = BookBarcode.objects.exclude(
                id__in=borrowed_barcodes
            )

        # ✅ EDIT MODE
        else:
            # Lock fields on edit
            self.fields["borrower"].disabled = True
            self.fields["borrower"].disabled = True
            self.fields["date_borrowed"].disabled = True
            self.fields["due_date"].disabled = True
            self.fields["date_returned"].disabled = True
            self.fields["book"].disabled = True

            # ✅ Show only barcodes for the same book
            if self.instance.book:
                self.fields["barcode"].queryset = BookBarcode.objects.filter(
                    book=self.instance.book
                )
            else:
                self.fields["barcode"].queryset = BookBarcode.objects.none()
