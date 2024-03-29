from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from FirstApp.forms import PostForm
from django.views.generic import DetailView
from django.views.generic import TemplateView


class Image(TemplateView):
    form = PostForm
    template_name = 'FirstApp/image.html'

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse_lazy('image_display', kwargs={'pk': obj.id}))

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ImageDisplay(DetailView):
    model = Post
    template_name = 'FirstApp/image_display.html'
    context_object_name = 'image'


def base(request):
    return render(request, 'FirstApp/base.html', data)


def post_list(request):
    posts = Post.objects.filter(
        publish_date__lte=timezone.now()).order_by('publish_date')
    return render(request, 'FirstApp/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'FirstApp/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'FirstApp/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'FirstApp/post_edit.html', {'form': form})

# Error's


def error_404_view(request, exception):
    data = {'name': 'FirstApp by Piotr Sierant'}
    return render(request, 'FirstApp/404.html', data)


def error_500_view(request):
    data = {'name': 'FirstApp by Piotr Sierant'}
    return render(request, 'FirstApp/500.html', data)
