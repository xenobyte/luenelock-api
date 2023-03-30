from django.db import models
import uuid
from django.contrib.auth.models import User


class Lock(models.Model):
    name = models.CharField(max_length=128)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    is_locked = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.uuid.__str__()
