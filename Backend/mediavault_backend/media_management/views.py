from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Media
from .forms import MediaUploadForm

@login_required
def dashboard(request):
    # Order by the most recent `uploaded_at` field
    user_media = Media.objects.filter(user=request.user).order_by('-uploaded_at')
    context = {
        'media_items': user_media,
        'form': MediaUploadForm()  # Pass an instance of our plain Form
    }
    return render(request, 'dashboard.html', context)

@login_required
def upload_media(request):
    if request.method == 'POST':
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Because we're using a plain Form (not a ModelForm),
            # we manually create the Media record.
            media_name = form.cleaned_data['media_name']
            media_type = form.cleaned_data['media_type']
            uploaded_file = form.cleaned_data['file']

            # Create a new Media object with the metadata
            media_obj = Media.objects.create(
                user=request.user,
                media_name=media_name,
                media_type=media_type,
                upload_platform='',  # or set default if you like
                upload_status='pending',
                media_url=''  # will be filled in after external upload
            )

            # Call your platform-specific upload logic here
            # Example:
            if media_type == 'video':
                # from platform_integration.youtube_service import upload_video_to_youtube
                # video_url = upload_video_to_youtube(uploaded_file)
                # media_obj.media_url = video_url
                # media_obj.upload_status = 'uploaded'
                pass
            elif media_type == 'photo':
                # from platform_integration.pinterest_service import upload_image_to_pinterest
                # image_url = upload_image_to_pinterest(uploaded_file)
                # media_obj.media_url = image_url
                # media_obj.upload_status = 'uploaded'
                pass

            # Finally save any changes to the Media object
            media_obj.save()

            return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)
