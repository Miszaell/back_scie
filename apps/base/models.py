from django.db import models
import uuid

class Common(models.Model):
    uuid=models.UUIDField(default=uuid.uuid4, editable=False)
    r_object = models.JSONField(null=True)
    create_uid = models.IntegerField(null=True)
    update_uid = models.IntegerField(null=True)
  
    class Meta:
        abstract = True