from django.conf import settings
from django.db.models.fields.related import ForeignKey, ManyToOneRel
from staff.middleware import CurrentStaffMiddleware

# Register fields with south, if installed


class CurrentStaffField(ForeignKey):

    def __init__(self, to_field=None, to='staff.Staff', **kwargs):
        self.add_only = kwargs.pop('add_only', False)
        kwargs.update({
            'editable': False,
            'null': True,
            'to': to,
            'to_field': to_field,
        })
        super(CurrentStaffField, self).__init__(**kwargs)

    def pre_save(self, model_instance, add):
        if add or not self.add_only:
            staff = CurrentStaffMiddleware.get_staff()
            if staff:
                setattr(model_instance, self.attname, staff.pk)
                return staff.pk

        return super(CurrentStaffField, self).pre_save(model_instance, add)
