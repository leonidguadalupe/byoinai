from django.db import models

from .base import BaseModel


class Sync(BaseModel):
    REQUESTED = 'requested'
    SYNCING = 'syncing'
    DONE = 'done'
    FAILED = 'failed'

    STATUS_TYPES = (
          ('requested', REQUESTED),
          ('syncing', SYNCING),
          ('done', DONE),
          ('failed', FAILED)
    )

    status = models.CharField(choices=STATUS_TYPES,
                              default=SYNCING, max_length=64)
    # this field is for adding a reason why syncing failed
    reason = models.CharField(blank=True, null=True, max_length=500)
    # TODO:
    # 1. Implement recording of which user ran sync
    #    (add a model foreign key here)
    # 2. status default will be requested and
    #    there will be queueing for syncing action.

    class Meta:
        verbose_name = "sync"
        verbose_name_plural = "syncs"
        ordering = ['-created_date']
