$(document).ready(function () {
    $(document).off('click', '.payWithRazorpay').on('click', '.payWithRazorpay', function (e) {
        e.preventDefault();
        var selected_address = $("[name='selected_address']").val();
        var payment_method = $("input[name='payment_method']:checked").val();
        var token = $("[name='csrfmiddlewaretoken']").val();

        if (!selected_address) {
            swal("Alert!", "Select the shipping address", "error");
            return false;
        }

        $.ajax({
            method: "GET",
            url: "/products/proceed-to-pay/",
            success: function (response) {
                var options = {
                    "key": "rzp_test_Yl6grfBbwpSDvh",
                    "amount": response.total_price * 100,
                    "currency": "INR",
                    "name": "Shopper Colorlib",
                    "description": "Thank you for choosing us",
                    "image": "https://example.com/your_logo",
                    "handler": function (responseb) {
                        swal("Payment ID: " + responseb.razorpay_payment_id);
                        var data = {
                            "payment_mode": "RazorPay",
                            "selected_address": selected_address,
                            "payment_id": responseb.razorpay_payment_id,
                            "csrfmiddlewaretoken": token,
                            "order_id": response.order_id, 
                        };
                        console.log(data); // Log the data to verify
                        $.ajax({
                            method: "POST",
                            url:  "/products/confirm-order-razorpay/",
                            data: data,
                            success: function (responsec) {
                                swal("Congratulations!", responsec.status, "success").then((value) => {
                                    window.location.href = '/products/order-success/' + responsec.order_number;
                                });
                            },
                            error: function (xhr, status, error) {
                                console.error("AJAX POST Request Failed:", xhr.responseText);
                            }
                        });
                    },
                    "prefill": {
                        "name": response.first_name,
                        "email": response.email,
                        "contact": response.phone_number
                    },
                    "theme": {
                        "color": "#3399cc"
                    }
                };
                var rzp1 = new Razorpay(options);
                rzp1.open();
            },
            error: function (xhr, status, error) {
                console.error("AJAX GET Request Failed:", xhr.responseText);
            }
        });
    });
});
