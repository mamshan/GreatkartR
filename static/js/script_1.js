function chk_loc() {

    let text = document.getElementById("pickup").value;
    let result = text.substring(0, 1);
    document.getElementById("avail").innerHTML = "";

    if (result == "S" || result == "D") {

        
        if (document.getElementById("b").value >0) {
            document.getElementById("avail").innerHTML = "Available In 3 Days";
        }
        if (document.getElementById("c").value >0) {
            document.getElementById("avail").innerHTML = "Available In 5 Days";
        }

        if (document.getElementById("a").value >0) {
            document.getElementById("avail").innerHTML = "Available In 24 Hours";
        }
        if (document.getElementById("d").value >0) {
            document.getElementById("avail").innerHTML = "Available In 24 Hours";
        }

        if ((document.getElementById("a").value+document.getElementById("b").value) <3) {
            if (document.getElementById("ha").value >3) {
                document.getElementById("avail").innerHTML = "Available In 5 Days";
            }
        }
    }

    if (result == "P") {

        if (document.getElementById("a").value >0) {
            document.getElementById("avail").innerHTML = "Available In 5 Days";
        } 
         
        if (document.getElementById("c").value >0) {
            document.getElementById("avail").innerHTML = "Available In 5 Days";
        }
        
        if (document.getElementById("d").value >0) {
            document.getElementById("avail").innerHTML = "Available In 5 Days";
        }

        if (document.getElementById("b").value >0) {
            document.getElementById("avail").innerHTML = "Available In 24 Hours";

            if (document.getElementById("b").value <3) {
                if (document.getElementById("ha").value >3) {
                    document.getElementById("avail").innerHTML = "Available In 5 Days";
                }
            }
        }
    }

    if (result == "J") {

        if (document.getElementById("a").value >0) {
            document.getElementById("avail").innerHTML = "Available In 5 Days";
        } 
         
        if (document.getElementById("b").value >0) {
            document.getElementById("avail").innerHTML = "Available In 5 Days";
        }
        
        if (document.getElementById("d").value >0) {
            document.getElementById("avail").innerHTML = "Available In 5 Days";
        }
        if (document.getElementById("c").value >0) {
            document.getElementById("avail").innerHTML = "Available In 24 Hours";

            if (document.getElementById("c").value <3) {
                if (document.getElementById("ha").value >3) {
                    document.getElementById("avail").innerHTML = "Available In 5 Days";
                }
            }
        }
    }

    // preventing from page reload and default actions
            
            // serialize the data for sending the form data.
            var serializedData = $(this).serialize();
            // make POST ajax call
            
            var data = new FormData();
             
            var dataString = "location="+ document.getElementById("pickup").value;
            
            
            document.getElementById("agdt").innerHTML = "";
            document.getElementById("agcontdt").innerHTML="";

            $.ajax({
                type: 'GET',
                url: "/store/get_agentdt/",
                data: dataString,
                success: function (response) {    
                    document.getElementById("agdt").innerHTML = response.agdt;
                    document.getElementById("agcontdt").innerHTML = response.agcontdt;
                    
                    

                },
                error: function (response) {
                    // alert the error if any error occured
                    alert(response["responseJSON"]["error"]);
                }
            })

}