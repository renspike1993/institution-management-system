from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect, get_object_or_404
from .models import Student,Folder,Profile,Department
from .forms import StudentForm, UserForm
from django.contrib import messages
from apps.app2.models import Transaction
from django.contrib.auth.models import User


from .forms import FolderForm, DepartmentForm, ProfileForm

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

import csv, io

@login_required
def import_users_csv(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]

        # ✅ Validate CSV extension
        if not csv_file.name.endswith(".csv"):
            messages.error(request, "Invalid file type. Please upload a CSV file.")
            return redirect("import_users")

        try:
            data = csv_file.read().decode("utf-8")
            io_string = io.StringIO(data)
            reader = csv.DictReader(io_string)

            created_count = 0
            skipped_count = 0

            for row in reader:
                school_id = row["school_id"].strip()
                lname = row["lname"].strip()
                fname = row["fname"].strip()
                midname = row["midname"].strip()
                extname = row["extname"].strip()
                sex = row["sex"].strip()
                course = row["course"].strip()
                year = row["year"].strip()
                major = row["major"].strip()
                email = row["email"].strip()
                student_id = row["student_id"].strip()

                username = student_id  # ✅ use student_id as username
                password = student_id  # ✅ default password

                if User.objects.filter(username=username).exists():
                    skipped_count += 1
                    continue

                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=fname,
                    last_name=lname
                )

                # ✅ OPTIONAL: If you have a Student Profile model
                # StudentProfile.objects.create(
                #     user=user,
                #     school_id=school_id,
                #     midname=midname,
                #     extname=extname,
                #     sex=sex,
                #     course=course,
                #     year=year,
                #     major=major,
                # )

                created_count += 1

            messages.success(
                request,
                f"✅ Import completed: {created_count} created, {skipped_count} skipped."
            )
            return redirect("user_list")

        except Exception as e:
            messages.error(request, f"CSV Import Error: {str(e)}")
            return redirect("import_users")

    return render(request, "app1/users/import_users.html")


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
from django.db.models import Q
from django.core.paginator import Paginator

@login_required
def user_list(request):
    search_query = request.GET.get("search", "")

    user_list = User.objects.all()

    # ✅ SEARCH FILTER
    if search_query:
        user_list = user_list.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    user_list = user_list.order_by("id")

    # ✅ PAGINATION
    paginator = Paginator(user_list, 15)  # 10 per page
    page_number = request.GET.get("page")
    users = paginator.get_page(page_number)

    return render(request, "app1/users/user_list.html", {
        "users": users,
        "search_query": search_query
    })

def user_detail(request, pk):
    user_obj = get_object_or_404(User, pk=pk)

    profile = Profile.objects.filter(user=user_obj).first()  # ✅ Safe fetch
    transactions = user_obj.transaction_set.all()  # adjust if your related_name is different

    return render(request, "app1/users/user_detail.html", {
        "user_obj": user_obj,
        "profile": profile,
        "transactions": transactions
    })
    
    
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
    
    # Ensure profile exists
    profile, created = Profile.objects.get_or_create(user=user)
    
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            if user_form.cleaned_data['password']:
                user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile_form.save()
            
            messages.success(request, f"User {user.username} updated successfully.")
            return redirect("user_list")
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': f"Edit User: {user.username}"
    }
    
    return render(request, "app1/users/user_edit.html", context)
@login_required
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.delete()
        messages.success(request, f"User {user.username} deleted successfully.")
        return redirect("user_list")
    return render(request, "app1/users/user_confirm_delete.html", {"user": user})


# -------------------------------- Departments --------------------------------
from .models import Department
from .forms import DepartmentForm

@login_required
def department_list(request):
    departments = Department.objects.all().order_by('name')
    return render(request, 'app1/department/department_list.html', {'departments': departments})

@login_required
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department created successfully!")
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'app1/department/department_form.html', {'form': form, 'title': 'Add Department'})

@login_required
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully!")
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'app1/department/department_form.html', {'form': form, 'title': 'Edit Department'})

@login_required
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        messages.success(request, "Department deleted successfully!")
        return redirect('department_list')
    return render(request, 'app1/department/department_confirm_delete.html', {'department': department})
