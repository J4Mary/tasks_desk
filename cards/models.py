from django.db import models

from helpdesk import settings

USER_MODEL = settings.AUTH_USER_MODEL


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Card(TimeStampModel):

    NEW = 1
    IN_PROGRESS = 2
    IN_QA = 3
    READY = 4
    DONE = 5

    STATUSES = (
        (NEW, 'NEW'),
        (IN_PROGRESS, 'IN_PROGRESS'),
        (IN_QA, 'IN_QA'),
        (READY, 'READY'),
        (DONE, 'DONE')
    )

    text = models.TextField(max_length=1000)
    status = models.PositiveIntegerField(choices=STATUSES, default=NEW)
    created_by = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, related_name='creator')
    assigned_to = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, related_name='executor')

    def __str__(self):
        return f"'{self.text} created by {self.created_by}"
