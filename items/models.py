from django.db import models
from django.utils import timezone
from django.utils.timezone import make_aware
import datetime
from accounts.models import User


class Item(models.Model):
    thumbnail = models.ImageField(upload_to='images/thumbnails/', default="images/thumbnails/no_image.png")
    comment = models.CharField(max_length=50)# verbose_name->formのlabel
    item_name = models.CharField(max_length=50)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(default=make_aware(datetime.datetime.now()))
    like_users = models.ManyToManyField(User, related_name='like_items', blank=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.item_name

    class Meta:
        db_table = 'item'
        managed = True
        verbose_name = 'Item'
        verbose_name_plural = 'Items'