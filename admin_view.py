from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, User, Comment

# User Management Views
def user_list(request):
    users = User.objects.all()
    return render(request, 'admin/user_list.html', {'users': users})

def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'admin/user_profile.html', {'user': user})

def verify_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.verified = True
    user.save()
    return redirect('admin_user_list')

# Post Management Views
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'admin/post_list.html', {'posts': posts})

def post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'admin/post_view.html', {'post': post})

def remove_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.comments.all().delete()
    return redirect('admin_post_view', post_id=post_id)

# Visitor Analytics Views
def visitors_count_graph(request):
    # Implement visitor count graph logic
    return render(request, 'admin/visitors_count_graph.html')

def visitors_country_list(request):
    # Implement visitor country list logic
    return render(request, 'admin/visitors_country_list.html')
