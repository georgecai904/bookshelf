from datetime import datetime

from django.db import models
from django.utils.html import format_html

from library.models import Book, BookList

# Create your models here.

FMT = "%Y-%m-%d %H:%M"

READSTATUS = (
    ('已读', '已读'),
    ('在读', '在读'),
    ('待读', '待读'),
)


class ReadBook(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)
    status = models.CharField(max_length=2, choices=READSTATUS, default='待读')
    ratio = models.IntegerField(default=0)

    def get_start_to_end(self):
        records = self.readbookrecord_set.all().order_by('start')
        output = ""
        if records:
            output = "{0} - {1}".format(records.first().start.strftime(FMT), records.last().end.strftime(FMT))
        return output

    def get_progress_bar(self):
        records = self.readbookrecord_set.all().order_by('start')
        if not self.finished:
            if records:
                ratio = int(records.last().end_page / self.book.pages * 100)
            else:
                ratio = 0
        else:
            ratio = 100
        self.ratio = ratio
        if ratio > 0 and self.status == '待读':
            if ratio == 100:
                self.status = "已读"
            else:
                self.status = '在读'
        self.save()
        return format_html("<progress value='{0}' max='100'></progress>".format(ratio))

    # def save(self, *args, **kwargs):
    #     super(ReadBook, self).save(*args, **kwargs)
    #     if self.readbookrecord_set.count() == 0:
    #         ReadBookRecord.objects.create(
    #             readBook=self,
    #             start=datetime.now(),
    #             end=datetime.now(),
    #             end_page=0
    #         )

    def __str__(self):
        return self.book.name


class ReadBookRecord(models.Model):
    readBook = models.ForeignKey(ReadBook, on_delete=models.CASCADE)
    start = models.DateTimeField(null=False, blank=False)
    end = models.DateTimeField(null=False, blank=False)
    end_page = models.IntegerField(default=0)

    def __str__(self):
        return "{0} - {1}".format(self.start.strftime(FMT), self.end.strftime(FMT))


class ReadingNote(models.Model):
    book = models.ForeignKey(Book)
    original = models.TextField(blank=True)
    thought = models.TextField(blank=True)
    createdDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{0}[{1}]".format(self.book, self.createdDate)