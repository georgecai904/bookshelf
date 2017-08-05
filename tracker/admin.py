from django.contrib import admin

# Register your models here.
from .models import *


class ReadBookLine(admin.StackedInline):
    model = ReadBookRecord
    extra = 1


class ReadBookAdmin(admin.ModelAdmin):
    inlines = [ReadBookLine]

    list_display = ('book', 'ratio', 'get_progress_bar', 'status')
    list_filter = ('status', )
    search_fields = ('book__name', )


class ReadingNoteAdmin(admin.ModelAdmin):
    list_display = ('book', 'createdDate', 'original', 'thought')


admin.site.register(ReadBook, ReadBookAdmin)
admin.site.register(ReadingNote, ReadingNoteAdmin)