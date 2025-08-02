from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from medicines.models import Medicine
from .models import Cart, CartItem, Order, OrderItem, ShippingAddress
import uuid


def store(request):
    """Pharmacy store view."""
    medicines = Medicine.objects.filter(is_active=True, stock_quantity__gt=0).order_by('name')
    categories = medicines.values_list('categories__name', flat=True).distinct()
    
    return render(request, 'pharmacy/store.html', {
        'medicines': medicines,
        'categories': categories
    })


@login_required
def cart(request):
    """Shopping cart view."""
    cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
    cart_items = cart.items.all()
    
    return render(request, 'pharmacy/cart.html', {
        'cart': cart,
        'cart_items': cart_items
    })


@login_required
def checkout(request):
    """Checkout view."""
    cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
    
    if not cart.items.exists():
        return redirect('pharmacy:cart')
    
    shipping_addresses = ShippingAddress.objects.filter(user=request.user)
    
    if request.method == 'POST':
        # Process checkout
        shipping_address = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method')
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=cart.total_price,
            shipping_address=shipping_address,
            billing_address=shipping_address,
            phone_number=request.user.phone_number or '',
            email=request.user.email,
            payment_method=payment_method
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                medicine=cart_item.medicine,
                quantity=cart_item.quantity,
                price=cart_item.medicine.price
            )
            
            # Update stock
            cart_item.medicine.stock_quantity -= cart_item.quantity
            cart_item.medicine.save()
        
        # Clear cart
        cart.is_active = False
        cart.save()
        
        return redirect('pharmacy:order_detail', order_id=order.id)
    
    return render(request, 'pharmacy/checkout.html', {
        'cart': cart,
        'shipping_addresses': shipping_addresses
    })


@login_required
def orders(request):
    """Orders history view."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'pharmacy/orders.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """Order detail view."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'pharmacy/order_detail.html', {'order': order})


# API Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_add_to_cart(request):
    """API endpoint to add item to cart."""
    medicine_id = request.data.get('medicine_id')
    quantity = request.data.get('quantity', 1)
    
    try:
        medicine = Medicine.objects.get(id=medicine_id, is_active=True)
    except Medicine.DoesNotExist:
        return Response({'error': 'Medicine not found'}, status=404)
    
    if medicine.stock_quantity < quantity:
        return Response({'error': 'Insufficient stock'}, status=400)
    
    cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
    
    # Check if item already in cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        medicine=medicine,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    return Response({
        'success': True,
        'message': 'Item added to cart',
        'cart_total': cart.total_price,
        'cart_items_count': cart.total_items
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_remove_from_cart(request):
    """API endpoint to remove item from cart."""
    medicine_id = request.data.get('medicine_id')
    
    try:
        cart = Cart.objects.get(user=request.user, is_active=True)
        cart_item = CartItem.objects.get(cart=cart, medicine_id=medicine_id)
        cart_item.delete()
        
        return Response({
            'success': True,
            'message': 'Item removed from cart',
            'cart_total': cart.total_price,
            'cart_items_count': cart.total_items
        })
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        return Response({'error': 'Item not found in cart'}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_update_cart(request):
    """API endpoint to update cart item quantity."""
    medicine_id = request.data.get('medicine_id')
    quantity = request.data.get('quantity')
    
    try:
        cart = Cart.objects.get(user=request.user, is_active=True)
        cart_item = CartItem.objects.get(cart=cart, medicine_id=medicine_id)
        
        if quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()
        
        return Response({
            'success': True,
            'message': 'Cart updated',
            'cart_total': cart.total_price,
            'cart_items_count': cart.total_items
        })
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        return Response({'error': 'Item not found in cart'}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_checkout(request):
    """API endpoint for checkout."""
    shipping_address = request.data.get('shipping_address')
    payment_method = request.data.get('payment_method')
    
    cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
    
    if not cart.items.exists():
        return Response({'error': 'Cart is empty'}, status=400)
    
    # Create order
    order = Order.objects.create(
        user=request.user,
        total_amount=cart.total_price,
        shipping_address=shipping_address,
        billing_address=shipping_address,
        phone_number=request.user.phone_number or '',
        email=request.user.email,
        payment_method=payment_method
    )
    
    # Create order items
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            medicine=cart_item.medicine,
            quantity=cart_item.quantity,
            price=cart_item.medicine.price
        )
        
        # Update stock
        cart_item.medicine.stock_quantity -= cart_item.quantity
        cart_item.medicine.save()
    
    # Clear cart
    cart.is_active = False
    cart.save()
    
    return Response({
        'success': True,
        'message': 'Order placed successfully',
        'order_id': order.id,
        'order_number': order.order_number
    })
