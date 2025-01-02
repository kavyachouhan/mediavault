from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Media(models.Model):
    MEDIA_TYPES = (
        ('video', 'Video'),
        ('image', 'Image'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    platform_url = models.URLField(blank=True)
    # file = models.FileField(upload_to='temp_uploads/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_processed = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Media'