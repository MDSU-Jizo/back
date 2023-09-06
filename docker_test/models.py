from django.db import models

# Create your models here.
class FakeEntity(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return '{} - {}'.format(self.pk, self.title)

    def get_title_text(self):
        return {'id': self.pk, 'title': self.title, 'text': self.text}