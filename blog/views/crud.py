from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render,get_object_or_404
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q



# Create your views here.
from blog.forms.createBlog import BlogForm
from blog.forms.comments import CommentForms

from blog.models import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render






def blogs_create(request):

    if not request.user.is_authenticated:
        #raise Http404
        return HttpResponseRedirect('/login/')
    quote="Create Blog"
    button ="Create Blog"
    form = BlogForm(request.POST or None ,request.FILES or None)
    if form.is_valid():

        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request,"Successfully created !")
        return HttpResponseRedirect('/blogs/')

    context = {
        "form":form,
        "quote":quote,
        "b": button,
    }
    return render(request,"blog_form.html",context)

def blogs_detail(request,pk= None): #one particular blog
    instance = get_object_or_404(Blog,id=pk)
    initial_data={
        "content_type":instance.get_content_type,
        "object_id":instance.id
    }
    form=CommentForms(request.POST or None,initial=initial_data)
    if form.is_valid():
        c_type=form.cleaned_data.get("content_type")
        content_type=ContentType.objects.get(model=c_type)
        obj_id=form.cleaned_data.get('object_id')
        content_data=form.cleaned_data.get("content")
        parent_obj=None
        try:
           parent_id=int(request.POST.get("parent_id"))
        except:
            parent_id=None
        if parent_id:
            parent_qs=Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count()==1:
                parent_obj=parent_qs.first()
        new_comment =Comment.objects.get_or_create(
            user_comment=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        return HttpResponseRedirect('/blogs/' + str(pk) + '/')


    content_type = ContentType.objects.get_for_model(Blog)
    obj_id=instance.id
    comments =Comment.objects.filter(content_type=content_type,object_id=obj_id).filter(parent=None)
    context = {

        "title": instance.title,
        "instance":instance,
        "comments":comments,
        "comment_form":form,

    }
    return render(request, "blog_detail.html", context)
def blogs_list(request):#list of all blogs
    query_set_list = Blog.objects.all()#.order_by("-timestamp")

    query = request.GET.get("q")
    if query:
        query_set_list = query_set_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)

        ).distinct()

    paginator = Paginator(query_set_list, 5)  # Show 25 contacts per page
    page_request_var='page'
    page = request.GET.get(page_request_var)
    query_set = paginator.get_page(page)
    context = {
        "object_list" : query_set,
        "title": "NewMeans",
        "page_request_var":page_request_var

    }
    return render(request, "blog_list.html", context)
def blogs_category(request,spk=None):
    query_set_list = Blog.objects.all()
    query_set_list=query_set_list.filter(category=spk)

    query = request.GET.get("q")
    if query:
        query_set_list = query_set_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)

        ).distinct()

    paginator = Paginator(query_set_list, 2)
    page_request_var='page'
    page = request.GET.get(page_request_var)
    query_set = paginator.get_page(page)
    context = {
        "object_list" : query_set,
        "title": "Blogs",
        "page_request_var":page_request_var,
        "genre":spk,
    }
    return render(request, "blog_list.html", context)

def blogs_update(request, pk=None ):
    if not request.user.is_authenticated:
        raise Http404

    instance = get_object_or_404(Blog, id=pk)
    if not instance.user_id == request.user.id:
        raise Http404
    quote = "Update Blog"
    button="Update and Save"
    form = BlogForm(request.POST or None,request.FILES or None,instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Updated and Saved !")

        return HttpResponseRedirect('/blogs/' + str(pk) + '/')
    context = {

        "title": instance.title,
        "instance": instance,
        "form":form,
        "quote":quote,
        "b":button,

    }
    return render(request, "blog_form.html",context)
def blogs_delete(request,pk=None):
    if not request.user.is_authenticated:
        raise Http404
    instance = get_object_or_404(Blog,id=pk)
    if not instance.user_id == request.user.id:
        raise Http404
    instance.delete()
    messages.success(request,"Successfully deleted")
    return HttpResponseRedirect('/blogs/')
