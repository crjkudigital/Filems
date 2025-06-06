import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Folder, File
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.http import FileResponse, Http404

@login_required
def secure_media_view(request, file_id):
    try:
        file_obj = File.objects.get(id=file_id)

        if file_obj.folder.user != request.user:
            raise Http404("Not allowed.")

        file_path = file_obj.file.path
        if not os.path.exists(file_path):
            raise Http404("File missing.")

        return FileResponse(open(file_path, 'rb'), as_attachment=True)

    except File.DoesNotExist:
        raise Http404("Invalid file.")
    

# Home View (lists folders belonging to the logged-in user)
class HomeView(LoginRequiredMixin, ListView):
    model = Folder
    template_name = 'index.html'
    context_object_name = 'folder'

    def get_queryset(self):
        return Folder.objects.filter(user=self.request.user)


class FileView(LoginRequiredMixin, DetailView):
    model = Folder
    template_name = 'det_files.html'
    context_object_name = 'folder'
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        folder = super().get_object(queryset)
        if folder.user != self.request.user:
            messages.error(self.request, "You do not have permission to view this folder.")
            return redirect('home')  # Replace 'home' with your actual homepage/view name
        return folder

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files'] = File.objects.filter(folder=self.object)
        return context
    

# Delete Folder View
@login_required
def delete_folder(request, pk):
    if request.method == 'POST':
        folder = get_object_or_404(Folder, pk=pk)
        folder.delete()
        messages.success(request, 'Folder deleted successfully.')
    return redirect('home')

# Delete File View
@login_required
def delete_file(request, pk):
    file = get_object_or_404(File, pk=pk)
    folder_pk = file.folder.pk
    file.delete()
    messages.success(request, 'File deleted successfully.')
    return redirect('dtfiles', pk=folder_pk)

# Copy File View
@login_required
def copy_file(request, pk):
    file = get_object_or_404(File, pk=pk)
    folder = file.folder

    # Optional: Handle duplicate file names better if needed
    File.objects.create(
        folder=folder,
        file_name=f"{file.file_name}_copy",
        file=file.file  # Reuses the same file (might be an issue if you want independent copies)
    )
    messages.success(request, 'File copied successfully.')
    return redirect('dtfiles', pk=folder.pk)

# Move File View
@login_required
def move_file(request, pk):
    file = get_object_or_404(File, pk=pk)

    if request.method == "POST":
        folder_id = request.POST.get('folder')
        new_folder = get_object_or_404(Folder, pk=folder_id, user=request.user)

        file.folder = new_folder
        file.save()

        messages.success(request, 'File moved successfully.')
        return redirect('dtfiles', pk=new_folder.pk)

    else:
        # Show list of folders the user owns to choose from
        folders = Folder.objects.filter(user=request.user)
        return render(request, 'move_file.html', {'folders': folders, 'file_pk': pk})
    


@login_required
def create_folder_view(request):
    if request.method == "POST":
        folder_name = request.POST.get('folder_name', '').strip()

        if not folder_name:
            messages.error(request, 'Folder name cannot be empty.')
        elif len(folder_name) > 100:
            messages.error(request, 'Folder name must be less than 100 characters.')
        else:
            # Correct: pass the user as well
            Folder.objects.create(user=request.user, folder_name=folder_name)
            messages.success(request, 'Folder created successfully.')
            return redirect('home')

    return render(request, 'create_folder.html')


@login_required
def add_file_view(request):
    folder_list = Folder.objects.filter(user=request.user)  # All folders (you can filter it if you want to show only the user's folders)
    
    if request.method == "POST":
        folder_id = request.POST.get('folder')  # Get the folder ID from the form
        file_name = request.POST.get('file_name', '').strip()
        uploaded_file = request.FILES.get('file')

        # Validate the inputs
        if not folder_id or not file_name or not uploaded_file:
            messages.error(request, 'Folder, file name, and file are required.')
        elif len(file_name) > 100:
            messages.error(request, 'File name must be less than 100 characters.')
        else:
            try:
                # Ensure the folder belongs to the current user
                folder = get_object_or_404(Folder, id=folder_id, user=request.user)
                
                # Create the file object
                File.objects.create(
                    folder=folder,
                    file_name=file_name,
                    file=uploaded_file
                )
                messages.success(request, 'File uploaded successfully.')
                return redirect('add_file')
            except Folder.DoesNotExist:
                messages.error(request, 'Selected folder does not exist or is not owned by you.')
            except Exception as e:
                print(e)
                messages.error(request, 'Error occurred while uploading the file.')

    return render(request, 'add_file.html', {'folder_list': folder_list})


@login_required
def search_view(request):
    query = request.GET.get('search', '')
    user = request.user
    if query:
        files = File.objects.filter(user=user, file_name__icontains=query)
        folders = Folder.objects.filter(user=user, folder_name__icontains=query)
    else:
        files = File.objects.none()
        folders = Folder.objects.none()
    return render(request, 'search.html', {
        'files': files,
        'folders': folders,
        'query': query
    })