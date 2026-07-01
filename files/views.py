import mimetypes
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.conf import settings
from django.core.files.storage import default_storage
from .models import Document
from .forms import DocumentUploadForm

def upload(request):
    success = False
    form = DocumentUploadForm()
    access_code = None
    original_filename = None

    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save()  # access_code is auto-generated in save()
            access_code = doc.access_code
            original_filename = doc.original_filename
            success = True
            messages.success(request, 'Document uploaded successfully!')
        else:
            # Pass the form errors as flash messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    context = {
        'form': form,
        'success': success,
        'access_code': access_code,
        'original_filename': original_filename,
    }
    return render(request, 'upload.html', context)


def retrieve(request):
    record = None
    access_code = request.POST.get('access_code', '').strip().upper()

    if request.method == 'POST' and access_code:
        try:
            record = Document.objects.get(access_code=access_code)
            # (Optional) update last_accessed here or in download
        except Document.DoesNotExist:
            messages.error(request, 'No document found with that access code.')

    context = {
        'record': record,
        'access_code': access_code,  # to pre‑fill the field on error
    }
    return render(request, 'retrieve.html', context)


def download(request, access_code):
    """
    Download the document matching the given access code.
    """
    doc = get_object_or_404(Document, access_code=access_code.upper())
    # Update last_accessed
    doc.update_last_accessed()

    # Get the file from storage
    file_path = doc.file.name
    if not default_storage.exists(file_path):
        raise Http404("File no longer exists.")

    # Determine content type
    content_type, _ = mimetypes.guess_type(doc.original_filename)
    if content_type is None:
        content_type = 'application/octet-stream'

    # Serve the file
    with default_storage.open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{doc.original_filename}"'
        response['Content-Length'] = doc.file.size if doc.file.size else 0
        return response