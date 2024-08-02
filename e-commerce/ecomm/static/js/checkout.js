$(document).ready(function () {
    $('.payWithRazorpay').off('click').on('click', function (e) {
        e.preventDefault();
        console.log("Razorpay button clicked");
        var token = $("[name='csrfmiddlewaretoken']").val();

        $.ajax({
            method: "GET",
            url: "/products/proceed-to-pay/",
            success: function (response) {
                console.log("Response from server:", response);

                if (response.total_price) {
                    var options = {
                        "key": "rzp_test_Yl6grfBbwpSDvh", // Enter the Key ID generated from the Dashboard
                        "amount": response.total_price * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name": "Shoppers - Colorlib e-commerce", // your business name
                        "description": "Thank you for choosing us",
                        "image": "https://example.com/your_logo",
                        //"order_id": "order_9A33XWu170gUtm", // This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "handler": function (responseb) {
                            alert(responseb.razorpay_payment_id);
                            data = {
                                "payment_method" : "Paid by RazorPay",
                                "payment_id" : responseb.razorpay_payment_id,
                                csrfmiddlewaretoken : token,
                            }
                            $.ajax({
                                method : "POST",
                                url : "/products/place-order/",
                                data:data,
                                success: function(responsec){
                                    swal("Congratulations",responsec.status,"success").then((value) => {
                                        window.location.href = '/User/my-orders'
                                      });

                                }
                            });
                        },
                        "prefill": { // We recommend using the prefill parameter to auto-fill customer's contact information, especially their phone number
                            "name": response.first_name, // your customer's name
                            "email": "gaurav.kumar@example.com",
                            "contact": "9000090000" // Provide the customer's phone number for better conversion rates 
                        },
                        "notes": {
                            "address": "Razorpay Corporate Office"
                        },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);

                    rzp1.open();
                } else {
                    console.error('Total price not returned from server');
                }
            },
            error: function (xhr, status, error) {
                console.error("AJAX request failed:", error);
            }
        });
    });
});
