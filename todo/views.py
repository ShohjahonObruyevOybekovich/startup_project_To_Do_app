# Create your views here.
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
)
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from todo.permission import IsOwner
from todo.serializers import *


class TaskListView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = (IsAuthenticated,IsOwner)
    filter_backends = (DjangoFilterBackend,)


class TaskCreateAPIView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


class TaskUpdateAPIView(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskUpdateSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    authentication_classes = (TokenAuthentication,)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, obj)
        return obj


 #fixx
class TaskDeleteAPIView(DestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
    authentication_classes = (TokenAuthentication,)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, obj)
        return obj

class ExpenseListView(ListAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseListSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'description')


class ExpenseCreateAPIView(CreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseCreateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


class ExpenseUpdateAPIView(UpdateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseUpdateSerializer
    permission_classes = (IsAuthenticated,IsOwner)
    authentication_classes = (TokenAuthentication,)

class ExpenseDeleteAPIView(DestroyAPIView):
    queryset = Expense.objects.all()
    permission_classes = (IsAuthenticated,IsOwner)
    authentication_classes = (TokenAuthentication,)
