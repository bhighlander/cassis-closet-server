# Generated by Django 4.2.6 on 2023-11-20 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cassisapi', '0003_article_last_edited'),
    ]

    operations = [
        migrations.CreateModel(
            name='Outfit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='OutfitArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cassisapi.article')),
                ('outfit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cassisapi.outfit')),
            ],
        ),
        migrations.AddField(
            model_name='outfit',
            name='articles',
            field=models.ManyToManyField(through='cassisapi.OutfitArticle', to='cassisapi.article'),
        ),
        migrations.AddField(
            model_name='outfit',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cassisapi.color'),
        ),
        migrations.AddField(
            model_name='outfit',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cassisapi.fashionista'),
        ),
    ]
