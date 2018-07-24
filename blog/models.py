from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

def upload_location(instance,filename):
    return f"{instance.id}/{filename}"

class Blog(models.Model):

    CATEGORY_CHOICES = (
        ('tn', 'Technology'),
        ('en', 'Entrepreneurship'),
        ('ds', 'Design'),
        ('cl', 'Culture'),
        ('sl', 'self'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1,on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    image= models.ImageField(upload_to=upload_location,null=True,blank=True,width_field="width_field",height_field="height_field")
    height_field =models.IntegerField(default=0,null=True)
    width_field = models.IntegerField(default=0,null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default='General',
    )


    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.title
    class Meta:
        ordering =["-timestamp","-updated"]
    @property
    def get_content_type(self):
        instance=self
        content_type=ContentType.objects.get_for_model(instance.__class__)
        return content_type

class Comment(models.Model):
    user_comment = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    parent=models.ForeignKey("self",null=True,on_delete=models.CASCADE)
    content = models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.user_comment.username)
    def __str__(self):
       return str(self.user_comment.username)
    class Meta:
        ordering =["-timestamp"]
    def children(self):
        return Comment.objects.filter(parent=self)
    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True