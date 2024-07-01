/**** protection against ddos ****/
if (window.history.replaceState){
    window.history.replaceState(null,null,window.location.href);
}
/**** protection against ddos ****/


/**** edit_toners_form ****/
$(document).ready(function(){
    $("#btn-back").click(function(){
        var toner_model = $("#toner_model").val()
        var toner_printer = $("#toner_printer").val()

        var toner_model2 = $("#toner_model2").val()
        var toner_printer2 = $("#toner_printer2").val()
        if((toner_printer != toner_printer2)||(toner_model!=toner_model2))
            {
                $("#modal-confirm").trigger('click');
                return false;
            }
    });
});
/**** edit_toners_form ****/

/**** edit_contract_details ****/
$(document).ready(function(){
    // Track if a file is chosen
    var fileChosen = false;
    $("#pdf_file").change(function(){
            fileChosen = true;
    });
    // Event listener for file input change
    $("#btn-back").click(function(){
        var lpo_no = $("#lpo_no").val()
        var purchased_by = $("#purchased_by").val()
        var warranty_years = $("#warranty_years").val()
        var purchased_date = $("#purchased_date").val()
        //var pdf_file = $("#pdf_file").val()  // Get the value of the file input

        var lpo_no2 = $("#lpo_no2").val()
        var purchased_by2 = $("#purchased_by2").val()
        var warranty_years2 = $("#warranty_years2").val()
        var purchased_date2 = $("#purchased_date2").val()
        //var pdf_file2 = $("#pdf_file2").val()  // Get the value of the hidden input

        // Check if any changes are made, including choosing a new file
        if (
            (lpo_no != lpo_no2) ||
            (purchased_by != purchased_by2) ||
            (warranty_years != warranty_years2) ||
            (purchased_date != purchased_date2) ||
            (fileChosen)
        )
            {
                // Show the modal
                $("#modal-confirm").trigger('click');
                return false;
            }

    });
});
/**** edit_contract_details ****/

/**** edit_tonerdetails_form ****/
$(document).ready(function(){
       $("#btn-back2").click(function(){
        var toner_model = $("#toner_model").val()
        var issued_to = $("#issued_to").val()
        var employee_name = $("#employee_name").val()
        var employee_designation = $("#employee_designation").val()
        var date_dispatched = $("#date_dispatched").val()
        var status = $("#status").val()

        var toner_model2 = $("#toner_model2").val()
        var issued_to2 = $("#issued_to2").val()
        var employee_name2 = $("#employee_name2").val()
        var employee_designation2 = $("#employee_designation2").val()
        var date_dispatched2 = $("#date_dispatched2").val()
        var status2 = $("#status2").val()
        if((toner_model!=toner_model2)||(issued_to!=issued_to2)||(employee_name != employee_name2)||(employee_designation != employee_designation2)
            ||(status!=status2)||(date_dispatched!=date_dispatched2))
            {
                $("#modal-confirm2").trigger('click');
                return false;
            }
    });
});
/**** edit_tonerdetails_form ****/

/**** disable save button in edit_tonerdetails_form(ETDF) ****/
$(document).ready(function(){
    $("#employee_name,#employee_name2").on("keyup",function(){
        $(".btn-action-ETDF").prop("disabled",false);
            if(($("#employee_name").val())==($("#employee_name2").val())){
                    $(".btn-action-ETDF").prop("disabled",true);
        }
    });
   });
$(document).ready(function(){
    $("#employee_designation,#employee_designation2").on("keyup",function(){
        $(".btn-action-ETDF").prop("disabled",false);
            if(($("#employee_designation").val())==($("#employee_designation2").val())){
                    $(".btn-action-ETDF").prop("disabled",true);
        }
    });
   });
$(document).ready(function(){
    $(".btn-action-ETDF").prop("disabled", true);
    $("#toner_model, #toner_model2").change(function() {
        if( ($("#toner_model").val()) == ($("#toner_model2").val()) ) {
            $(".btn-action-ETDF").attr("disabled", "disabled");
        }
        else {
            $(".btn-action-ETDF").removeAttr("disabled");
        }
     });
   });
$(document).ready(function(){
    $(".btn-action-ETDF").prop("disabled", true);
    $("#issued_to, #issued_to2").change(function() {
        if( ($("#issued_to").val()) == ($("#issued_to2").val()) ) {
            $(".btn-action-ETDF").attr("disabled", "disabled");
        }
        else {
            $(".btn-action-ETDF").removeAttr("disabled");
        }
     });
   });
 $(document).ready(function(){
    $(".btn-action-ETDF").prop("disabled", true);
    $("#status, #status2").change(function() {
        if( ($("#status").val()) == ($("#status2").val()) ) {
            $(".btn-action-ETDF").attr("disabled", "disabled");
        }
        else {
            $(".btn-action-ETDF").removeAttr("disabled");
        }
     });
   });

/**** modal in edit_items_form ****/
$(document).ready(function(){
    $("#btn-back").click(function(){
        var model_no = $("#model_no").val()
        var description = $("#description").val()

        var model_no2 = $("#model_no2").val()
        var description2 = $("#description2").val()
        if((model_no != model_no2)||(description!=description2))
            {
                $("#modal-confirm").trigger('click');
                return false;
            }
    });
});

/**** modal in edit_prosecutions_form ****/
$(document).ready(function(){
    $("#btn-back").click(function(){
        var name = $("#name").val()
        var location = $("#location").val()

        var name2 = $("#name2").val()
        var location2 = $("#location2").val()
        if((name!= name2)||(location!=location2))
            {
                $("#modal-confirm").trigger('click');
                return false;
            }
    });
});
/**** modal in edit_prosecutions_form ****/

/**** modal in edit_item_details_form ****/
$(document).ready(function(){
    // Track if a file is chosen
    var fileChosen = false;
    $("#pdf_file").change(function(){
            fileChosen = true;
    });
    $("#btn-back").click(function(){
        var model_no = $("#model_no").val()
        var serial_no = $("#serial_no").val()
        var tag_no = $("#tag_no").val()
        var room_tag = $("#room_tag").val()
        var issued_to = $("#issued_to").val()
        var lpo_no = $("#lpo_no").val()
        var employee_name = $("#employee_name").val()
        var employee_designation = $("#employee_designation").val()
        var date_dispatched = $("#date_dispatched").val()
        var status = $("#status").val()

        var model_no2 = $("#model_no2").val()
        var serial_no2 = $("#serial_no2").val()
        var tag_no2 = $("#tag_no2").val()
        var room_tag2 = $("#room_tag2").val()
        var issued_to2 = $("#issued_to2").val()
        var lpo_no2 = $("#lpo_no2").val()
        var employee_name2 = $("#employee_name2").val()
        var employee_designation2 = $("#employee_designation2").val()
        var date_dispatched2 = $("#date_dispatched2").val()
        var status2 = $("#status2").val()
        if((model_no!=model_no2)||(serial_no!=serial_no2)||(tag_no!=tag_no2)||(room_tag!=room_tag2)||
            (issued_to!=issued_to2)||(employee_name!=employee_name2)||(lpo_no!=lpo_no2)
            ||(employee_designation!=employee_designation2)||(date_dispatched!=date_dispatched2)||(status!=status2)||(fileChosen))
            {
                $("#modal-confirm").trigger('click');
                return false;
            }

    });
});
/**** modal in edit_item_details_form ***/

/**** disable save button in edit_toners_form(ETF) ****/
$(document).ready(function(){
    $("#toner_model,#toner_model2").on("keyup",function(){
        $(".btn-action-ETF").prop("disabled",false);
            if(($("#toner_model").val())==($("#toner_model2").val())){
                    $(".btn-action-ETF").prop("disabled",true);
        }
    });
   });

 $(document).ready(function(){
    $(".btn-action-ETF").prop("disabled", true);
    $("#toner_printer, #toner_printer2").change(function() {
        if( ($("#toner_printer").val()) == ($("#toner_printer2").val()) ) {
            $(".btn-action-ETF").attr("disabled", "disabled");
        }
        else {
            $(".btn-action-ETF").removeAttr("disabled");
        }
     });
   });

 /**** disable save button in edit_toners_form(ETF)  ****/

 /**** disable save button in edit_items_form(EIF) ****/
$(document).ready(function(){
    $("#model_no,#model_no2").on("keyup",function(){
        $(".btn-action-EIF").prop("disabled",false);
            if(($("#model_no").val())==($("#model_no2").val())){
                    $(".btn-action-EIF").prop("disabled",true);
        }
    });
   });

$(document).ready(function(){
    $("#description,#description2").on("keyup",function(){
        $(".btn-action-EIF").prop("disabled",false);
            if(($("#description").val())==($("#description2").val())){
                    $(".btn-action-EIF").prop("disabled",true);
        }
    });
   });

 /**** disable save button in edit_items_form(EIF) ****/

 /**** disable save button in edit_contract_details(ECD) ****//*
*/
$(document).ready(function(){
    $("#lpo_no,#lpo_no2").on("keyup",function(){
        $(".btn-action-ECD").prop("disabled",false);
            if(($("#lpo_no").val())==($("#lpo_no2").val())){
                    $(".btn-action-ECD").prop("disabled",true);
        }
    });
   });

$(document).ready(function(){
    $(".btn-action-ECD").prop("disabled", true);
    $("#purchased_by, #purchased_by2").change(function() {
        if( ($("#purchased_by").val()) == ($("#purchased_by2").val()) ) {
            $(".btn-action-ECD").attr("disabled", "disabled");
        }
        else {
            $(".btn-action-ECD").removeAttr("disabled");
        }
     });
   });

$(document).ready(function(){
    $(".btn-action-ECD").prop("disabled", true);
    $("#warranty_years, #warranty_years2").change(function() {
        if( ($("#warranty_years").val()) == ($("#warranty_years2").val()) ) {
            $(".btn-action-ECD").attr("disabled", "disabled");
        }
        else {
            $(".btn-action-ECD").removeAttr("disabled");
        }
     });
   });

$(document).ready(function(){
    $(".btn-action-ECD").prop("disabled", true);
    $("#purchased_date, #purchased_date2").change(function() {
        if( ($("#purchased_date").val()) == ($("#purchased_date2").val()) ) {
            $(".btn-action-ECD").attr("disabled", "disabled");
        }
        else {
            $(".btn-action-ECD").removeAttr("disabled");
        }
     });
   });

$(document).ready(function(){
    $(".btn-action-ECD").prop("disabled", true);

    $("#pdf_file").change(function() {
      // Check if a new PDF file is selected
      if ($(this).val()) {
        $(".btn-action-ECD").prop("disabled", false);
      } else {
        $(".btn-action-ECD").prop("disabled", true);
      }
    });
});


 /**//**** disable save button in edit_contract_details(ECD) ****/


  /**** disable save button in edit_prosecutions_form(EPF) ****/
$(document).ready(function(){
    $("#name,#name2").on("keyup",function(){
        $(".btn-action-EPF").prop("disabled",false);
            if(($("#name").val())==($("#name2").val())){
                    $(".btn-action-EPF").prop("disabled",true);
        }
    });
   });

$(document).ready(function(){
    $("#location,#location2").on("keyup",function(){
        $(".btn-action-EPF").prop("disabled",false);
            if(($("#location").val())==($("#location2").val())){
                    $(".btn-action-EPF").prop("disabled",true);
        }
    });
   });

 /**** disable save button in edit_prosecutions_form(EPF) ****/

/**** disable save button in edit_item_details_form(EIDF) ****/

 $(document).ready(function(){
    $(".btn-action-EIDF").prop("disabled", true);
    $("#model_no, #model_no2").change(function() {
        if( ($("#model_no").val()) == ($("#model_no2").val()) ) {
            $(".btn-action-EIDF").attr("disabled", "disabled");
        }
        else {
            $(".btn-action-EIDF").removeAttr("disabled");
        }
     });
   });

   $(document).ready(function(){
    $("#serial_no,#serial_no2").on("keyup",function(){
        $(".btn-action-EIDF").prop("disabled",false);
            if(($("#serial_no").val())==($("#serial_no2").val())){
                    $(".btn-action-EIDF").prop("disabled",true);
        }
    });
   });


   $(document).ready(function(){
    $("#tag_no,#tag_no2").on("keyup",function(){
        $(".btn-action-EIDF").prop("disabled",false);
            if(($("#tag_no").val())==($("#tag_no2").val())){
                    $(".btn-action-EIDF").prop("disabled",true);
        }
    });
   });

   $(document).ready(function(){
    $("#room_tag,#room_tag2").on("keyup",function(){
        $(".btn-action-EIDF").prop("disabled",false);
            if(($("#room_tag").val())==($("#romm_tag2").val())){
                    $(".btn-action-EIDF").prop("disabled",true);
        }
    });
   });

 $(document).ready(function(){
    $(".btn-action-EIDF").prop("disabled", true);
    $("#issued_to, #issued_to2").change(function() {
        if( ($("#issued_to").val()) == ($("#issued_to2").val()) ) {
            $(".btn-action-EIDF").attr("disabled", "disabled");
        }
        else {
            $(".btn-action-EIDF").removeAttr("disabled");
        }
     });
   });

 $(document).ready(function(){
    $(".btn-action-EIDF").prop("disabled", true);
    $("#lpo_no, #lpo_no2").change(function() {
        if( ($("#lpo_no").val()) == ($("#lpo_no2").val()) ) {
            $(".btn-action-EIDF").attr("disabled", "disabled");
        }
        else {
            $(".btn-action-EIDF").removeAttr("disabled");
        }
     });
   });

  $(document).ready(function(){
    $("#employee_name,#employee_name2").on("keyup",function(){
        $(".btn-action-EIDF").prop("disabled",false);
            if(($("#employee_name").val())==($("#employee_name2").val())){
                    $(".btn-action-EIDF").prop("disabled",true);
        }
    });
   });

   $(document).ready(function(){
    $("#employee_designation,#employee_designation2").on("keyup",function(){
        $(".btn-action-EIDF").prop("disabled",false);
            if(($("#employee_designation").val())==($("#employee_designation2").val())){
                    $(".btn-action-EIDF").prop("disabled",true);
        }
    });
   });

 $(document).ready(function(){
    $(".btn-action-EIDF").prop("disabled", true);
    $("#status, #status2").change(function() {
        if( ($("#status").val()) == ($("#status2").val()) ) {
            $(".btn-action-EIDF").attr("disabled", "disabled");
        }
        else {
            $(".btn-action-EIDF").removeAttr("disabled");
        }
     });
   });

$(document).ready(function(){
    $(".btn-action-EIDF").prop("disabled", true);

    $("#pdf_file").change(function() {
      // Check if a new PDF file is selected
      if ($(this).val()) {
        $(".btn-action-EIDF").prop("disabled", false);
      } else {
        $(".btn-action-EIDF").prop("disabled", true);
      }
    });
});

/*$(document).ready(function(){
    $(".btn-action-EIDF").prop("disabled", true);
    $("#date_dispatched, #date_dispatched2").change(function() {
        if( ($("#date_dispatched").val()) == ($("#date_dispatched2").val()) ) {
            $(".btn-action-ETDF").attr("disabled", "disabled");
        }
        else {
            $(".btn-action-EIDF").removeAttr("disabled");
        }
     });
   });*/
/**** disable save button in edit_item_details_form(EIDF) ****/

/**** to show bulk delete button on checkbox select ****/
$(document).ready(function() {
        $('.bulk-action-checkbox').change(function() {
            if ($('.bulk-action-checkbox:checked').length > 0) {
                console.log('Buttons should be shown');
                $('#btn-bulkdelete').show();
                $('#btn-bulkdispatch').show();
                $('#btn-selectdispatch').show();
                $('#btn-selectremove').show();
                $('#btn-select_print_sent_items_invoice').show();
                $('#btn-dispatch').hide();
                $('#btn-print_sent_items_invoice').hide();
            } else {
                console.log('Buttons should be hidden');
                $('#btn-bulkdelete').hide();
                $('#btn-bulkdispatch').hide();
                $('#btn-selectdispatch').hide();
                $('#btn-selectremove').hide();
                $('#btn-select_print_sent_items_invoice').hide();
                $('#btn-dispatch').show();
                $('#btn-print_sent_items_invoice').show();
            }
        });
});

/**** to show bulk delete button on checkbox select ****/

/**** select picker and search box ****/
$(document ).ready(function (){
    $('#issued_to').selectpicker();
    $('#toner_model').selectpicker();
    $('#model_no').selectpicker();
    $('#toner_printer').selectpicker();
})

/**** select picker and search box ****/

/**** Login verification and messages ****/
 $(document).ready(function() {
        $('#login-form').on('submit', function(event) {
                event.preventDefault();
                var form = $(this);
            var username = $("#username").val();
            var password = $("#password").val();
            var redirectUrl = $('#login-redirect-url').data('url');
            var csrf=$('input[name=csrfmiddlewaretoken]').val();
            if (username==''){

                swal("Verify !", "Username cannot be empty.","error");
                return false;
            }
            else if (password==''){
                swal("Verify !", "Password cannot be empty.","error");
                return false;
             }
            // Make an AJAX request to check the credentials
            $.ajax({
                url: "/check_login/",
                type: "POST",
                data: {
                    username: username,
                    password: password,
                    csrfmiddlewaretoken: csrf
                },
                success: function(response) {
                    // Handle the response from the server
                    if (response.is_valid) {
                        window.location.href = redirectUrl;
                    } else {
                        swal("Error!",response.message, "error");

                    }
                },
                error: function(xhr, errmsg, err) {
                    swal("Error!",errmsg, "error");
                }
            });
        });
    });
/**** Login verification and messages ****/



    document.addEventListener("DOMContentLoaded", function() {
        var logoutButton = document.getElementById("btn-logout");
//        var csrftoken = getCookie('csrftoken');
        if (logoutButton) {
            logoutButton.addEventListener("click", function(e) {
                e.preventDefault();

                // Use Ajax to send a POST request to the logout URL
                fetch('/logout/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),  // Include the CSRF token
//                        'X-CSRFToken': csrftoken
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Successful logout, redirect to the login page
                        window.location.href = data.redirect_url;
                    } else {
                        // Handle error response if needed
                        console.error('Logout failed:', data);
                    }
                })
                .catch(error => {
                    console.error('Error during logout:', error);
                });
            });
        }
    });
   /* function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        console.log(cookieValue)
        return cookieValue;
    }*/
