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


def export_data(cls):
    module_name = cls.__module__.split(".")[0]
    model_name = cls.__name__
    folder_path = "bookshelf/data/export/{0}".format(module_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open("{0}/{1}.csv".format(folder_path, model_name), "w") as f:
        header = ""
        for query in cls.objects.all():
            # print(query.__dict__)
            if not header:
                header = ",".join(str(key) for key, value in query.__dict__.items() if not key.startswith("_")) + "\n"
                f.write(header)
            f.write(",".join(str(value) for key, value in query.__dict__.items() if not key.startswith("_")) + "\n")

for cls in cls_list:
    export_data(cls)

