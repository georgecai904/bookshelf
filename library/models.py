# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models



class Country(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Countries'


class Author(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return "[{0}]-{1}".format(self.country, self.name)


class Publisher(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False, unique=True)
    subtitle = models.CharField(max_length=30, blank=True, null=True)
    series = models.CharField(max_length=30, blank=True, null=True)
    pages = models.IntegerField()
    year = models.IntegerField()
    author = models.ForeignKey(Author, default=None, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, default=None, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return "{0}".format(self.name)

    # def save(self, *args, **kwargs):
    #     from tracker.models import ReadBook
    #     super(Book, self).save(*args, **kwargs)
    #     rbs = ReadBook.objects.filter(book=self)
    #     if not rbs:
    #         ReadBook.objects.create(
    #             book=self,
    #         )


COMPLETE = "已读列表"
ONREAD = "在读列表"
ONWAIT = "待读列表"


class BookList(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        from tracker.models import ReadBook
        if self.name == COMPLETE:
            for rb in ReadBook.objects.filter(finished=True):
                book_line = BookListLine.objects.filter(bookList__name__in=[ONREAD, ONWAIT], book=rb.book)
                if book_line:
                    book_line[0].bookList = self
                    book_line[0].save()
                else:
                    BookListLine.objects.update_or_create(
                        bookList=self,
                        book=rb.book
                    )
        elif self.name == ONREAD:
            for rb in ReadBook.objects.filter(finished=False):
                book_line = BookListLine.objects.filter(bookList__name__in=[COMPLETE, ONWAIT], book=rb.book)
                if book_line:
                    book_line[0].bookList = self
                    book_line[0].save()
                else:
                    BookListLine.objects.update_or_create(
                        bookList=self,
                        book=rb.book
                    )
        elif self.name == ONWAIT:
            for book in Book.objects.filter(readbook=None):
                book_line = BookListLine.objects.filter(bookList__name__in=[COMPLETE, ONREAD], book=book)
                if book_line:
                    book_line[0].bookList = self
                    book_line[0].save()
                else:
                    BookListLine.objects.update_or_create(
                        bookList=self,
                        book=book
                    )
        # elif self.name == ONWAIT:


        super(BookList, self).save(*args, **kwargs)


class BookListLine(models.Model):
    bookList = models.ForeignKey(BookList, on_delete=models.CASCADE)
    book = models.ForeignKey(Book)
    modified_at = models.DateField(auto_now=True)
