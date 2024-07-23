
from django.urls import path

from todo.views import *

urlpatterns = [
    path('task-list/',TaskListView.as_view(), name='user_list'),
    path('task-create/', TaskCreateAPIView.as_view(), name='task_create'),
    path('task-update/<int:uuid>/', TaskUpdateAPIView.as_view(), name='task_update'),
    path('task-delete/<int:uuid>/', TaskDeleteAPIView.as_view(), name='task_delete'),


    path('expense-list/',ExpenseListView.as_view(), name='expense_list'),
    path('expense-create/', ExpenseCreateAPIView.as_view(), name='expense_create'),
    path('expense-update/<int:uuid>/', ExpenseUpdateAPIView.as_view(), name='exp_update'),
    path('expense-delete/<int:uuid>/', ExpenseDeleteAPIView.as_view(), name='exp_update'),
]