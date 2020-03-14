from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.utils.http import urlencode
from django.views.generic.base import View

from webapp.forms import FileForm, SimpleSearchForm,AuthFileForm
from webapp.models import File, PrivateFile


class FileListView(ListView):

    model = File
    template_name = 'file/list.html'
    context_object_name = 'files'
    ordering = ['-created_at']
    paginate_by = 10
    paginate_orphans = 1

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(access='shared')
        if self.search_value:
            queryset = queryset.filter(
                Q(name__icontains=self.search_value)
            )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_search_form(self):
        return SimpleSearchForm(data=self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class FileDetailView(DetailView):

    model = File
    template_name = 'file/detail.html'
    context_object_name = 'file'


class FileCreateView(CreateView):

    model = File
    form_class = FileForm
    template_name = 'file/create.html'

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return AuthFileForm
        return FileForm

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user
        if not self.request.user.is_authenticated:
            form.instance.author = None
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:file_detail', kwargs={'pk': self.object.pk})

class FileUpdateView(UpdateView):

    model = File
    form_class = FileForm
    context_object_name = 'file'
    template_name = 'file/update.html'

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return AuthFileForm
        return FileForm

    def get_object(self, queryset=None):
        file = File.objects.get(pk=self.kwargs.get('pk'))
        return file

    def dispatch(self, request, *args, **kwargs):
        file = self.get_object()
        if self.request.user == file.author:
            return super().dispatch(request, *args, **kwargs)
        if not request.user.has_perm('webapp.change_file'):
            raise PermissionDenied('403 Forbidden')
        return super().dispatch(request, *args, **kwargs)



class FileDeleteView(DeleteView):

    model = File
    template_name = 'file/delete.html'
    success_url = reverse_lazy('webapp:index')

    def get_object(self, queryset=None):
        file = File.objects.get(pk=self.kwargs.get('pk'))
        return file

    def dispatch(self, request, *args, **kwargs):
        file = self.get_object()
        if self.request.user == file.author:
            return super().dispatch(request, *args, **kwargs)
        if not request.user.has_perm('webapp.delete_file'):
            raise PermissionDenied('403 Forbidden')
        return super().dispatch(request, *args, **kwargs)

class AddToPrivate(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        user = request.POST.get('username')
        file = request.POST.get('file_id')
        print(file, user)
        try:
            file = File.objects.get(pk=file)
            real_user = User.objects.get(username=user)
            private = PrivateFile.objects.get_or_create(accesed_user=real_user, file=file)
            private = private[0]
            return JsonResponse({'pk': private.pk, 'user_pk': real_user.pk,'username':real_user.username})
        except User.DoesNotExist:
            return JsonResponse({'message': 'user does not exist'})


class DeletePrivate(LoginRequiredMixin, View):
    def post(self,request):
        user = request.POST.get('user')
        file = request.POST.get('file')
        try:
            file = File.objects.get(pk=file)
            real_user = User.objects.get(pk=user)
            PrivateFile.objects.delete(accesed_user=real_user, file=file)
            return JsonResponse({'user_pk': real_user.pk})
        except User.DoesNotExist:
            return JsonResponse({'message': 'user does not exist'})