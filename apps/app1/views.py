from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect, get_object_or_404
from .models import Student,Folder
from .forms import StudentForm, UserForm
from django.contrib import messages
from apps.app2.models import Transaction
from django.contrib.auth.models import User


from .forms import FolderForm

@login_required
def index(request):
    return render(request, 'app1/index.html')


# READ (LIST)
@login_required
def student_list(request):
    students = Student.objects.all().order_by("last_name")
    return render(request, "app1/student/student_list.html", {"students": students})

@login_required
def student_detail(request, pk):
    # Get the student
    student = get_object_or_404(Student, pk=pk)
    
    # Get transactions for the associated user
    transactions = Transaction.objects.select_related(
        "book", "borrower"
    ).filter(
        borrower=student.user
    ).order_by("-date_borrowed")
    
    return render(request, "app1/student/student_detail.html", {
        "student": student,
        "transactions": transactions,
    })

@login_required  # Optional: remove if anyone can create users
def create_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Hash the password
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, f"User {user.username} created successfully.")
            return redirect("user_list")  # change to your desired route
    else:
        form = UserForm()

    return render(request, "app1/user_form.html", {"form": form, "title": "Create User"})

# CREATE STUDENT AND USER
@login_required
def student_create(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        student_form = StudentForm(request.POST)

        if user_form.is_valid() and student_form.is_valid():
            # Save User first
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])  # Hash password
            user.save()

            # Save Student and assign user
            student = student_form.save(commit=False)
            student.user = user
            student.save()

            messages.success(request, "Student and user created successfully!")
            return redirect("student_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserForm()
        student_form = StudentForm()

    context = {
        "user_form": user_form,
        "student_form": student_form,
        "title": "Add Student",
    }
    return render(request, "app1/student/student_form.html", context)
# UPDATE
@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("student_list")  # corrected
    else:
        form = StudentForm(instance=student)
    return render(request, "app1/student/student_form.html", {"form": form, "title": "Edit Student"})

# DELETE
@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        return redirect("student_list")
    return render(request, "app1/student/student_confirm_delete.html", {"student": student})

# --------------------- Folders -----------------------------------
@login_required
def folder_list(request):
    folders = Folder.objects.all().order_by('-created_at')
    return render(request, 'app1/folder/folder_list.html', {'folders': folders})

@login_required
def folder_create(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.created_by = request.user
            folder.save()
            messages.success(request, 'Folder created successfully!')
            return redirect('folder_list')
    else:
        form = FolderForm()
    return render(request, 'app1/folder/folder_form.html', {'form': form, 'title': 'Add Folder'})

@login_required
def folder_update(request, pk):
    folder = get_object_or_404(Folder, pk=pk)
    if request.method == 'POST':
        form = FolderForm(request.POST, instance=folder)
        if form.is_valid():
            form.save()
            messages.success(request, 'Folder updated successfully!')
            return redirect('folder_list')
    else:
        form = FolderForm(instance=folder)
    return render(request, 'app1/folder/folder_form.html', {'form': form, 'title': 'Edit Folder'})

@login_required
def folder_delete(request, pk):
    folder = get_object_or_404(Folder, pk=pk)
    if request.method == 'POST':
        folder.delete()
        messages.success(request, 'Folder deleted successfully!')
        return redirect('folder_list')
    return render(request, 'app1/folder/folder_confirm_delete.html', {'folder': folder})



from .forms import UserForm

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, "app1/users/user_list.html", {"users": users})

@login_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    # Fetch transactions for this user
    transactions = Transaction.objects.select_related('book').filter(borrower=user).order_by('-date_borrowed')
    
    return render(request, "app1/users/user_detail.html", {
        "user_obj": user,
        "transactions": transactions
    })

@login_required
def create_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, f"User {user.username} created successfully.")
            return redirect("user_list")
    else:
        form = UserForm()
    return render(request, "app1/users/user_form.html", {"form": form, "title": "Create User"})

@login_required
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, f"User {user.username} updated successfully.")
            return redirect("user_list")
    else:
        form = UserForm(instance=user)
    return render(request, "app1/users/user_form.html", {"form": form, "title": "Update User"})

@login_required
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.delete()
        messages.success(request, f"User {user.username} deleted successfully.")
        return redirect("user_list")
    return render(request, "app1/users/user_confirm_delete.html", {"user": user})