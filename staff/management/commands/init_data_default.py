from django.core.management.base import BaseCommand, CommandError
from staff.models import Role
from staff.serializers import RoleSerializer
import traceback

"""
    Init data default.
"""


class Command(BaseCommand):

    class BASE_DATA:
        ROLE_DATA_CONST = [
            {"name": "System Admin", "description": "System Admin", "permission": ""},
            {"name": "Manager", "description": "Manager", "permission": ""},
            {"name": "Article/SEO Admin",
             "description": "Article/SEO Admin", "permission": ""},
            {"name": "Content Staff",
             "description": "Content Staff", "permission": ""},
            {"name": "Content Leader",
             "description": "Content Leader", "permission": ""},
            {"name": "Sale", "description": "Sale", "permission": ""},
            {"name": "Sale Leader", "description": "Sale Leader", "permission": ""},
            {"name": "Accountant", "description": "Accountant", "permission": ""},
            {"name": "Accountant Leader",
             "description": "Accountant Leader", "permission": ""},
            {"name": "Customer Care",
             "description": "Customer Care", "permission": ""},
            {"name": "Customer Care Leader",
             "description": "Customer Care Leader", "permission": ""}
        ]

    """
        Init data default for role table.
    """

    def init_role_data(self):
        print "Init Role Data"
        try:
            roles = [Role(name=role['name'], description=role['description'])
                     for role in self.BASE_DATA.ROLE_DATA_CONST]
            Role.objects.bulk_create(roles)
        except Exception, e:
            print "Error Init Data For Roles : ", traceback.format_exc()
            pass

    def handle(self, *args, **options):
        try:
            # init data for role
            self.init_role_data()
        except Exception, e:
            print "Error Init Data: ", e
            pass
