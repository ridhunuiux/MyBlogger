# ++++++++++++++++++++++++++++++++
#           Register 
# ++++++++++++++++++++++++++++++++


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Author

def register_author(request):
    if request.method == 'POST':
        # Extract data from the POST request
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        profile_name = request.POST['profile_name']
        contact_number = request.POST['contact_number']
        bio = request.POST['bio']
        designation = request.POST.get('designation', '')
        facebook_url = request.POST.get('facebook_url', '')
        twitter_url = request.POST.get('twitter_url', '')
        linkedin_url = request.POST.get('linkedin_url', '')
        registration_type = request.POST['registration_type']  # Extract registration type

        # Extract profile image if provided
        profile_image = request.FILES.get('profile_image')

        # Check if email or contact number already exists
        if User.objects.filter(email=email).exists() or Author.objects.filter(contact_number=contact_number).exists():
            error_message = "User with the same email or contact number already exists."
            return render(request, 'registration_form.html', {'error_message': error_message})

        # Create a new user
        user = User.objects.create_user(username=username, password=password, email=email)

        if registration_type == 'author':
            # Create a corresponding author profile
            author = Author.objects.create(
                user=user,
                profile_name=profile_name,
                contact_number=contact_number,
                bio=bio,
                designation=designation,
                facebook_url=facebook_url,
                twitter_url=twitter_url,
                linkedin_url=linkedin_url,
                profile_image=profile_image
            )
            # Redirect to a success page or homepage
            return redirect('author_success_page')  # Change 'author_success_page' to the actual URL name for author registration success
        else:
            # Redirect to a success page or homepage for reader registration
            return redirect('reader_success_page')  # Change 'reader_success_page' to the actual URL name for reader registration success

    return render(request, 'registration_form.html')  # Change 'registration_form.html' to the actual template name



# ++++++++++++++++++++++++++++++++
#           Login 
# ++++++++++++++++++++++++++++++++


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful login, change to appropriate URL
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')  # Redirect back to the login page with an error message
    return render(request, 'login.html')





# ++++++++++++++++++++++++++++++++
#           Category 
# ++++++++++++++++++++++++++++++++


from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Category

def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        if name and slug:
            # Check if the selected category already exists
            existing_category = Category.objects.filter(name=name).first()
            if existing_category:
                return redirect('category_detail', slug=existing_category.slug)  # Redirect to category detail if category already exists

            # If the selected category does not exist, create a new category
            category = Category.objects.create(name=name, slug=slug)
            return redirect('category_detail', slug=category.slug)  # Redirect to category detail for the new category
        else:
            error_message = "Please provide both name and slug for the category."
            return render(request, 'create_category.html', {'error_message': error_message})
    return render(request, 'create_category.html')


def delete_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        category.delete()
        return redirect('home')  # Redirect to home page after deletion, change to appropriate URL
    return render(request, 'delete_category.html', {'category': category})





# ++++++++++++++++++++++++++++++++
#           Tag 
# ++++++++++++++++++++++++++++++++


from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Tag

def create_tag(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        if name and slug:
            # Check if the tag already exists
            existing_tag = Tag.objects.filter(name=name).first()
            if existing_tag:
                return redirect('tag_detail', slug=existing_tag.slug)  # Redirect to tag detail if tag already exists

            # If the tag does not exist, create a new tag
            tag = Tag.objects.create(name=name, slug=slug)
            return redirect('tag_detail', slug=tag.slug)  # Redirect to tag detail for the new tag
        else:
            error_message = "Please provide both name and slug for the tag."
            return render(request, 'create_tag.html', {'error_message': error_message})
    return render(request, 'create_tag.html')

def delete_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    if request.method == 'POST':
        tag.delete()
        return redirect('home')  # Redirect to home page after deletion, change to appropriate URL
    return render(request, 'delete_tag.html', {'tag': tag})



# ++++++++++++++++++++++++++++++++
#           POST 
# ++++++++++++++++++++++++++++++++


from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from .models import Post, Author, Category, Tag
from django.utils.text import slugify

def post_create(request):
    if request.method == 'POST':
        # Extract data from the POST request
        title = request.POST.get('title')
        content = request.POST.get('content')
        meta_title = request.POST.get('meta_title')
        meta_description = request.POST.get('meta_description')
        published_at = request.POST.get('published_at')
        author_id = request.POST.get('author')
        category_ids = request.POST.getlist('categories')
        tag_ids = request.POST.getlist('tags')
        featured_image = request.FILES.get('featured_image')
        youtube_link = request.POST.get('youtube_link')

        # Get author object
        author = Author.objects.get(id=author_id)

        # Create post object
        post = Post.objects.create(
            title=title,
            content=content,
            meta_title=meta_title,
            meta_description=meta_description,
            published_at=published_at,
            author=author,
            featured_image=featured_image,
            youtube_link=youtube_link
        )

        # Set slug
        post.slug = slugify(title)

        # Add categories and tags
        post.categories.add(*category_ids)
        post.tags.add(*tag_ids)

        # Save post object
        post.save()

        return redirect('post_detail', slug=post.slug)  # Redirect to post detail page

    authors = Author.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'post_create.html', {'authors': authors, 'categories': categories, 'tags': tags})




def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})



def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'post_detail.html', {'post': post})




def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        # Extract data from the POST request
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.meta_title = request.POST.get('meta_title')
        post.meta_description = request.POST.get('meta_description')
        post.published_at = request.POST.get('published_at')
        post.author_id = request.POST.get('author')
        post.category_ids = request.POST.getlist('categories')
        post.tag_ids = request.POST.getlist('tags')
        post.featured_image = request.FILES.get('featured_image')
        post.youtube_link = request.POST.get('youtube_link')

        # Save the updated post object
        post.save()
        return redirect('post_detail', slug=post.slug)  # Redirect to post detail page
    
    authors = Author.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'post_update.html', {'post': post, 'authors': authors, 'categories': categories, 'tags': tags})




def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        post.delete()
        return redirect('home')  # Redirect to home page after deletion, change to appropriate URL
    return render(request, 'post_delete.html', {'post': post})
