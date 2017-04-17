# -*- coding: utf-8 -*-
from south.db import db, engine
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Category.slug'
        db.alter_column('qa_category', 'slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255))

        # Changing field 'Category.name'
        db.alter_column('qa_category', 'name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255))

        # Changing field 'Reference.name'
        db.alter_column('qa_reference', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Test.name'
        db.alter_column('qa_test', 'name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255))

        if 'sql_server' in engine:
            sql_server_idxs = (('qa_testlist', 'name'), ('qa_testlistcycle', 'name'),)
            for table_name, column_name in sql_server_idxs:
                try:
                    db.drop_index(table_name, column_name)
                except:
                    pass
                # sqlserver_utils.drop_index(db,table_name,column_name)

        # Changing field 'TestList.name'
        db.alter_column('qa_testlist', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'TestListCycle.name'
        db.alter_column('qa_testlistcycle', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        if 'sql_server' in engine:
            for table_name, column_name in sql_server_idxs:
                db.create_index(table_name, [column_name])

    def backwards(self, orm):

        # Changing field 'Category.slug'
        db.alter_column('qa_category', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=255, unique=True))

        # Changing field 'Category.name'
        db.alter_column('qa_category', 'name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True))

        # Changing field 'Reference.name'
        db.alter_column('qa_reference', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Test.name'
        db.alter_column('qa_test', 'name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True))

        # Changing field 'TestList.name'
        db.alter_column('qa_testlist', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'TestListCycle.name'
        db.alter_column('qa_testlistcycle', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'qa.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        'qa.frequency': {
            'Meta': {'ordering': "('nominal_interval',)", 'object_name': 'Frequency'},
            'due_interval': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'nominal_interval': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'overdue_interval': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'qa.reference': {
            'Meta': {'object_name': 'Reference'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reference_creators'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reference_modifiers'", 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'numerical'", 'max_length': '15'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'qa.test': {
            'Meta': {'object_name': 'Test'},
            'calculation_procedure': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qa.Category']"}),
            'choices': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'constant_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'test_creator'", 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'test_modifier'", 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'procedure': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'simple'", 'max_length': '10'})
        },
        'qa.testinstance': {
            'Meta': {'ordering': "('work_completed',)", 'object_name': 'TestInstance'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'test_instance_creator'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_progress': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'test_instance_modifier'", 'to': "orm['auth.User']"}),
            'pass_fail': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'reference': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qa.Reference']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'review_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'reviewed_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'skipped': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qa.TestInstanceStatus']"}),
            'test_list_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qa.TestListInstance']", 'null': 'True', 'blank': 'True'}),
            'tolerance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qa.Tolerance']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'unit_test_info': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qa.UnitTestInfo']"}),
            'value': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'work_completed': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'work_started': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'qa.testinstancestatus': {
            'Meta': {'object_name': 'TestInstanceStatus'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'export_by_default': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'requires_comment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'requires_review': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'qa.testlist': {
            'Meta': {'object_name': 'TestList'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'qa_testlist_created'", 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'qa_testlist_modified'", 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'sublists': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['qa.TestList']", 'null': 'True', 'blank': 'True'}),
            'tests': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['qa.Test']", 'through': "orm['qa.TestListMembership']", 'symmetrical': 'False'})
        },
        'qa.testlistcycle': {
            'Meta': {'object_name': 'TestListCycle'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'qa_testlistcycle_created'", 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'qa_testlistcycle_modified'", 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'test_lists': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['qa.TestList']", 'through': "orm['qa.TestListCycleMembership']", 'symmetrical': 'False'})
        },
        'qa.testlistcyclemembership': {
            'Meta': {'ordering': "('order',)", 'object_name': 'TestListCycleMembership'},
            'cycle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qa.TestListCycle']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'test_list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qa.TestList']"})
        },
        'qa.testlistinstance': {
            'Meta': {'ordering': "('work_completed',)", 'object_name': 'TestListInstance'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'test_list_instance_creator'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_progress': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'test_list_instance_modifier'", 'to': "orm['auth.User']"}),
            'test_list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qa.TestList']"}),
            'unit_test_collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qa.UnitTestCollection']"}),
            'work_completed': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'db_index': 'True'}),
            'work_started': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'qa.testlistmembership': {
            'Meta': {'ordering': "('order',)", 'unique_together': "(('test_list', 'test'),)", 'object_name': 'TestListMembership'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qa.Test']"}),
            'test_list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qa.TestList']"})
        },
        'qa.tolerance': {
            'Meta': {'object_name': 'Tolerance'},
            'act_high': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'act_low': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tolerance_creators'", 'to': "orm['auth.User']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mc_pass_choices': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'mc_tol_choices': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tolerance_modifiers'", 'to': "orm['auth.User']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'tol_high': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'tol_low': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'qa.unittestcollection': {
            'Meta': {'ordering': "('testlist__name', 'testlistcycle__name')", 'unique_together': "(('unit', 'frequency', 'content_type', 'object_id'),)", 'object_name': 'UnitTestCollection'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Group']", 'null': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'frequency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qa.Frequency']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qa.TestListInstance']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['units.Unit']"}),
            'visible_to': ('django.db.models.fields.related.ManyToManyField', [], {'default': '[]', 'related_name': "'test_collection_visibility'", 'symmetrical': 'False', 'to': "orm['auth.Group']"})
        },
        'qa.unittestinfo': {
            'Meta': {'unique_together': "(['test', 'unit'],)", 'object_name': 'UnitTestInfo'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Group']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qa.TestInstance']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'reference': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qa.Reference']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qa.Test']"}),
            'tolerance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qa.Tolerance']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['units.Unit']"})
        },
        'units.modality': {
            'Meta': {'unique_together': "[('type', 'energy')]", 'object_name': 'Modality'},
            'energy': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'units.unit': {
            'Meta': {'ordering': "['number']", 'object_name': 'Unit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'install_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'modalities': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['units.Modality']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['units.UnitType']"})
        },
        'units.unittype': {
            'Meta': {'unique_together': "[('name', 'model')]", 'object_name': 'UnitType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['qa']
