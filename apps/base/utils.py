from datetime import datetime
from rest_framework.permissions import DjangoModelPermissions

def validate_files(request, field, update=False):
    """ 
    :params
    :request: request.data
    :field: key of file    
    """
    
    request = request.copy()

    if update:
        if type(request[field]) == str: request.__delitem__(field)
    else:
        if type(request[field]) == str: request.__setitem__(field, None)        

    return request

def format_date(date):
    date = datetime.strptime(date, '%d/%m/%Y')
    date = f"{date.year}-{date.month}-{date.day}"
    return date

class CustomModelPermissions(DjangoModelPermissions):
    view_permissions = ['%(app_label)s.view _%(model_name)s']
    
    perms_map = {
        'GET': view_permissions,
        'OPTIONS': view_permissions,
        'HEAD': view_permissions,
        'POST': DjangoModelPermissions.perms_map['POST'],
        'PUT': DjangoModelPermissions.perms_map['PUT'],
        'PATCH': DjangoModelPermissions.perms_map['PATCH'],
        'DELETE': DjangoModelPermissions.perms_map['DELETE']
    }