from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Media
from .forms import MediaUploadForm

@login_required
def dashboard(request):
    user_media = Media.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'media_items': user_media,
        'form': MediaUploadForm()
    }
    return render(request, 'dashboard.html', context)

@login_required
def upload_media(request):
    if request.method == 'POST':
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.user = request.user
            media.save()
            
            # Call platform specific upload function
            if media.media_type == 'video':
                # Import and call video upload function
                pass
            elif media.media_type == 'image':
                # Import and call image upload function
                pass
                
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)