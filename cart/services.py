def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})
    
    product_id_str = str(product_id)
    
    cart[product_id_str] = cart.get(product_id_str, 0) + 1
    
    request.session["cart"] = cart