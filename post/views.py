from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from . forms import MakePost
from . models import *
from django.db.models import Count
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    # post = Post.objects.all().order_by('-created_at')
    # count each comments
    search = request.GET.get('search')
    post = Post.objects.annotate(total_comments=Count('comments')).order_by('-created_at') 
    # serach 
    if search:
        post = post.filter(title__icontains=search)

    # Pagination
    paginator = Paginator(post, 4)  # Show 4 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request,'index.html',{'post':posts})

# post new data
# @login_required(login_url='login')
# def post(request):
#     form = MakePost()
#     if request.method == 'POST':
#         form = MakePost(request.POST,request.FILES)
#         if form.is_valid():
#             print(form)
#             form.save()
#             form = MakePost()
#             return redirect('home')    
#     return render(request,'post.html',{"form":form})

@login_required(login_url='login')
def post(request):
    if request.method == "POST":
        
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        Post.objects.create(
            title =title,
            content = content,
            image = image,
            created_user = request.user
        )
        return redirect('home')

    return render(request,'post.html')
    

# // Show details
def details(request,id):
    try:
        post = Post.objects.get(id=id)
    except:
        post = None

    if request.method == "POST":
        comment = request.POST.get('comment')
        if comment:
            Comments.objects.create(
                comment_text = comment,
                comment_auther = request.user,
                blog_data = post
            )
        return HttpResponseRedirect(reverse('details',args=[id]))    
    comments = Comments.objects.filter(blog_data=post)
    context = {
               'edit':False,
               'post':post,
               'comments':comments}
    return render(request,'details.html',context)




# // delete data
def delete(request,id):
    try:
        post = Post.objects.get(id=id)
    except:
        post = None  

    # check user  is login
    if request.user != post.created_user:
        return HttpResponse('you are not autherize to view this page !!!')

    if request.method == 'POST':
        post.delete()
        return redirect('home')
    
# // edit data
def edit(request,id):
    try:
        post = Post.objects.get(id=id)
    except:
        post:None
    # check user is login
    if request.user != post.created_user:
        return HttpResponse('you are not autherize to view this page !!!')
    
    form = MakePost(instance=post)
    if request.method == "POST":
        form = MakePost(request.POST,request.FILES,instance=post)
        if form.is_valid():
            form.save()
            return redirect('details',id=post.id)
    return render(request,'edit.html',{'form':form})    


def deleteComment(request,id):
    comment = Comments.objects.get(id=id)
    blog_id = comment.blog_data.id
    print(blog_id)
    comment.delete()
    return redirect('details',id=blog_id)

def editComment(request,id):
    comment = Comments.objects.get(id=id)
    blog = comment.blog_data
    if request.method == "POST":
        text = request.POST.get('comment')
        comment.comment_text = text
        comment.save()
        return redirect('details',blog.id)
    comments = Comments.objects.filter(blog_data=blog) 

    context = {
               'edit':True,
               'edit_comment':comment,
               'post':blog,
               'comments':comments
               }

    return render(request,'details.html',context)
