# Generated by Django 2.0.6 on 2018-06-13 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_search_project'),
    ]

    operations = [
        migrations.RenameField(
            model_name='searchresult',
            old_name='including_charges',
            new_name='charges_included',
        ),
    ]
