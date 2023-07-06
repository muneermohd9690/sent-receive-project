from django.shortcuts import render
from .models import Toners, ExcelFile, Items
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from pathlib import Path


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def excel(request):
    return HttpResponse("this is for the excel operations")

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def excel_import_items_db(request):
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']

            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.path(filename)

            print(str(uploaded_file_url))
            itemsexceldata = pd.read_csv(uploaded_file_url, sep=",", encoding='utf-8')
            dbframe = itemsexceldata
            for dbframe in dbframe.itertuples():
                obj = Items.objects.create(model_no=dbframe.model_no, description=dbframe.description)
                obj.save()
            filename = fs.delete(myfile.name)
            #return render(request, 'excel_import_db.html', {'uploaded_file_url': uploaded_file_url})
            return render(request, 'excel_import_db.html', {})
    except Exception as identifier:
        print(identifier)
    return render(request, 'excel_import_db.html', {})

