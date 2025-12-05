from django.urls import path
from . import views




urlpatterns = [
    path('', views.student_list, name='registrar'),
    
    
    path("students/", views.student_list, name="student_list"),
    path("students/create/", views.student_create, name="student_create"),
    path("students/<int:pk>/", views.student_detail, name="student_detail"),   # 👈 ADD THIS
    path("students/<int:pk>/edit/", views.student_update, name="student_update"),
    path("students/<int:pk>/delete/", views.student_delete, name="student_delete"),

    path("users/", views.user_list, name="user_list"),
    path("users/<int:pk>/", views.user_detail, name="user_detail"),
    path("users/create/", views.create_user, name="create_user"),
    path("users/<int:pk>/update/", views.update_user, name="update_user"),
    path("users/<int:pk>/delete/", views.delete_user, name="delete_user"),

    path("departments/", views.department_list, name="department_list"),
    path("departments/create/", views.department_create, name="department_create"),
    path("departments/<int:pk>/update/", views.department_update, name="department_update"),
    path("departments/<int:pk>/delete/", views.department_delete, name="department_delete"),


    path('folders/', views.folder_list, name='folder_list'),
    path('folders/add/', views.folder_create, name='folder_create'),
    path('folders/<int:pk>/edit/', views.folder_update, name='folder_update'),
    path('folders/<int:pk>/delete/', views.folder_delete, name='folder_delete'),

    path("users/import/", views.import_users_csv, name="import_users"),

    path("importer/", views.importer, name="importer"),
    path("map-fields/", views.map_fields, name="map_fields"),
    path("process-import/", views.process_import, name="process_import"),


]
