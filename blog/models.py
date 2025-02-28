from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property  # Cache decorator
from django.template.loader import render_to_string  # Rendering the template
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Category(models.Model):
    """ blog category """
    name = models.CharField(max_length=32, verbose_name="name")
    desc = models.TextField(max_length=200, blank=True, default='', verbose_name="description")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="add date")
    pub_date = models.DateTimeField(auto_now=True, verbose_name="publish date")

    class Meta:
        verbose_name = "blog category"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Tag(models.Model):
    """ article tag """
    name = models.CharField(max_length=10, verbose_name="tag name")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="add date")
    pub_date = models.DateTimeField(auto_now=True, verbose_name="publish date")

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    """ Post """
    title = models.CharField(max_length=61, verbose_name="title")
    desc = models.TextField(max_length=200, blank=True, default='', verbose_name="description")
    category = models.ForeignKey(Category,on_delete=models.CASCADE, verbose_name="category")
    content = RichTextUploadingField()
    tags = models.ForeignKey(Tag, blank=True, null=True, on_delete=models.CASCADE, verbose_name="tag")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="author")
    is_hot = models.BooleanField(default=False, verbose_name="if the article is popular")
    pv = models.IntegerField(default=0, verbose_name="page view")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="add date")
    pub_date = models.DateTimeField(auto_now=True, verbose_name="publish date")

    class Meta:
        verbose_name = "article"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class Sidebar(models.Model):

    STATUS = (
        (1, 'hide'),
        (2, 'display')
    )

    DISPLAY_TYPE = (
        (1, 'search'),
        (2, 'create a new post'),
        (3, 'Latest Articles'),
        (4, 'Hot Articles'),
        (5, 'Article Archives'),
    )

    title = models.CharField(max_length=50, verbose_name="Module Name")
    display_type = models.PositiveIntegerField(default=1, choices=DISPLAY_TYPE, verbose_name="Display type")
    content = models.CharField(max_length=500, blank=True, default='', verbose_name="content", help_text="If the type is not HTML, it can be null")
    sort = models.PositiveIntegerField(default=1, verbose_name="sort", help_text='The larger the number, the higher the number')
    status = models.PositiveIntegerField(default=2, choices=STATUS, verbose_name="status")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="add date")

    class Meta:
        verbose_name = "Sidebar"
        verbose_name_plural = verbose_name
        ordering = ['-sort']

    def __str__(self):
        return self.title

    @classmethod
    def get_sidebar(cls):
        return cls.objects.filter(status=2)

    @property
    def get_content(self):
        if self.display_type == 1:
            context = {

            }
            return render_to_string('blog/sidebar/search.html', context=context)
        elif self.display_type == 2:
            context = {

            }
            return render_to_string('blog/sidebar/create.html', context=context)
        elif self.display_type == 3:
            context = {

            }
            return render_to_string('blog/sidebar/new_post.html', context=context)
        elif self.display_type == 4:
            context = {

            }
            return render_to_string('blog/sidebar/hot_post.html', context=context)
        elif self.display_type == 5:
            context = {

            }
            return render_to_string('blog/sidebar/archives.html', context=context)



