from django import forms
from django.core.exceptions import ValidationError
from .models import Document

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'email', 'description', 'file']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'field-input',
                'placeholder': 'Jane Doe'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'field-input',
                'placeholder': 'jane@example.com'
            }),
            'description': forms.Textarea(attrs={
                'class': 'field-input field-textarea',
                'rows': 4,
                'placeholder': 'Briefly describe the document…'
            }),
            'file': forms.FileInput(attrs={
                'class': 'file-input',
                'accept': '.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.txt,.png,.jpg,.jpeg,.gif,.zip,.rar,.7z'
            }),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            max_size = 1024 * 1024 * 1024  # 1 GB
            if file.size > max_size:
                raise ValidationError(f"File size must be under {max_size // (1024**2)} MB.")
        return file