from django.db import models
from django.db.models import ForeignKey

from clients.models import Client
from config import settings

from users.models import NULLABLE


class MailingMessage(models.Model):
    subject = models.CharField(max_length=150, verbose_name='тема письма')
    body = models.TextField(**NULLABLE, verbose_name='тело письма')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='mails', related_query_name="mail",
                              **NULLABLE, verbose_name='автор рассылки')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class MailingSettings(models.Model):
    class FREQUENCY(models.TextChoices):
        DAILY = 'Ежедневно'
        WEEKLY = 'Еженедельно'
        MONTHLY = 'Ежемесячно'

    class STATUS(models.TextChoices):
        DRAFT = 'Черновик'
        CREATED = 'Создана'
        RUNNING = 'Запущена'
        COMPLETED = 'Завершена'

    message = ForeignKey(MailingMessage, on_delete=models.CASCADE,
                         related_name='settings', related_query_name="setting",
                         verbose_name='рассылка')
    mailing_start = models.DateField(**NULLABLE, verbose_name='начало рассылки')
    mailing_end = models.DateField(**NULLABLE, verbose_name='конец рассылки')
    mailing_period = models.CharField(max_length=12, choices=FREQUENCY.choices,
                                      **NULLABLE, verbose_name='периодичность')
    mailing_status = models.CharField(max_length=10, choices=STATUS.choices,
                                      default='draft', verbose_name='статус рассылки')

    recipient = models.ManyToManyField(Client, related_name='clients', verbose_name='клиенты')

    def __str__(self):
        return f'{self.mailing_start} - {self.mailing_end}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

        ordering = ('mailing_start', 'mailing_end',)
