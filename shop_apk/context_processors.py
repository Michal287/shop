from shop_apk.functions import split_array
from shop_apk.cart import Cart
from shop_apk.models import Category, Image, Favourites


def global_context(request):
    context = {
        'cart': Cart(request),
        'categories': Category.objects.all(),
        'lastest_products': split_array(Image.objects.all().distinct('product')[:6], 3),
        'propose_products': Image.objects.all().distinct('product').order_by('product', '?')[:6],
    }

    if request.user.is_authenticated:
        context['favourites_products_ids'] = [product[0] for product in Favourites.objects.filter(user=request.user).values_list('product_id')]
    return context
