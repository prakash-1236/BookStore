

// $('.plus-cart').click(function(){
//     var id=$(this).attr("pid").toString();
//     var eml=this.parentNode.children[2]
//     console.log("pid =", id)
//     $.ajax({
//         type:"GET",
//         url:"/pluscart",
//         data:{
//             prod_id:id
//         },
//         success:function(data){
//             console.log("data = ",data);
//             eml.innerText=data.quantity
//             document.getElementById("amount").innerText=data.amount
//             document.getElementById("totalamount").innerText=data.totalamount
//             eml.parentNode.parentNode.parentNode.parentNode.remove()
//         }
//     })
// })


    // ✅ INCREASE QUANTITY (+)
    $('.plus-cart').click(function(){
        var id = $(this).attr("pid");
        var eml = $(this).siblings("span")[0];

        $.ajax({
            type: "GET",
            url: "/pluscart",
            data: { prod_id: id },
            success: function(data){
                $(eml).text(data.quantity);
                $("#amount").text("Rs. " + data.amount);
                $("#totalamount").text("Rs. " + data.totalamount);
            },
            error: function(xhr, status, error) {
                console.error("Error:", error);
            }
        });
    });

    // ✅ DECREASE QUANTITY (-)
    $('.minus-cart').click(function(){
        var id = $(this).attr("pid");
        var eml = $(this).siblings("span")[0];

        $.ajax({
            type: "GET",
            url: "/minuscart",
            data: { prod_id: id },
            success: function(data){
                if (data.quantity === 0) {
                    $(this).closest('.row').remove(); // Remove the item row dynamically
                } else {
                    $(eml).text(data.quantity);
                }
                $("#amount").text("Rs. " + data.amount);
                $("#totalamount").text("Rs. " + data.totalamount);
            },
            error: function(xhr, status, error) {
                console.error("Error:", error);
            }
        });
    });

    // ✅ REMOVE ITEM FROM CART
    $('.remove-cart').click(function(){
        var id = $(this).attr("pid");

        $.ajax({
            type: "GET",
            url: "/removecart",
            data: { prod_id: id },
            success: function(data){
                $(this).closest('.row').remove(); // Remove item from UI without reload
                $("#amount").text("Rs. " + data.amount);
                $("#totalamount").text("Rs. " + data.totalamount);
            },
            error: function(xhr, status, error) {
                console.error("Error:", error);
            }
        });
    });


    

    $(".plus-wishlist").click(function() {  
        var id = $(this).attr("pid").toString();  

        $.ajax({
            type: "GET",
            url: "/pluswishlist",
            data: { prod_id: id },
            success: function(data) {
                alert(data.message);  // Show a success message
                $("#wishlist-icon-" + id).removeClass("btn-success").addClass("btn-danger");
                $("#wishlist-icon-" + id).html('<i class="fas fa-heart fa-lg"></i>'); // Change icon
            },
            error: function() {
                alert("Failed to add to wishlist.");
            }
        });
    });

    $(".minus-wishlist").click(function() {  
        var id = $(this).attr("pid").toString();  

        $.ajax({
            type: "GET",
            url: "/minuswishlist",
            data: { prod_id: id },
            success: function(data) {
                alert(data.message);
                $("#wishlist-icon-" + id).removeClass("btn-danger").addClass("btn-success");
                $("#wishlist-icon-" + id).html('<i class="far fa-heart fa-lg"></i>'); // Change icon
            },
            error: function() {
                alert("Failed to remove from wishlist.");
            }
        });
    });