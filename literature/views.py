from django.shortcuts import render, get_object_or_404, redirect
from .models import Literature, Attachment, Project
from .forms import ImportForm, LiteratureForm, AttachmentForm, ProjectForm
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib import messages
import os,csv,tempfile
from django.core.files.storage import FileSystemStorage
import os

def literature_list(request):
    literatures = Literature.objects.all()
    return render(request, 'literature/literature_list.html', {'literatures': literatures})

def literature_create(request):
    if request.method == 'POST':
        form = LiteratureForm(request.POST)
        if form.is_valid():
            literature = form.save()
            return redirect('literature:literature_detail', pk=literature.pk)
    else:
        form = LiteratureForm()
    return render(request, 'literature/literature_form.html', {'form': form})


def literature_update(request, pk):
    literature = get_object_or_404(Literature, pk=pk)
    if request.method == 'POST':
        form = LiteratureForm(request.POST, instance=literature)
        if form.is_valid():
            form.save()
            return redirect('literature:literature_detail', pk=literature.pk)
    else:
        form = LiteratureForm(instance=literature)
    return render(request, 'literature/literature_form.html', {'form': form})

def literature_delete(request, pk):
    literature = get_object_or_404(Literature, pk=pk)
    if request.method == 'POST':
        literature.delete()
        return redirect('literature:literature_list')
    return render(request, 'literature/literature_confirm_delete.html', {'literature': literature})

def literature_detail(request, pk):
    literature = get_object_or_404(Literature, pk=pk)
    attachments = literature.attachment_set.all()
    
    if request.method == "POST":
        if 'delete_attachment' in request.POST:
            attachment_id = request.POST['delete_attachment']
            attachment = Attachment.objects.get(pk=attachment_id)
            # 获取附件的文件路径
            attachment_file_path = attachment.file.path
            # 删除附件
            attachment.delete()
            # 检查文件夹是否为空，如果为空则删除文件夹
            folder_path = os.path.dirname(attachment_file_path)
            if not os.listdir(folder_path):  # 如果文件夹为空
                os.rmdir(folder_path)
            return redirect('literature:literature_detail', pk=literature.pk)
            
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.literature = literature
            attachment.save()
            return redirect('literature:literature_detail', pk=literature.pk)
    else:
        form = AttachmentForm()
    return render(request, 'literature/literature_detail.html', {'literature': literature, 'attachments': attachments, 'form': form})

def upload_attachment(request, pk):
    literature = get_object_or_404(Literature, pk=pk)
    if request.method == "POST":
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.literature = literature
            attachment.save()
            return redirect('literature_detail', pk=literature.pk)
    else:
        form = AttachmentForm()
    return render(request, 'literature/upload_attachment.html', {'form': form, 'literature': literature})

@receiver(post_delete, sender=Attachment)
def delete_attachment_file(sender, instance, **kwargs):
    # 删除文件系统中的附件文件
    instance.file.delete(save=False)

def import_literature_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if 'Title' in row and row['Title']:
                title = row['Title']
                doi = row.get('DOI', '')  # 注意此处使用 'doi'
                
                # 检查是否存在项目信息，如果存在则关联到文献上
                project_name = row.get('project', '')  # 假设项目信息在CSV中的字段名为 'project'
                if project_name:
                    project, _ = Project.objects.get_or_create(name=project_name)

                # 检查数据库中是否已存在相同的 DOI
                if Literature.objects.filter(doi=doi).exists():
                    print(f"Skipping row with existing DOI: {doi}")
                    continue
                
                # 创建新的 Literature 实例并保存
                literature = Literature(
                    title=title,
                    journal_abbr=row.get('journal_abbr', ''),
                    publication_year=row.get('publication_year', ''),
                    doi=doi
                )
                              
                literature.save()
                literature.projects.set([project])
            else:
                print("Skipping row with empty title:", row)


def literature_import(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        file_path = os.path.join(fs.location, filename)
        import_literature_from_csv(file_path)
        fs.delete(filename)  # 删除临时文件
        return redirect('literature_list')
    return render(request, 'literature/literature_import.html')
