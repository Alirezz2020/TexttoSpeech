from django.db import models

class ConversionHistory(models.Model):
    file_name = models.CharField(max_length=100)
    text = models.TextField()
    audio_file = models.FileField(upload_to='tts/')
    conversion_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name
