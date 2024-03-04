from django.shortcuts import redirect, render
from django.conf import settings
from .utils import get_all_custom_models
from uploads.models import Upload
from django.core.management import call_command
from django.contrib import messages

# Create your views here.
def import_data(request):
    if request.method == 'POST':
        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')


        #Store this file into uplod model
        upload = Upload.objects.create(file=file_path, model_name=model_name)

        #contruct the full path

        relative_path = str(upload.file.url)
        base_url = str(settings.BASE_DIR)

        # Construct the absolute full path
        file_path = base_url+relative_path

        # trigger the import data command
        try:
            call_command('importdata', file_path, model_name)
            messages.success(request, 'Data imported succesfully')
        except Exception as e:
            messages.error(request, str(e))
        
        return redirect('import_data')
    else:
        custom_models = get_all_custom_models()
        context = {
            'custom_models': custom_models,
        }
    return render(request, 'dataentry/importdata.html', context)