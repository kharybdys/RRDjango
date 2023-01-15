from abc import ABC

from django.db import models


class AbstractModelMeta(type(ABC), type(models.Model)):
    pass
