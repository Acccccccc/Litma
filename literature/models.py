# literature/models.py
import os
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils import timezone

def attachment_upload_path(instance, filename):
    # Replace '/' with '_' in DOI
    doi_safe = instance.literature.doi.replace('/', '_')
    # Return the upload path
    return os.path.join('literature', doi_safe, filename)

class Journal(models.Model):
    journal_fullname = models.CharField(max_length=200)
    journal_abbr = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.journal_fullname

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class Literature(models.Model):
    title = models.CharField(max_length=200)
    journal_abbr = models.CharField(max_length=100, blank=True)
    publication_year = models.CharField(max_length=10, blank=True, null=True)
    doi = models.CharField(max_length=200, unique=True)
    journal = models.ForeignKey(Journal, on_delete=models.SET_NULL, null=True, blank=True)
    projects = models.ManyToManyField(Project, related_name='literatures', null=True, blank=True)


    
    def save(self, *args, **kwargs):
        # Check if the journal exists, if not create it
        if self.journal_abbr:
            journal, created = Journal.objects.get_or_create(
                journal_abbr=self.journal_abbr,
                defaults={'journal_fullname': self.journal_abbr}  # You can adjust this logic as needed
            )
            self.journal = journal
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.attachment_set.all().delete()
        #if self.file:
        #    if os.path.isfile(self.file.path):
        #        os.remove(self.file.path)
        super().delete(*args, **kwargs)

    def has_attachments(self):
        """
        Check if the literature has any attachments.
        """
        return self.attachment_set.exists()

    def __str__(self):
        return self.title

class Attachment(models.Model):
    literature = models.ForeignKey(Literature, on_delete=models.CASCADE)
    file = models.FileField(upload_to=attachment_upload_path)
    uploaded_at = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=200, null=True, blank=True)  # 添加了一个描述字段

    def __str__(self):
        return self.file.name
    
