#literature/forms.py

from django import forms
from .models import Literature, Attachment, Project

class LiteratureForm(forms.ModelForm):
    class Meta:
        model = Literature
        fields = ['title', 'journal_abbr', 'publication_year', 'doi', 'projects']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'journal_abbr': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Journal Abbr'}),
            'publication_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Publication Year'}),
            'doi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DOI'}),
            'projects': forms.CheckboxSelectMultiple(attrs={'class': 'ms-3'})
        }


        

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file', 'description']  
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Description'}),
            'file': forms.ClearableFileInput(attrs={}),
        }


#    def clean_file(self):
#        file = self.cleaned_data['file']
#        # 文件大小不能超过10MB
#        if file.size > 10 * 1024 * 1024:
#            raise forms.ValidationError("File size cannot exceed 10MB.")
#        # 仅允许上传PDF和文本文件
#        content_type = file.content_type
#        if content_type not in ['application/pdf', 'text/plain']:
#            raise forms.ValidationError("Only PDF and plain text files are allowed.")
#        return file
    
class ImportForm(forms.Form):
    file = forms.FileField(label='Select a CSV file')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Project Name'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}),
        }