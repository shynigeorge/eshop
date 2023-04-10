$(document).ready(function(){
    $('.pay').click(function (e){
        e.preventDefault();

        var fname=$("[name='fname']").val();
        var lname=$("[name='lname']").val();
        var email=$("[name='email']").val();
        var mobileno=$("[name='mobileno']").val();
        var address=$("[name='address']").val();
        var country=$("[name='country']").val();
        var city=$("[name='city']").val();
        var state=$("[name='state']").val();
        var zipcode=$("[name='zipcode']").val();
        var token=$("[name='csrfmiddlewaretoken']").val();

        if(fname == "" || lname == "" || email == "" || mobileno =="" ||  address=="" || country=="" || city=="" || state=="" || zipcode=="" ){


             swal("Alert!", "All fields are mandatory", "error");
             return false;
         }
        else{
                $.ajax({
                    method:"GET",
                    url:"/proceed-to-pay",
                    success: function (response){
                        //console.log(response);
                          var options = {
                              "key": "rzp_test_PC3X9wIjaDZhHe", // Enter the Key ID generated from the Dashboard
                              "amount":1*100, //response.total_price * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                              "currency": "INR",
                              "name": "Eshop", //your business name
                              "description": "Than you for buying from us",
                              "image": "https://example.com/your_logo",
                                //"order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                              "handler": function (responseb){
                                   alert(responseb.razorpay_payment_id);
                                   data={
                                         "fname": fname,
                                         "lname": lname,
                                         "email": email,
                                         "mobileno": mobileno,
                                         "address": address,
                                         "country": country,
                                         "city": city,
                                         "state": state,
                                         "zipcode": zipcode,
                                         "payment_mode":"Paid by Razorpay",
                                         "payment_id":responseb.razorpay_payment_id,
                                          csrfmiddlewaretoken: token
                                        }

                                   $.ajax({
                                       method:"POST",
                                       url:"/placeorder",
                                       data:data,
                                       success: function (responsec){
                                           swal("Congratulations!", responsec.status, "Success").then((value) => {
                                               window.location.href = '/my-orders'
                                            });


                                        }
                                    });

                                  },
                              "prefill": {
                                   "name": fname+" "+lname, //your customer's name
                                   "email": email,
                                   "contact": mobileno
                                },

                              "theme": {
                                  "color": "#3399cc"
                                    }
                                };
                        var rzp1 = new Razorpay(options);
                        rzp1.open();

                    }
            });

        }

    });


});