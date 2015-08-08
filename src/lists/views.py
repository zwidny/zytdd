# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.utils.html import escape
# from django.http import HttpResponse

from .models import Item, List


def home(request):
    return render(request, 'lists/home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request,
                  'lists/list.html',
                  {'items': items,
                   'list': list_})


def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        expected_error = escape("You can't have an empty list item")
        return render(request, 'lists/home.html', {"error": expected_error})
    return redirect('/lists/%d/' % (list_.id, ))


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id, ))
