from django.shortcuts import render, get_object_or_404, redirect
from literature.models import Project
from literature.forms import ProjectForm

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project/project_list.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'project/project_detail.html', {'project': project})

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return redirect('project:project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'project/project_form.html', {'form': form})

def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project:project_detail', pk=pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project/project_form.html', {'form': form, 'project': project})

def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('project:project_list')
    return render(request, 'project/project_confirm_delete.html', {'project': project})
