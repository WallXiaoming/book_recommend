# Generated by Django 3.1.1 on 2020-09-02 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('active', models.BooleanField(default=False)),
                ('body', models.TextField(verbose_name='内容')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post')),
                ('reply', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='comment.comment')),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
    ]
