from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
]


urlpatterns = [
    path('post/create/', views.post_create, name='post_create'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/update/', views.post_update, name='post_update'),
    path('post/<slug:slug>/delete/', views.post_delete, name='post_delete'),
]


urlpatterns = [
    path('category/create/', views.create_category, name='category_create'),
    path('category/<slug:slug>/delete/', views.delete_category, name='category_delete'),
]

urlpatterns = [
    path('tag/create/', views.create_tag, name='tag_create'),
    path('tag/<slug:slug>/delete/', views.delete_tag, name='tag_delete'),
]



# ================== Admin Section ==================


from django.urls import path
from . import views

app_name = 'admin_app'

urlpatterns = [
    # User Management URLs
    path('admin/users/', views.user_list, name='admin_user_list'),
    path('admin/user/<int:user_id>/', views.user_profile, name='admin_user_profile'),
    path('admin/user/<int:user_id>/verify/', views.verify_user, name='admin_verify_user'),

    # Post Management URLs
    path('admin/posts/', views.post_list, name='admin_post_list'),
    path('admin/post/<int:post_id>/', views.post_view, name='admin_post_view'),
    path('admin/post/<int:post_id>/remove-comments/', views.remove_comments, name='admin_remove_comments'),

    # Visitor Analytics URLs
    path('admin/analytics/visitors-count/', views.visitors_count_graph, name='admin_visitors_count_graph'),
    path('admin/analytics/visitors-country/', views.visitors_country_list, name='admin_visitors_country_list'),
]



# create an admin app in django to monitor
# 1. user list, view user profile, verify user
# 2. view post list, post view, remove if any unwonted comments in the post
# 3. total visitors count in the website as a graph with date
# 4. visitors country list

# i need to create a url.py for this sections first