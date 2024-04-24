from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', args=[str(self.slug)])


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag_detail', args=[str(self.slug)])


# Author

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    registration_type = models.CharField(max_length=10, default='reader')
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    def __str__(self):
        return self.user.username
    

from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import slugify

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    published_at = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    featured_image = models.ImageField(upload_to='images/', null=True, blank=True)
    youtube_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title
        if not self.meta_description:
            self.meta_description = self.content[:160]  # Limiting to 160 characters for meta description
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-published_at']

    @property
    def related_posts(self):
        return Post.objects.filter(categories__in=self.categories.all()).exclude(id=self.id)[:3]

    def get_seo_title(self):
        return f"{self.title} - Your Blog Name"



# Blogpost with SEO content

from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    publish_date = models.DateField()
    tags = models.CharField(max_length=200)
    
    # SEO Fields
    meta_title = models.CharField(max_length=200)
    meta_description = models.CharField(max_length=250)
    meta_keywords = models.CharField(max_length=250)
    og_title = models.CharField(max_length=200)
    og_description = models.CharField(max_length=250)
    og_image = models.URLField()
    og_type = models.CharField(max_length=50)
    robots = models.CharField(max_length=100)
    contributor = models.CharField(max_length=100)
    yandex_verification = models.CharField(max_length=100)
    msvalidate = models.CharField(max_length=100)
    copyright = models.CharField(max_length=100)
    viewport = models.CharField(max_length=100)
    content_type = models.CharField(max_length=100)
    ua_compatible = models.CharField(max_length=100)
    theme_color = models.CharField(max_length=50)
    navbutton_color = models.CharField(max_length=50)
    mobile_web_app_capable = models.CharField(max_length=10)
    apple_mobile_web_app_capable = models.CharField(max_length=10)

    def __str__(self):
        return self.title
