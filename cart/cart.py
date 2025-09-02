from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session  # Store the session object tied to the current request
        
        self.request = request

        # Attempt to get existing cart from session under 'session_key'
        cart = self.session.get('session_key')

        # If cart doesn't exist in session, initialize it as an empty dict
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart  # Assign the cart dictionary to an instance variable

    def db_add(self, product, quantity):
        product_id = str(product)  # Convert product ID to string for dictionary key
        product_qty = str(quantity) 

        # If product already in cart, currently do nothing (could increase qty here)
        if product_id in self.cart:
            pass
        else:
            # Add the product ID as key and quantity as value in the cart dictionary
            self.cart[product_id] = int(product_qty)

        self.session.modified = True  
        
        if self.request.user.is_authenticated:
           current_user = Profile.objects.filter(user__id = self.request.user.id)
           
           carty = str(self.cart)   
           carty = carty.replace("\'", "\"")
           
           current_user.update(old_cart = str(carty))

    # Method to add a product and quantity to the cart
    def add(self, product, quantity):
        product_id = str(product.id)  # Convert product ID to string for dictionary key
        product_qty = str(quantity) 

        # If product already in cart, currently do nothing (could increase qty here)
        if product_id in self.cart:
            pass
        else:
            # Add the product ID as key and quantity as value in the cart dictionary
            self.cart[product_id] = int(product_qty)

        self.session.modified = True  
        
        if self.request.user.is_authenticated:
           current_user = Profile.objects.filter(user__id = self.request.user.id)
           
           carty = str(self.cart)   
           carty = carty.replace("\'", "\"")
           
           current_user.update(old_cart = str(carty))

    # Method to calculate total price of all items in cart
    def cart_total(self):
        product_ids = self.cart.keys()  # Get all product IDs currently in cart

        products = Product.objects.filter(id__in=product_ids)  # Fetch product instances from DB
        quantities = self.cart 
        total = 0

        for key, value in quantities.items():
            key = int(key)  # Convert product ID back to int

            # For each product in DB, if it matches the cart product ID
            for product in products:
                if product.id == key:
                    # Add to total depending on if the product is on sale or not
                    if product.is_sale:
                        total += product.sale_price * value
                    else:
                        total += product.price * value

            # **Note:** The return statement here is indented inside the loop, 
            # which means it will return total after processing only the first item!
            # This is likely a bug and should be unindented to be outside the loop.

        return total  # Should return total after summing all items

    # Returns number of unique products in the cart
    def __len__(self):
        return len(self.cart)

    # Returns the product objects currently in the cart
    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    # Returns the quantities dictionary
    def get_quants(self):
        quantities = self.cart
        return quantities

    # Updates the quantity for a given product in the cart
    def update(self, product, quantity):
        product_id = str(product)  # Product ID as string key
        product_qty = int(quantity)

        ourcart = self.cart
        ourcart[product_id] = product_qty  # Update quantity

        self.session.modified = True  # Save session

        if self.request.user.is_authenticated:
           current_user = Profile.objects.filter(user__id = self.request.user.id)
           
           carty = str(self.cart)   
           carty = carty.replace("\'", "\"")
           
           current_user.update(old_cart = str(carty))
        
        thing = self.cart  

        return thing  # Return updated cart (usually not used)

    # Removes a product from the cart
    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]  # Delete the product entry from cart

        self.session.modified = True  # Save session

        if self.request.user.is_authenticated:
           current_user = Profile.objects.filter(user__id = self.request.user.id)
           
           carty = str(self.cart)   
           carty = carty.replace("\'", "\"")
           
           current_user.update(old_cart = str(carty))
