from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import csv
import datetime
from dataentry.utils import generate_csv_file


# Proposed command - python manage.py exportdata model_name


class Command(BaseCommand):
    help = "Export data from database to a CSV file"

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Name of the model')

    def handle(self, *args, **kwargs):
        model_name = kwargs['model_name'].capitalize()


        # Search through all the installed apps for the model
        model = None
        for app_config in apps.get_app_configs():
            #Try to search for the model
            try:
                model = apps.get_model(app_config.label, model_name)
                break # stop searching once the model is found
            except LookupError:
                pass # model not found in this app, continue searching.
        if not model:
            self.stderr.write(f'Model "{model_name}" could not found!')
            return

        # fetch the data from the database
        data = model.objects.all()

        # generate the exported csv file
        file_path = generate_csv_file(model_name)

        # open the CSV file and write the data
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)

            # writer the CSV header

            # we want to print the field names of the model that we are tring to export
            writer.writerow([field.name for field in model._meta.fields])

            # writer the data rows
            for dt in data:
                writer.writerow([getattr(dt, field.name) for field in model._meta.fields])

        self.stdout.write(self.style.SUCCESS('Data exported successfully!'))