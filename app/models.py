from django.db import models

class Melody(models.Model):
    name = models.CharField(max_length=200, unique=True)
    type = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateTimeField()
    comment = models.CharField(max_length=200, blank=True)

class Tab(models.Model):
    melody = models.ForeignKey(Melody, on_delete=models.CASCADE)
    tab = models.TextField(null=True, blank=True)
    # order_num = models.IntegerField()
    # date = models.DateTimeField()
    # comment = models.CharField(max_length=200)

class Image(models.Model):
    melody = models.ForeignKey(Melody, on_delete=models.CASCADE)
    path = models.ImageField(upload_to='images', null=True, blank=True)
    order_num = models.IntegerField(default=1)
    # date = models.DateTimeField()
    image_comment = models.CharField(max_length=200, blank=True)

class URL(models.Model):
    melody = models.ForeignKey(Melody, on_delete=models.CASCADE)
    url = models.URLField(blank=True)
    # order_num = models.IntegerField()
    # date = models.DateTimeField()
    # comment = models.CharField(max_length=200)

class Type(models.Model):
    type = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.type