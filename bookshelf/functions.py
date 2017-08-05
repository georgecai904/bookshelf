import os


def export_data(self, request, queryset):
    module_name = self.model.__module__.split(".")[0]
    model_name = self.model.__name__
    folder_path = "data/export/{0}".format(module_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open("{0}/{1}.csv".format(folder_path, model_name), "w") as f:
        header = ""
        for query in queryset:
            if not header:
                header = ",".join(str(key) for key, value in query.__dict__.items() if not key.startswith("_")) + "\n"
                f.write(header)
            f.write(",".join(str(value) for key,value in query.__dict__.items() if not key.startswith("_")) + "\n")