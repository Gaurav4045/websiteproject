$(document).ready(function () {
    // Plus cart button click event
    $(document).on('click', '.plus-cart', function () {
        const prodId = $(this).attr('pid'); // Get product ID
        const url = $(this).data('url'); // URL for increasing quantity
        updateCart(url, prodId);
    });

    // Minus cart button click event
    $(document).on('click', '.minus-cart', function () {
        const prodId = $(this).attr('pid'); // Get product ID
        const url = $(this).data('url'); // URL for decreasing quantity
        updateCart(url, prodId);
    });

    // Remove cart item button click event
    $(document).on('click', '.remove-cart', function () {
        const prodId = $(this).attr('pid'); // Get product ID
        const url = $(this).data('url'); // URL for removing item

        // Call the updateCart function and remove the item from the DOM
        $.ajax({
            type: "GET",
            url: url,
            data: { prod_id: prodId },
            success: function (data) {
                if (data.status === 'success') {
                    // Remove the cart item from the DOM
                    $(`.product-${prodId}`).remove();

                    // Update the total amount
                    $('#amount').text('Rs. ' + data.amount);
                    $('#total_amount').text('Rs. ' + data.total_amount);

                    // Show a message if the cart is empty
                    if (data.cart_empty) {
                        $('#cart-items').html('<p>Your cart is empty.</p>');
                    }
                } else {
                    console.error(data.message);
                }
            },
            error: function (xhr, status, error) {
                console.error("Request failed: ", error);
            }
        });
    });

    // Common function to update cart (for plus/minus actions)
    function updateCart(url, prodId) {
        $.ajax({
            type: "GET",
            url: url,
            data: { prod_id: prodId },
            success: function (data) {
                if (data.status === 'success') {
                    // Update the quantity
                    const quantityElement = $(`.product-${prodId}`).find('.quantity');
                    quantityElement.text(data.quantity);

                    // Update the total amount
                    $('#amount').text('Rs. ' + data.amount);
                    $('#total_amount').text('Rs. ' + data.total_amount);

                    // If quantity is 0, remove the item from the cart
                    if (data.quantity === 0) {
                        $(`.product-${prodId}`).remove();

                        // Show a message if the cart is empty
                        if (data.cart_empty) {
                            $('#cart-items').html('<p>Your cart is empty.</p>');
                        }
                    }
                } else {
                    console.error(data.message);
                }
            },
            error: function (xhr, status, error) {
                console.error("Request failed: ", error);
            }
        });
    }
});

$(document).ready(function () {
    // Add to wishlist
    $(document).on('click', '.plus-wishlist', function () {
        const prodId = $(this).attr('pid');
        $.ajax({
            type: "GET",
            url: "/plus-wishlist/",
            data: { prod_id: prodId },
            success: function (data) {
                if (data.status === 'success' || data.status === 'exists') {
                    alert(data.message);
                    // Optionally, toggle button style or refresh part of the page
                    location.reload();
                } else {
                    console.error(data.message);
                }
            },
            error: function (xhr, status, error) {
                console.error("Request failed: ", error);
            }
        });
    });

    // Remove from wishlist
    $(document).on('click', '.minus-wishlist', function () {
        const prodId = $(this).attr('pid');
        $.ajax({
            type: "GET",
            url: "/minus-wishlist/",
            data: { prod_id: prodId },
            success: function (data) {
                if (data.status === 'success') {
                    alert(data.message);
                    // Optionally, toggle button style or refresh part of the page
                    location.reload();
                } else {
                    console.error(data.message);
                }
            },
            error: function (xhr, status, error) {
                console.error("Request failed: ", error);
            }
        });
    });
});

