from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='home'),
    path('post/',views.post,name='post'),
    path('details/<int:id>',views.details,name='details'),
    path('delete/<int:id>',views.delete,name="delete"),
    path('edit/<int:id>',views.edit,name='edit'),
    path('delete_comment/<int:id>',views.deleteComment,name='delete_comment'),
    path('edit_comment/<int:id>',views.editComment,name='edit_comment'),
]