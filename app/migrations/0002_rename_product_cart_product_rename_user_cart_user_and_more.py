# Generated by Django 4.1 on 2022-09-04 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='Product',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='User',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='orderplaced',
            old_name='Customer',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='orderplaced',
            old_name='Product',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='orderplaced',
            old_name='User',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='product',
            name='CATEGORY',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('ch', 'chair'), ('tb', 'table'), ('sf', 'sofa'), ('oc', 'officechair'), ('ot', 'officetable'), ('os', 'officesofa'), ('kb', 'kidsbed'), ('ks', 'kidsstudy'), ('kst', 'kidsseating')], default=' ', max_length=5),
            preserve_default=False,
        ),
    ]
