from django.shortcuts import render, get_object_or_404
from .cart import Cart  # Custom cart class to handle cart logic (add, update, delete items)
from store.models import Product  # Product model from store app
from django.http import JsonResponse  # For sending JSON responses (usually with AJAX)
from django.contrib import messages  # To display success/error messages to the user


# View to display the current shopping cart summary page
def cart_summary(request):
    cart = Cart(request)  # Initialize the cart object tied to the current session/request
    cart_products = cart.get_prods  # Get all products currently in the cart
    quantities = cart.get_quants  # Get corresponding quantities for each product
    totals = cart.cart_total()  # Calculate total price of all items in the cart

    # Render the cart summary template with the cart details in the context
    return render(request, "cart_summary.html", {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals
    })


# View to add a product to the cart (usually called via AJAX POST)
def cart_add(request):
    cart = Cart(request)  # Initialize the cart object

    # Check if the POST request contains an 'action' named 'post'
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))  # Extract product ID from POST data
        product_qty = int(request.POST.get('product_qty'))  # Extract desired quantity from POST data

        # Retrieve the product instance, or return 404 if not found
        product = get_object_or_404(Product, id=product_id)

        # Add the product with the specified quantity to the cart
        cart.add(product=product, quantity=product_qty)

        # Get updated total quantity of items in the cart
        cart_quantity = cart.__len__()

        # Send a JSON response back with the new cart quantity
        response = JsonResponse({'qty': cart_quantity})

        # Add a success message to be displayed on next page load (if applicable)
        messages.success(request, ("Product added to cart..."))

        return response  # Return the JSON response to AJAX caller


# View to delete a product from the cart (called via AJAX POST)
def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))  # Get product ID to remove

        # Remove the product from the cart
        cart.delete(product=product_id)

        # Send JSON response confirming deletion
        response = JsonResponse({'product': product_id})

        messages.success(request, ("Item deleted from shopping cart..."))

        return response


# View to update the quantity of a product in the cart (via AJAX POST)
def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))  # Product to update
        product_qty = int(request.POST.get('product_qty'))  # New quantity desired

        # Update the cart with the new quantity for the specified product
        cart.update(product=product_id, quantity=product_qty)

        # Respond with the updated quantity
        response = JsonResponse({'qty': product_qty})

        messages.success(request, ("your cart has been updated..."))

        return response
