# Generated by Django 4.0 on 2022-01-06 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_table_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table_cart',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.table_product'),
        ),
        migrations.AlterField(
            model_name='table_cart',
            name='status',
            field=models.CharField(default='pending', max_length=100),
        ),
        migrations.AlterField(
            model_name='table_cart',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.table_user'),
        ),
    ]