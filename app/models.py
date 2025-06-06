import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.CharField(max_length=50, unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    folder_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.folder_name

class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    id = models.CharField(max_length=50, unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='files')
    add_new_folder = models.CharField(max_length=100, null=True, blank=True)
    file_name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    file = models.FileField(upload_to='folder/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    def __str__(self):
        return self.file_name