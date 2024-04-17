# ========== USER =================
 

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
