from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from shop_apk.cart import Cart
from shop_apk.models import Profile, Product, Image, Category, Favourites, Opinion
from shop_apk.forms import RegisterForm, UserEditForm, ProfileEditForm
from django.urls import reverse
from django.urls import reverse_lazy
from django.forms import modelformset_factory


class RegisterView(View):
    def get(self, request):
        return render(request, "registration/register.html", {'RegisterForm': RegisterForm})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            Profile.objects.create(user=new_user)
            return redirect(reverse('login'))

        return render(request, "registration/register.html", {'RegisterForm': RegisterForm(), 'error': 'Error!'})


class UserDetailView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, "user/user_details.html", {"user_form": user_form, "profile_form": profile_form})

    def post(self, request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        return redirect(reverse("user_detail"))


class ProductsListUserView(ListView):
    paginate_by = 30
    template_name = 'user/user_list_products.html'

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)


class ProductDeleteView(View):
    def get(self, request, id):
        product = Product.objects.get(id=id)

        if product.user_id == request.user.id:
            product.delete()

        return redirect(reverse("products_user"))


class ProductAddView(CreateView):
    model = Product
    fields = ['name', 'price', 'description', 'quantity', 'category']
    template_name = 'user/user_product_add.html'

    def __init__(self, *args, **kwargs):
        super(ProductAddView, self).__init__(*args, **kwargs)
        self.ImageForm = modelformset_factory(Image, fields=('source',), extra=7, help_texts='pomoc')

    def get_context_data(self, **kwargs):
        context = super(ProductAddView, self).get_context_data(**kwargs)
        context['form2'] = self.ImageForm(queryset=Image.objects.none())
        return context

    def form_valid(self, form):
        formset = self.ImageForm(self.request.POST or None, self.request.FILES or None)

        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.user = self.request.user
            product.save()

            imageInstances = formset.save(commit=False)

            for instance in imageInstances:
                instance.product_id = product.id
                instance.save()

            return redirect(reverse('products_user'))

        return redirect(reverse('product_add'))


class ProductFrontListView(ListView):
    paginate_by = 12
    template_name = 'products/front_list_products.html'

    def get_queryset(self):
        return Image.objects.distinct('product')


class ProductListView(ListView):
    paginate_by = 18
    template_name = 'products/list_products.html'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products_ids = Product.objects.filter(category=category).values('id')

            return Image.objects.filter(product__in=products_ids).distinct('product')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail_product.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['images'] = Image.objects.filter(product=self.object.id)
        context['propose_products'] = Image.objects.all().distinct('product').order_by('product', '?')[:4]
        context['counter_opinions'] = Opinion.objects.filter(user=self.object.user.id).count()
        return context


def cart_add(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.add(product=product,
             quantity=1,
             update_quantity=False)
    return redirect(reverse('cart_detail'))


def cart_remove(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.remove(product)
    return redirect(reverse('cart_detail'))


def cart_detail(request):
    return render(request, 'cart.html')


@login_required
def add_or_remove_favourite(request, id):
    product = get_object_or_404(Product, id=int(id))
    if Favourites.objects.filter(user_id=request.user.id, product_id=product.id).exists():
        Favourites.objects.get(user_id=request.user.id, product_id=product).delete()
        return HttpResponse(status=200)
    else:
        Favourites.objects.create(user_id=request.user.id, product_id=product).save()
    return HttpResponse(status=201)


class FavouriteListView(LoginRequiredMixin, ListView):
    template_name = 'favourite_list.html'

    def get_queryset(self):
        favourite_ids = Favourites.objects.filter(user_id=self.request.user).values('product_id_id')
        return Image.objects.filter(product__in=favourite_ids).distinct('product')


class OpinionUserListView(LoginRequiredMixin, ListView):
    template_name = 'opinion.html'

    def get_queryset(self):
        seller_id = self.kwargs['id']
        opinions = Opinion.objects.filter(user=seller_id)
        return opinions

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OpinionUserListView, self).get_context_data(**kwargs)
        context['seller'] = User.objects.get(id=self.kwargs['id'])
        return context


class OpinionUserAddView(LoginRequiredMixin, CreateView):
    model = Opinion
    fields = ['description', 'rating']
    template_name = 'opinion_create.html'

    def form_valid(self, form):
        form.instance.user = User.objects.get(id=self.kwargs['id'])
        form.instance.author = self.request.user
        return super(OpinionUserAddView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('opinion_user_list', kwargs={'id': self.kwargs['id']})

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        seller = get_object_or_404(User, id=self.kwargs['id'])
        if user != seller:
            return super(OpinionUserAddView, self).dispatch(request, *args, **kwargs)
        return HttpResponse(status=401)
