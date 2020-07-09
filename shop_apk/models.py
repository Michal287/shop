from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField(null=True)
    street = models.CharField(max_length=32, null=True)
    city = models.CharField(max_length=32, null=True)
    zip_code = models.CharField(max_length=8, null=True)


class Opinion(models.Model):
    description = models.TextField(null=False)
    rating = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_user')


class Category(models.Model):
    name = models.CharField(max_length=32, null=False)
    slug = models.SlugField(max_length=200)

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('products_list_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=48, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    quantity = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    source = models.ImageField(upload_to='pictures/%Y/%m/%d/', max_length=255, null=False, blank=True)


class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.product_id}'

