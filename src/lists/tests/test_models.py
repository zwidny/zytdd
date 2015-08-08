# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, "Item the second")
        self.assertEqual(second_saved_item.list, list_)

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text="")
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/%d/' % (list_.id))


class ListViewTest(TestCase):

    # def test_displays_all_items(self):
    #     list_ = List.objects.create()
    #     Item.objects.create(text='itemey 1', list=list_)
    #     Item.objects.create(text='itemey 2', list=list_)

    #     response = self.client.get('/lists/the-only-list-in-the-world/')

    #     self.assertContains(response, 'itemey 1')
    #     self.assertContains(response, 'itemey 2')

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id, ))
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id, ))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id, ))
        self.assertEqual(response.context['list'], correct_list)


class NewListTest(TestCase):

        def test_saving_a_POST_request(self):
            self.client.post('/lists/new',
                             data={'id_text': 'A new list item'})
            self.assertEqual(Item.objects.count(), 1)
            new_item = Item.objects.first()
            self.assertEqual(new_item.text, "A new list item")

        def test_redirects_after_POST(self):
            response = self.client.post(
                '/lists/new',
                data={'id_text': 'A new list item'})
            new_list = List.objects.first()
            self.assertRedirects(response, '/lists/%d/' % (new_list.id, ))

        def test_can_save_a_POST_request_to_an_existing_list(self):
            other_list = List.objects.create()
            correct_list = List.objects.create()

            self.client.post(
                '/lists/%d/' % (correct_list.id, ),
                data={'id_text': "A new item for an existing list"}
            )

            self.assertEqual(Item.objects.count(), 1)
            new_item = Item.objects.first()
            self.assertEqual(new_item.text, 'A new item for an existing list')
            self.assertEqual(new_item.list, correct_list)
            self.assertNotEqual(new_item.list, other_list)

        def test_redirects_to_list_view(self):
            correct_list = List.objects.create()

            response = self.client.post(
                '/lists/%d/' % (correct_list.id, ),
                data={'id_text': "A new item for an existing list"}
            )
            self.assertRedirects(response, '/lists/%d/' % (correct_list.id, ))
