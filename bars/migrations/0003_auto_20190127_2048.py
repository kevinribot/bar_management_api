# Generated by Django 2.1.5 on 2019-01-27 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bars', '0002_auto_20190126_1501'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('bar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bars.Bar')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderItems', to='bars.Reference')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='orderItems',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='bars.OrderItem'),
        ),
    ]
