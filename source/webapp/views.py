from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from webapp.forms import FileForm
from webapp.models import File


class FileListView(ListView):

    model = File
    template_name = 'file/list.html'
    context_object_name = 'files'
    ordering = ['-created_at']


class FileDetailView(DetailView):

    model = File
    template_name = 'file/detail.html'
    context_object_name = 'file'


class FileCreateView(CreateView):

    model = File
    form_class = FileForm
    template_name = 'file/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        print('yeds')
        return reverse('webapp:announce_detail', kwargs={'pk': self.object.pk})

class FileUpdateView(UpdateView):

    model = File
    form_class = FileForm
    context_object_name = 'announcement'
    template_name = 'file/update.html'

    def get_success_url(self):
        return reverse('webapp:announce_detail', kwargs={'pk': self.object.pk})



class FileDeleteView(DeleteView):

    model = File
    template_name = 'file/delete.html'
    success_url = reverse_lazy('webapp:index')
