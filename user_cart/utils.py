def checkout_calculation(user_cart_data):
    """
    Calculates cart totals with and without special offers, and computes savings percentages.

    Args:
        user_cart_data: List of cart item dictionaries containing:
            - quantity: Number of units
            - unit_price: Regular price per unit
            - no_of_units_for_offer: Units needed for special offer (optional)
            - special_price_on_offer: Special price when offer applies (optional)

    Returns:
        Dictionary containing:
            - items: List of enhanced cart items with calculated totals
            - totals: Dictionary of aggregated cart totals and savings
    """

    # Initialize totals
    total = 0  # Total without any offers
    total_with_offers = 0  # Total with offers applied
    items_list = []  # Will store enhanced item data

    # Process each item in the cart
    for data in user_cart_data:
        # Extract item data with defaults for optional fields
        quantity = data['quantity']
        unit_price = float(data['unit_price'])
        no_of_units = data.get('no_of_units_for_offer', 1)  # Default 1 if not specified
        special_price = float(data.get('special_price_on_offer', 0.0))  # Default 0 if not specified

        # Calculate regular total price (without offers)
        item_total = unit_price * quantity
        total += item_total

        # Calculate price with offers applied
        if no_of_units > 0 and special_price > 0:
            # If offer conditions are met:
            offer_units = quantity // no_of_units  # Number of complete offer bundles
            regular_units = quantity % no_of_units  # Remaining units at regular price
            item_offer_total = (offer_units * special_price) + (regular_units * unit_price)
        else:
            # No applicable offer
            item_offer_total = item_total

        total_with_offers += item_offer_total

        # Calculate percentage savings for this item
        if item_total > 0:  # Prevent division by zero
            item_savings = ((item_total - item_offer_total) / item_total) * 100
        else:
            item_savings = 0

        # Add enhanced item data to the list
        items_list.append({
            **data,  # Include original item data
            "item_total": round(item_total, 2),
            "item_offer_total": round(item_offer_total, 2),
            "item_savings_percent": round(item_savings, 2)
        })

    # Calculate overall savings percentage for entire cart
    if total > 0:  # Prevent division by zero
        savings_percent = ((total - total_with_offers) / total) * 100
    else:
        savings_percent = 0

    # Prepare final response structure
    response = {
        "items": items_list,  # List of items with calculated values
        "totals": {
            "subtotal": round(total, 2),  # Total without discounts
            "discounted_total": round(total_with_offers, 2),  # Total with discounts
            "total_savings": round(total - total_with_offers, 2),  # Absolute savings amount
            "savings_percent": round(savings_percent, 2)  # Percentage saved
        }
    }

    return response