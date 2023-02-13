import json
from django.db import models
import uuid


def get_r_object():
    return {"commits": [{"date": "2020-01-01 00:00:00", "type": "new", "fecha": "miércoles, 1 enero 2020 00:00", "comment": "Nuevo elemento creado", "user_id": "?", "user_icon": 'null', "campos_mutated": [], "nombre_usuario": "?"}]}

class Common(models.Model):
    uuid=models.UUIDField(default=uuid.uuid4, editable=False)
    r_object = models.JSONField(null=True, default=get_r_object)
  
    class Meta:
        abstract = True