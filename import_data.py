# --------------------------Set Up Django Environment--------------------------
from django.core.wsgi import get_wsgi_application
import os, sys, csv

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookshelf.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
application = get_wsgi_application()
# --------------------------Set Up Django Environment--------------------------

from library.models import *
from tracker.models import *

cls_list = []
cls_list.extend([Country, Author, Publisher, Category, Book, BookList])
cls_list.extend([ReadBook, ReadBookRecord])

ORIG = "original"
EXPO = "export"


def import_data(cls, type):
    # print(os.path.abspath(__file__))
    file_path = "bookshelf/data/{0}/{1}/{2}.csv".format(type, cls.__module__.split(".")[0], cls.__name__)
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            print(cls)
        for row in reader:
            # print({header[index]:row[index] for index,_ in enumerate(row)})
            row = [i if i != "None" else "" for i in row]
            cls.objects.update_or_create(
                **{header[index]: row[index] for index, _ in enumerate(row)}
            )

for cls in cls_list:
    import_data(cls, EXPO)

def import_user():
    from django.contrib.auth.models import User
    if not User.objects.filter(username='george'):
        u = User(username='george')
        u.set_password('yiming123')
        u.is_superuser = True
        u.is_staff = True
        u.save()

import_user()