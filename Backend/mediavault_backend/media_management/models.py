from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Media(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media_name = models.CharField(max_length=255)
    media_type = models.CharField(max_length=50)  # video, photo, etc.
    upload_platform = models.CharField(max_length=100)  # YouTube, Pinterest, etc.
    upload_status = models.CharField(max_length=50, default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    media_url = models.URLField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Media'