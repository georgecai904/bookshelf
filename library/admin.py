# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from jet.filters import RelatedFieldAjaxListFilter

from bookshelf.functions import export_data
from tracker.models import ReadBook
from .models import *

# Register your models here.


class BookAdmin(admin.ModelAdmin):
    def get_book_list(self, obj):
        output = ""
        for line in obj.booklistline_set.all():
            output += '<li>{0}</li>'.format(line.bookList.name)
        return format_html(output + "")
    get_book_list.short_description = "Booklist"

    def get_read_status(self, obj):
        return obj.readbook.status
    get_read_status.short_description = "Status"

    def get_cover(self, obj):
        if obj.cover:
            return format_html("<img src='http://localhost:8000/media/{0}' style='max-width:100px;'>".format(obj.cover))
    get_cover.short_description = "Cover"

    def get_tags(self, obj):
        return format_html(",".join([i.name for i in obj.tags.all()]))
    get_tags.short_description = "Tags"

    list_display = ('get_cover', 'name', 'author', 'category', 'get_tags', 'get_read_status')

    list_filter = ('author', 'year', 'category',)
    def add_to_complete(self, request, queryset):
        for book in queryset:
            rbs = ReadBook.objects.filter(book=book)
            if not rbs:
                ReadBook.objects.create(
                    book=book,
                    finished=True
                )
            else:
                rb = rbs[0]
                if not rb.finished:
                    rb.finished = True
                    rb.save()
        for bl in BookList.objects.all():
            bl.save()

    def add_to_onread(self, request, queryset):
        for book in queryset:
            rbs = ReadBook.objects.filter(book=book)
            if not rbs:
                ReadBook.objects.create(
                    book=book,
                    finished=False
                )
            else:
                rb = rbs[0]
                if rb.finished:
                    rb.finished = False
                    rb.save()
        for bl in BookList.objects.all():
            bl.save()

    actions = ('add_to_complete', )

    search_fields = ['name', 'author__name', 'category__name']

    ordering = ('name', )
    empty_value_display = ''

admin.site.register(Book, BookAdmin)


class BookManagement(admin.ModelAdmin):
    def get_book_count(self, obj):
        return obj.book_set.count()
    get_book_count.short_description = "Book Count"

    list_display = ('__str__', 'get_book_count')

    actions = (export_data, )


class CountryAdmin(BookManagement):
    def get_book_count(self, obj):
        return sum(i.book_set.count() for i in obj.author_set.all())
    get_book_count.short_description = "Book Count"

admin.site.register(Author, BookManagement)
admin.site.register(Country, CountryAdmin)
admin.site.register(Publisher, BookManagement)
admin.site.register(Category, BookManagement)


class BookListLine(admin.StackedInline):
    model = BookListLine


class BookListAdmin(admin.ModelAdmin):
    fields = ('name',)
    inlines = [
        BookListLine,
    ]

    def get_books_in_list(self, obj):
        output = ""
        for line in obj.booklistline_set.all():
            rbs = ReadBook.objects.filter(book=line.book)
            if not rbs:
                link = reverse("admin:tracker_readbook_add")
            else:
                link = reverse("admin:tracker_readbook_change", args=[rbs[0].id])
            output += '<li><a href="{1}">{0}</a></li>'.format(line.book.name, link)
        return format_html(output)

    def update_list(self, request, queryset):
        for query in queryset:
            query.save()

    get_books_in_list.short_description = "Books in List"

    list_display = ('name', 'created_at', 'get_books_in_list')

    actions = (export_data, update_list)


admin.site.register(BookList, BookListAdmin)

admin.site.register(Tag)