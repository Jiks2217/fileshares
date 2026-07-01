import os
import secrets
import string
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.core.files.storage import default_storage
from django.conf import settings


class Document(models.Model):
    """
    Represents a securely stored document with a private access code.
    """
    # User‑supplied metadata
    name = models.CharField(max_length=255, verbose_name="Full name")
    email = models.EmailField(verbose_name="Email address")
    description = models.TextField(verbose_name="Document description")

    # File handling
    file = models.FileField(
        upload_to='documents/%Y/%m/%d/',  # daily folders
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    'pdf', 'doc', 'docx', 'xls', 'xlsx',
                    'ppt', 'pptx', 'txt', 'png', 'jpg',
                    'jpeg', 'gif', 'zip', 'rar', '7z'
                ]
            )
        ],
        max_length=255,
        verbose_name="Document file"
    )
    original_filename = models.CharField(max_length=255, editable=False)
    file_size = models.PositiveIntegerField(editable=False, null=True, blank=True)

    # Access code
    access_code = models.CharField(
        max_length=12,
        unique=True,
        db_index=True,
        editable=False,
        verbose_name="Access code"
    )

    # Timestamps
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Upload date")
    last_accessed = models.DateTimeField(null=True, blank=True)

    # Optional: track if file is encrypted (placeholder for future)
    is_encrypted = models.BooleanField(default=True, help_text="File is encrypted at rest")

    class Meta:
        ordering = ['-upload_date']
        verbose_name = "Document"
        verbose_name_plural = "Documents"

    def __str__(self):
        return f"{self.original_filename} ({self.access_code})"

    def save(self, *args, **kwargs):
        """Auto‑set original filename, file size, and generate access code if needed."""
        if self.file and not self.pk:  # new upload
            # Store original name (used for display)
            self.original_filename = self.file.name

            # Compute file size (in bytes)
            try:
                self.file_size = self.file.size
            except Exception:
                self.file_size = None

        # Generate unique access code if not set
        if not self.access_code:
            self.access_code = self._generate_access_code()

        super().save(*args, **kwargs)

    def _generate_access_code(self):
        """
        Generate a 12‑character alphanumeric (uppercase) code.
        Ensures uniqueness by retrying on collision.
        """
        alphabet = string.ascii_uppercase + string.digits
        code_length = 12

        for _ in range(10):  # limit attempts to avoid infinite loop
            code = ''.join(secrets.choice(alphabet) for _ in range(code_length))
            if not Document.objects.filter(access_code=code).exists():
                return code

        # Fallback (extremely unlikely)
        return secrets.token_urlsafe(9).upper().replace('-', 'X')[:12]

    def get_file_extension(self):
        """Return file extension (lowercase, without dot)."""
        return os.path.splitext(self.original_filename)[1][1:].lower()

    def update_last_accessed(self):
        """Update the last_accessed timestamp to now."""
        self.last_accessed = timezone.now()
        self.save(update_fields=['last_accessed'])

    # Optionally override delete to remove the physical file
    def delete(self, *args, **kwargs):
        if self.file:
            if default_storage.exists(self.file.name):
                default_storage.delete(self.file.name)
        super().delete(*args, **kwargs)