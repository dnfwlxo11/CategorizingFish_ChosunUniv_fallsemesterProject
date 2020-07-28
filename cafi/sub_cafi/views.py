from django.shortcuts import render
from .forms import UploadForm
from django.shortcuts import redirect

# Create your views here.

def index(request):
    return render(request, 'sub_cafi/index.html', {})

def image_list(request):
    return render(request, 'sub_cafi/list.html', {})

def upload_image(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('image_list')
    else:
        form = UploadForm()
    
    return render(request, 'sub_cafi/upload.html', {
        'form':form
    })