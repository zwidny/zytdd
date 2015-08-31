# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from .models import List
from .forms import ExistingListItemForm, ItemForm
User = get_user_model()


def home(request):
    return render(request, 'lists/home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'lists/list.html',
                  {'list': list_, "form": form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        list_.owner = request.user
        list_.save()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'lists/home.html', {"form": form})


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'lists/my_lists.html', {'owner': owner})
