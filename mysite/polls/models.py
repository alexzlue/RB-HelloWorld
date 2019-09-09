import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .helper import language_check


def language_filter(text):
    value = language_check(text)
    if value[0]:
        raise ValidationError(_(
                'Coarse words like ' + value[1] + ' are not allowed.'))


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def clean(self):
        language_filter(self.question_text)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def clean(self):
        language_filter(self.choice_text)

    def __str__(self):
        return self.choice_text


class Company(models.Model):
    BUSINESS_TYPES = (
        ('B2B', 'Business-to-Business'),
        ('B2C', 'Business-to-Consumer'),
        ('B2A', 'Business-to-Anyone')
    )
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    type = models.CharField(max_length=2, choices=BUSINESS_TYPES)
    created_at = models.DateTimeField('date created')
    updated_at = models.DateField('date updated')
