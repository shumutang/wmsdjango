# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-21 16:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='\u5ba2\u6237\u540d\u79f0')),
                ('address', models.CharField(max_length=80, verbose_name='\u5730\u5740')),
                ('city', models.CharField(max_length=20, verbose_name='\u57ce\u5e02')),
                ('tel', models.CharField(max_length=15, verbose_name='\u7535\u8bdd')),
                ('phone', models.CharField(max_length=11, verbose_name='\u624b\u673a')),
                ('email', models.EmailField(blank=True, max_length=75, verbose_name='\u90ae\u7bb1')),
            ],
            options={
                'verbose_name': '\u5ba2\u6237',
                'verbose_name_plural': '\u5ba2\u6237',
            },
        ),
        migrations.CreateModel(
            name='OrderIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(blank=True, max_length=16, null=True, verbose_name='\u8ba2\u5355\u6d41\u6c34(\u7cfb\u7edf\u81ea\u52a8\u751f\u6210)')),
                ('invoice', models.IntegerField(verbose_name='\u53d1\u7968\u53f7')),
                ('pcs', models.IntegerField(verbose_name='\u8ba2\u5355pcs')),
                ('boxes', models.IntegerField(verbose_name='\u5408\u8ba1\u7bb1\u6570')),
                ('in_store', models.CharField(choices=[('1', '\u662f'), ('2', '\u5426')], default='2', max_length=4, verbose_name='\u5165\u5e93')),
                ('order_type', models.CharField(choices=[('\u5165\u5e93', (('1', '\u6b63\u5e38\u5165\u5e93'), ('2', '\u8d60\u54c1\u5165\u5e93'), ('3', '\u4e0d\u826f\u54c1\u5165\u5e93'))), ('\u51fa\u5e93', (('4', '\u6b63\u5e38\u51fa\u5e93'), ('5', '\u8d60\u54c1\u51fa\u5e93'))), ('\u5176\u4ed6', (('6', '\u672a\u77e5'),))], default='1', max_length=10, verbose_name='\u8ba2\u5355\u7c7b\u578b')),
                ('order_comment', models.CharField(blank=True, max_length=60, null=True, verbose_name='\u8ba2\u5355\u5907\u6ce8')),
                ('order_state', models.CharField(choices=[('1', '\u63a5\u5355'), ('2', '\u64cd\u4f5c\u4e2d'), ('3', '\u5df2\u5165\u5e93'), ('4', '\u5df2\u51fa\u5e93')], max_length=10, verbose_name='\u8ba2\u5355\u72b6\u6001')),
                ('operate_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='\u64cd\u4f5c\u65e5\u671f')),
                ('in_number', models.CharField(max_length=20, verbose_name='\u5165\u5e93\u7f16\u53f7')),
                ('sender', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u7ed3\u7b97\u5355\u4f4d')),
                ('receiver', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u9001\u8d27\u5355\u4f4d')),
                ('plan_in_time', models.DateField(blank=True, null=True, verbose_name='\u8ba1\u5212\u5165\u5e93\u65e5\u671f')),
                ('operator', models.CharField(blank=True, max_length=60, null=True, verbose_name='\u5236\u5355\u4eba')),
                ('fact_in_time', models.DateField(blank=True, null=True, verbose_name='\u5b9e\u9645\u5165\u5e93\u65e5\u671f')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wms.Customer', verbose_name='\u6240\u5c5e\u5ba2\u6237')),
            ],
            options={
                'ordering': ['plan_in_time'],
                'verbose_name': '\u8ba2\u5355(\u5165\u5e93)',
                'verbose_name_plural': '\u8ba2\u5355(\u5165\u5e93)',
            },
        ),
        migrations.CreateModel(
            name='OrderInProductship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderin_pcs', models.IntegerField(default=0, verbose_name='\u5165\u5e93\u6570\u91cf')),
                ('orderin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wms.OrderIn', verbose_name='\u8ba2\u5355\u7f16\u53f7')),
            ],
            options={
                'verbose_name': '\u5165\u5e93\u8ba2\u5355-\u5546\u54c1',
                'verbose_name_plural': '\u5165\u5e93\u8ba2\u5355-\u5546\u54c1',
            },
        ),
        migrations.CreateModel(
            name='OrderOut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(blank=True, max_length=16, null=True, verbose_name='\u8ba2\u5355\u6d41\u6c34(\u7cfb\u7edf\u81ea\u52a8\u751f\u6210)')),
                ('invoice', models.IntegerField(verbose_name='\u53d1\u7968\u53f7')),
                ('pcs', models.IntegerField(verbose_name='\u8ba2\u5355pcs')),
                ('boxes', models.IntegerField(verbose_name='\u5408\u8ba1\u7bb1\u6570')),
                ('in_store', models.CharField(choices=[('1', '\u662f'), ('2', '\u5426')], default='2', max_length=4, verbose_name='\u5165\u5e93')),
                ('order_type', models.CharField(choices=[('\u5165\u5e93', (('1', '\u6b63\u5e38\u5165\u5e93'), ('2', '\u8d60\u54c1\u5165\u5e93'), ('3', '\u4e0d\u826f\u54c1\u5165\u5e93'))), ('\u51fa\u5e93', (('4', '\u6b63\u5e38\u51fa\u5e93'), ('5', '\u8d60\u54c1\u51fa\u5e93'))), ('\u5176\u4ed6', (('6', '\u672a\u77e5'),))], default='1', max_length=10, verbose_name='\u8ba2\u5355\u7c7b\u578b')),
                ('order_comment', models.CharField(blank=True, max_length=60, null=True, verbose_name='\u8ba2\u5355\u5907\u6ce8')),
                ('order_state', models.CharField(choices=[('1', '\u63a5\u5355'), ('2', '\u64cd\u4f5c\u4e2d'), ('3', '\u5df2\u5165\u5e93'), ('4', '\u5df2\u51fa\u5e93')], max_length=10, verbose_name='\u8ba2\u5355\u72b6\u6001')),
                ('operate_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='\u64cd\u4f5c\u65e5\u671f')),
                ('out_number', models.CharField(max_length=20, verbose_name='\u51fa\u5e93\u7f16\u53f7')),
                ('fact_out_time', models.DateField(blank=True, null=True, verbose_name='\u51fa\u5e93\u65e5\u671f')),
                ('receiver', models.CharField(blank=True, max_length=10, null=True, verbose_name='\u6536\u8d27\u4eba')),
                ('receiver_addr', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u9001\u8d27\u5730\u5740')),
                ('receiver_phone', models.IntegerField(blank=True, null=True, verbose_name='\u6536\u8d27\u4eba\u7535\u8bdd')),
                ('operator', models.CharField(blank=True, max_length=60, null=True, verbose_name='\u51fa\u5e93\u4eba')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wms.Customer', verbose_name='\u6240\u5c5e\u5ba2\u6237')),
            ],
            options={
                'ordering': ['fact_out_time'],
                'verbose_name': '\u8ba2\u5355(\u51fa\u5e93)',
                'verbose_name_plural': '\u8ba2\u5355(\u51fa\u5e93)',
            },
        ),
        migrations.CreateModel(
            name='OrderOutProductship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderout_pcs', models.IntegerField(default=0, verbose_name='\u51fa\u5e93\u6570\u91cf')),
                ('orderout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wms.OrderOut')),
            ],
            options={
                'verbose_name': '\u51fa\u5e93\u8ba2\u5355-\u5546\u54c1',
                'verbose_name_plural': '\u51fa\u5e93\u8ba2\u5355-\u5546\u54c1',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='\u4e2d\u6587\u540d\u79f0')),
                ('ename', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u82f1\u6587\u540d\u79f0')),
                ('help_name', models.CharField(blank=True, max_length=75, verbose_name='\u52a9\u8bb0\u7801')),
                ('batch_num', models.IntegerField(default=100, verbose_name='\u8d27\u7269\u6279\u53f7')),
                ('type', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u578b\u53f7')),
                ('categories', models.CharField(choices=[('1', '\u6709\u6761\u7801'), ('2', '\u65e0\u6761\u7801'), ('3', '\u5176\u4ed6')], default='1', max_length=20, verbose_name='\u5546\u54c1\u5206\u7c7b')),
                ('base_unit', models.CharField(choices=[('1', '\u7bb1'), ('2', '\u6876'), ('3', '\u5305'), ('4', '\u53f0'), ('5', '\u74f6'), ('6', '\u4ef6'), ('9', '\u5176\u4ed6')], default='1', max_length=6, verbose_name='\u57fa\u672c\u5355\u4f4d')),
                ('pcs_perunit', models.IntegerField(default=1, verbose_name='PCS/\u7bb1')),
                ('Logistics_unit', models.CharField(blank=True, choices=[('1', '\u7bb1'), ('2', '\u6876'), ('3', '\u5305'), ('4', '\u53f0'), ('5', '\u74f6'), ('6', '\u4ef6'), ('9', '\u5176\u4ed6')], max_length=10, null=True, verbose_name='\u7269\u6d41\u5355\u4f4d')),
                ('pcs_Logistics', models.IntegerField(default=1, verbose_name='PCS/\u6807\u51c6\u677f')),
                ('life_day', models.IntegerField(default=0, verbose_name='\u4fdd\u8d28\u671f(\u5929)')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='\u5355\u4ef7')),
                ('width', models.IntegerField(default=0, verbose_name='\u5bbd\u5ea6(CM)')),
                ('height', models.IntegerField(default=0, verbose_name='\u9ad8\u5ea6(CM)')),
                ('length', models.IntegerField(default=0, verbose_name='\u957f\u5ea6(CM)')),
                ('weight', models.IntegerField(default=0, verbose_name='\u91cd\u91cf(KG)')),
                ('net_weight', models.IntegerField(default=0, verbose_name='\u51c0\u91cd(KG)')),
                ('valid_flag', models.CharField(default='Y', max_length=6, verbose_name='\u6709\u6548\u6807\u5fd7')),
                ('barcode', models.CharField(max_length=20, verbose_name='\u6761\u5f62\u7801')),
                ('specs', models.CharField(blank=True, max_length=60, null=True, verbose_name='\u89c4\u683c')),
                ('brand', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u54c1\u724c')),
                ('ordinal', models.IntegerField(blank=True, default=0, null=True, verbose_name='\u5e8f\u53f7')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wms.Customer', verbose_name='\u6240\u5c5e\u5ba2\u6237')),
            ],
            options={
                'verbose_name': '\u5546\u54c1',
                'verbose_name_plural': '\u5546\u54c1',
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='\u4ed3\u5e93\u540d\u79f0')),
                ('ename', models.CharField(blank=True, max_length=4, null=True, verbose_name='\u4ed3\u5e93\u7b80\u7801')),
                ('address', models.CharField(blank=True, max_length=75, verbose_name='\u4ed3\u5e93\u5730\u5740')),
                ('type', models.CharField(choices=[('normal', '\u5168\u54c1\u7c7b\u4ed3\u5e93'), ('blp', '\u4e0d\u826f\u54c1\u4ed3\u5e93'), ('zp', '\u8d60\u54c1\u4ed3\u5e93')], default='normal', max_length=8, verbose_name='\u4ed3\u5e93\u7c7b\u578b')),
            ],
            options={
                'verbose_name': '\u4ed3\u5e93',
                'verbose_name_plural': '\u4ed3\u5e93',
            },
        ),
        migrations.AddField(
            model_name='orderoutproductship',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wms.Product', verbose_name='\u5546\u54c1\u540d\u79f0'),
        ),
        migrations.AddField(
            model_name='orderout',
            name='product',
            field=models.ManyToManyField(through='wms.OrderOutProductship', to='wms.Product', verbose_name='\u5546\u54c1\u540d\u79f0'),
        ),
        migrations.AddField(
            model_name='orderout',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wms.Warehouse', verbose_name='\u64cd\u4f5c\u4ed3\u5e93'),
        ),
        migrations.AddField(
            model_name='orderinproductship',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wms.Product', verbose_name='\u5546\u54c1\u540d\u79f0'),
        ),
        migrations.AddField(
            model_name='orderin',
            name='product',
            field=models.ManyToManyField(through='wms.OrderInProductship', to='wms.Product', verbose_name='\u5546\u54c1\u540d\u79f0'),
        ),
        migrations.AddField(
            model_name='orderin',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wms.Warehouse', verbose_name='\u64cd\u4f5c\u4ed3\u5e93'),
        ),
    ]
