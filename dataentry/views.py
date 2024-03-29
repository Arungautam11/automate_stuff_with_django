from django.shortcuts import redirect, render
from django.conf import settings
from .utils import check_csv_errors, get_all_custom_models
from uploads.models import Upload
from django.contrib import messages
from .tasks import import_data_task, export_data_task
from django.core.management import call_command

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

        # Check for the CSV errors
        try:
            check_csv_errors(file_path, model_name)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('import_data')

        # Handle the import data task here
        import_data_task.delay(file_path, model_name)
        
        # Show the message to the user
        messages.success(request, 'Data is being imported, notify by email when it is done.!')
        return redirect('import_data')
    else:
        custom_models = get_all_custom_models()
        context = {
            'custom_models': custom_models,
        }
    return render(request, 'dataentry/importdata.html', context)


def export_data(request):
    if request.method == 'POST':
        model_name = request.POST.get('model_name')

        # Call the export data task
        export_data_task.delay(model_name)

        # Show the message to the user
        messages.success(request, 'Data is being exported, notify by email when it is done.!')
        return redirect('export_data')
    else:
        custom_models = get_all_custom_models()
        context = {
            'custom_models': custom_models,
        }
    return render(request, 'dataentry/exportdata.html', context)