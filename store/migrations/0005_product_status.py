# Generated by Django 5.0.3 on 2024-06-27 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('waitingapproval', 'Waiting Approval'), ('active', 'Active'), ('deleted', 'Deleted')], default='active', max_length=50),
        ),
    ]