
import csv
from myapp.models import Customer
import pandas as pd
from django.db import migrations
csv_file = 'E:\MyDemoOU\DoAN\Python\Churn_Modelling.csv'


df  = pd.read_csv("E:\MyDemoOU\DoAN\Python\Churn_Modelling.csv")
def import_data(apps, schema_editor):
    # Import and insert your data here
    YourModel = apps.get_model('my_app', 'Customer')

    # Load data from your DataFrame (replace 'your_dataframe' with your actual DataFrame)
    data_to_import = df.to_dict(orient='records')

    for item in data_to_import:
        # Create a new object for YourModel with the data from the DataFrame
        YourModel.objects.create(**item)

class Migration(migrations.Migration):

    dependencies = [
        ('your_app_name', '0002_initial'),  # Replace with the correct dependency
    ]

    operations = [
        migrations.RunPython(import_data),
    ]