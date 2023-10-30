from django.shortcuts import render, redirect,get_object_or_404, HttpResponseRedirect
from dashboard.cms.pages.models import Page,PageSeo
from dashboard.cms.blog.models import Blogs,Categories
from dashboard.cms.blog.models import Tags
from dashboard.cms.comment.forms import BlogCommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from frontend import utils
from dashboard.cms.contactus.forms import ContactusForm
from django.http import Http404, HttpResponse 
from django.conf import settings
from django.core.mail import send_mail
from smtplib import SMTPException
from django.db import IntegrityError
from django.contrib import messages
from dashboard import setup_config
from django.utils.translation import gettext_lazy as _



def index(request):
    config = setup_config.loadConfig()
    query = request.GET.get('search')
    if config['Reading']['show_on_front']['value'] == 'Page':
        if query:
            render_data = blog_list(request)
        else:
            render_data = page_detail(request)
    if config['Reading']['show_on_front']['value'] == 'Blog':
        render_data = blog_list(request)
    return render_data


def contactus(request):
    config = setup_config.loadConfig()
    template_name=f"{setup_config.loadConfig()['Theme']['value']}/contact-us.html"
    message=""
    errors=""
    if request.method == 'POST':
        contactus_form = ContactusForm(request.POST)
        if contactus_form.is_valid():
            contactus_obj = contactus_form.save(commit=False)
            
            try:
                contactus_form.save()
            except IntegrityError as e:
                messages.warning(request,e.args[0])

            message="We've received your message and will respond within 24 hours."
            
            subject = 'W3CMS | Contact Form | A Person Want To Contact'
            email_message= f'''Name: {contactus_obj.name}\nPhone: {contactus_obj.phone}\nEmail: {contactus_obj.email}\nMessage: {contactus_obj.message}\n'''
            ReceiversList = [config['Site']['support_email']['value']]
            EmailSender = settings.EMAIL_HOST_USER
            
            try:
                send_mail(subject, email_message, EmailSender, ReceiversList, fail_silently=False)

            except SMTPException as e:
                message=""
                messages.warning(request,e)
        else:
            errors=contactus_form.errors
    
    contactus_form = ContactusForm()
    context={
        "contactus_form":contactus_form,
        "banner_title":"Contact Us",
        "message":message,
        "errors":errors
    }    
    return render(request, template_name,context)



def blog_list(request):
    template_name=f"{setup_config.loadConfig()['Theme']['value']}/index.html"
    query = request.GET.get('search')
    if query:
        print("I am in Qurery blog list")
        blogs = Blogs.objects.filter(title__icontains=query).filter(status='Published').exclude(visibility='Pr')
    else:
        blogs = Blogs.objects.filter(status='Published').exclude(visibility='Pr')
        paginator = Paginator(blogs, utils.nodes_per_page())
        blogs = paginator.get_page(request.GET.get('page'))
    
    context={
        "blogs":blogs,  
        "banner_title":"Blogs",
        "query":query    
    }
    return render(request, template_name,context)

def page_detail(request,slug='home'):
    template_name = f"{setup_config.loadConfig()['Theme']['value']}/page-detail.html"
    page_obj=None
    page_seo=None
    is_locked=None
    message=''
    banner_title=''

    if Page.objects.filter(slug=slug).exists():
        page_obj = Page.objects.get(slug=slug)
        banner_title = page_obj.title
    else:
        raise Http404

    if request.method=='POST':
        password = request.POST.get('password').strip()
        if page_obj:
            if password == page_obj.password:
                is_locked=False
            else:
                is_locked=True
                message='Password not correct'
    else:
        if page_obj and page_obj.status == 'Published':
            if page_obj.visibility=='PP':
                is_locked = True
            else:
                is_locked = False
        else:
            page_obj=None
            raise Http404
            
    if page_obj:
        page_seo = PageSeo.objects.get(page=page_obj)


    context={
        "page_obj":page_obj,
        "is_locked":is_locked,
        "message":message,
        "page_seo":page_seo,
        "banner_title":f"{banner_title}" 
    }
    return render(request, template_name,context)

def blog_detail(request,slug):
    template_name=f"{setup_config.loadConfig()['Theme']['value']}/blog-detail.html"
    instance=None
    is_locked=None
    message=''
    banner_title=''
    category_title=''
    post = get_object_or_404(Blogs, slug=slug)

    allcomments = post.comments.filter(status='approved')
    page = request.GET.get('page', 1)

    paginator = Paginator(allcomments, 20)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    user_comment = None

    if request.method == 'POST':
        comment_form = BlogCommentForm(data=request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            # user_comment.user = request.user
            user_comment.post = post
            user_comment.save()
            messages.success(request,"Comment Added Successfully")
        else:
            messages.warning(request, comment_form.errors)

        return redirect(request.path)
    else:
        comment_form = BlogCommentForm()
        
    if Blogs.objects.filter(slug=slug).exists():
        instance = Blogs.objects.get(slug=slug)
        if instance.status == 'Published':
            banner_title=instance.title
            instance.views += 1
            instance.save()
        else:
            banner_title = f"Status: {instance.status}"
                

    if request.method=='POST':
        password = request.POST.get('password').strip()
        if instance:
            if password == instance.password:
                is_locked=False
            else:
                is_locked=True
                message='Password not correct'
    else:
        if instance and instance.status == 'Published':
            if instance.visibility=='PP':
                is_locked = True
            else:
                is_locked = False
        else:
            instance = None
            message="Blog Not Found or Blog Status Not Published"
    context={
        "instance":instance,
        "is_locked":is_locked,
        "message":message,
        "banner_title":f"{banner_title}",
        "post":post,
        "comments":user_comment,
        "comments":comments,
        "allcomments": allcomments,
        'comment_form': comment_form,
    }
    return render(request,template_name,context)

##############################################--WIDGET--WIDGET--WIDGET-########################################################

#Not in use
# def widget_search(request):
#     query = request.GET.get('search')
#     template_name=f"{setup_config.loadConfig()['Theme']['value']}/index.html"
#     if query:
#         blogs = set(Blogs.objects.filter(Q(title__icontains=query) | Q(categories__title__icontains=query)))
#     else:
#         query=''
#         blogs=None
#     context={
#         "blogs":blogs,  
#         "banner_title":f"Search: {query}",
#         "query":query 
#     }
#     return render(request,template_name,context)



def month_archive(request,year,month):
    template_name=f"{setup_config.loadConfig()['Theme']['value']}/index.html"
    blogs_archive_list = None
    if year and month:
        if Blogs.objects.filter(publish_on__year=year,publish_on__month=month).exists():
            blogs_archive_list = Blogs.objects.filter(publish_on__year=year,publish_on__month=month).filter(status='Published').exclude(visibility='Pr')
    context = {
        "blogs":blogs_archive_list,
        "banner_title":f"Archive: {year} {utils.month_name.get(f'{month}')}",
    }
    return render(request,template_name,context)
    
    
def author(request,username=None):
    template_name=f"{setup_config.loadConfig()['Theme']['value']}/index.html"
    blogs=None
    if username:
        if Blogs.objects.filter(user__username=username).exists():
            blogs = Blogs.objects.filter(user__username=username).filter(status='Published').exclude(visibility='Pr')
            paginator = Paginator(blogs, utils.nodes_per_page())
            blogs = paginator.get_page(request.GET.get('page'))
        
    context={
        "blogs":blogs,  
        "banner_title":f"Author: {username}",

    }
    return render(request,template_name,context)

def blogtag(request,slug=None):
    template_name=f"{setup_config.loadConfig()['Theme']['value']}/index.html"
    blogs=None
    if slug:
        if Blogs.objects.filter(tags__slug=slug).exists():
            blogs = Blogs.objects.filter(tags__slug=slug).filter(status='Published').exclude(visibility='Pr')
            paginator = Paginator(blogs,utils.nodes_per_page())
            blogs = paginator.get_page(request.GET.get('page'))
    context={
        "blogs":blogs,  
        "banner_title":f"Tag:{slug}",

    }
    return render(request,template_name,context)

def blogcategory(request,slug=None):
    template_name=f"{setup_config.loadConfig()['Theme']['value']}/index.html"
    blogs=None
    if slug:
        if Blogs.objects.filter(categories__slug=slug).exists():
            blogs = Blogs.objects.filter(categories__slug=slug).filter(status='Published').exclude(visibility='Pr')
            paginator = Paginator(blogs, utils.nodes_per_page())
            blogs = paginator.get_page(request.GET.get('page'))
    context={
        "blogs":blogs, 
        "banner_title":f"Category: {slug}",
    }
    return render(request,template_name,context) 


