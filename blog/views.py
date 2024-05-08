from typing import Any
from django.db.models.query import QuerySet
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView,CreateView, UpdateView, DeleteView, View 
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    

class PostDetailView(DetailView):
    model = Post
    template_name= 'blog/post_detail.html'
    context_object_name = 'post'


class PostNewView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_edit.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user # This line sets the author attribute of the form's instance to the currently logged-in user
        return super().form_valid(form)  # This line calls the form_valid() method of the parent class (CreateView) to perform the default behavior of saving the form data to the database. This ensures that the form data is saved correctly after the additional processing in the overridden form_valid() method.
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk':self.object.pk})


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_edit.html'
    form_class = PostForm
    context_object_name = 'form'


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})
    
class PostDraftList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/post_draft_list.html'
    context_object_name = 'posts'


    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')
    
class PostPublishView(LoginRequiredMixin, View):


    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.publish()
        return redirect('post_detail', pk=pk)
        


class PostRemoveView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
    def delete(self):
        post = self.get_object()
        post.delete()
        return redirect(self.get_success_url())
    

class AddCommentToPostView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comment_to_post.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs['pk']})
    
class CommentApproveView(LoginRequiredMixin, View):


    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.approve()
        return redirect('post_detail', pk=comment.post.pk)


class CommentRemoveView(LoginRequiredMixin, View):


    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return redirect('post_detail', pk=comment.post.pk)
    

def custom_logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect('post_list')