from django import forms

class MediaUploadForm(forms.Form):
    file = forms.FileField(required=True)
    media_name = forms.CharField(max_length=255)
    media_type = forms.ChoiceField(choices=[('video', 'Video'), ('photo', 'Photo')])
    # If you need them:
    # upload_platform = forms.ChoiceField(choices=[('YouTube', 'YouTube'), ('Pinterest', 'Pinterest')])
