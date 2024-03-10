from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, OrderItem, Order
from .forms import OrderItemForm, ProductForm, MesajForm
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import F
from django.views.generic import ListView


def home_view(request):
    return render(request, 'app_bakerystore/home.html')


class ProductListView(ListView): # class with the help of which we display a list of objects
    model = Product
    template_name = 'app_bakerystore/products.html'

    def get_context_data(self, **kwargs): # method by which we provide additional data to the template, products.html page
        context = super().get_context_data(**kwargs)
        context['products'] = context['object_list']
        return context


def product_detail(request, product_id): # function that displays product information based on an id
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'app_bakerystore/product.html', {'product': product})


def upload_product(request): # function with which we can upload products to our application using a template, page upload_product.html
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('/')
    else:
        form = ProductForm()

    return render(request, 'app_bakerystore/upload_product.html', {'form': form})

@login_required
def add_to_cart(request, product_id): # function with the help of which we can add products to the shopping cart
    try:
        # Get product by id
        product = get_object_or_404(Product, id=product_id)

        # Check if there is already an OrderItem for this product and user
        order_item, created = OrderItem.objects.get_or_create(
            user=request.user,
            ordered=False,
            product=product
        )

        if created:
            messages.success(request, f"{product.name} a fost adăugat în coș.")
        else:
            # If OrderItem already exists, we will update the quantity
            order_item.quantity = F('quantity') + 1
            order_item.save()
            messages.info(request, f"Cantitatea pentru {product.name} a fost actualizată în coș.")

        # Redirect to shopping cart page
        return redirect(reverse('app_bakerystore:shopping_cart'))
    except Exception as e:
        # We can handle the error and return a message
        messages.error(request, f"Eroare la adăugarea produsului în coș: {str(e)}")
        return redirect('/')


@login_required
def create_order(request): # function with which we can create an order
    form = OrderItemForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            product_id = form.cleaned_data['product'].id
            quantity = form.cleaned_data['quantity']

            order_item, created = OrderItem.objects.get_or_create(
                user=request.user,
                ordered=False,
                product_id=product_id,
            )
            order_item.quantity += quantity
            order_item.save()

            return JsonResponse({'status': 'success'})

    order_items = OrderItem.objects.filter(user=request.user, ordered=False)
    order_total = sum(item.get_final_price() for item in order_items)

    context = {
        'form': form,
        'order_items': order_items,
        'order_total': order_total,
    }
    return render(request, 'app_bakerystore/shopping_cart.html', context)


def finalizeaza_comanda(request):
    if request.method == 'POST':

        order_items = OrderItem.objects.filter(user=request.user, ordered=False)

        new_order = Order.objects.create(user=request.user, ordered=True)
        new_order.items.set(order_items)

        order_items.update(ordered=True)

        messages.success(request, 'Comanda a fost plasată cu succes!')
        return redirect(reverse('app_bakerystore:home'))

    return redirect(reverse('app_bakerystore:home'))


def shopping_cart(request):
    order_items = OrderItem.objects.filter(user=request.user, ordered=False)

    order_total = sum(item.get_final_price() for item in order_items)

    context = {
        'order_items': order_items,
        'total_cumparaturi': order_total,
    }

    return render(request, 'app_bakerystore/shopping_cart.html', context)


@login_required
def delete_product(request, product_id):
    if request.method == 'DELETE':
        try:
            order_item = OrderItem.objects.get(user=request.user, product_id=product_id, ordered=False)
            order_item.delete()
            return JsonResponse({'status': 'success'})
        except OrderItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Produsul nu a fost găsit în coș'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Metoda solicitată nu este permisă'})


def contact(request):
    if request.method == 'POST':
        form = MesajForm(request.POST)
        if form.is_valid():
            mesaj_nou = form.save(commit=False)
            mesaj_nou.status = 'necitit'
            mesaj_nou.save()
            return redirect('/')  # Redirect to home page
    else:
        form = MesajForm()

    return render(request, 'app_bakerystore/contact.html', {'form': form})