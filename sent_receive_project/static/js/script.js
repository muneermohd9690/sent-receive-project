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

/**** edit_tonerdetails_form ****/
$(document).ready(function(){
       $("#btn-back2").click(function(){
        var toner_model = $("#toner_model").val()
        var issued_to = $("#issued_to").val()
        var employee_name = $("#employee_name").val()
        var employee_designation = $("#employee_designation").val()
        var status = $("#status").val()

        var toner_model2 = $("#toner_model2").val()
        var issued_to2 = $("#issued_to2").val()
        var employee_name2 = $("#employee_name2").val()
        var employee_designation2 = $("#employee_designation2").val()
        var status2 = $("#status2").val()
        if((toner_model!=toner_model2)||(issued_to!=issued_to2)||(employee_name != employee_name2)||(employee_designation != employee_designation2)
            ||(status!=status2))
            {
                $("#modal-confirm2").trigger('click');
                return false;
            }
    });
});
/**** edit_tonerdetails_form ****/

/**** disable save button in edit_tonerdetails_form ****/
$(document).ready(function(){
    $("#employee_name,#employee_name2").on("keyup",function(){
        $(".btn-action2").prop("disabled",false);
            if(($("#employee_name").val())==($("#employee_name2").val())){
                    $(".btn-action2").prop("disabled",true);
        }
    });
   });
$(document).ready(function(){
    $("#employee_designation,#employee_designation2").on("keyup",function(){
        $(".btn-action2").prop("disabled",false);
            if(($("#employee_designation").val())==($("#employee_designation2").val())){
                    $(".btn-action2").prop("disabled",true);
        }
    });
   });
$(document).ready(function(){
    $(".btn-action2").prop("disabled", true);
    $("#toner_model, #toner_model2").change(function() {
        if( ($("#toner_model").val()) == ($("#toner_model2").val()) ) {
            $(".btn-action2").attr("disabled", "disabled");
        }
        else {
            $(".btn-action2").removeAttr("disabled");
        }
     });
   });
$(document).ready(function(){
    $(".btn-action2").prop("disabled", true);
    $("#issued_to, #issued_to2").change(function() {
        if( ($("#issued_to").val()) == ($("#issued_to2").val()) ) {
            $(".btn-action2").attr("disabled", "disabled");
        }
        else {
            $(".btn-action2").removeAttr("disabled");
        }
     });
   });
 $(document).ready(function(){
    $(".btn-action2").prop("disabled", true);
    $("#status, #status2").change(function() {
        if( ($("#status").val()) == ($("#status2").val()) ) {
            $(".btn-action2").attr("disabled", "disabled");
        }
        else {
            $(".btn-action2").removeAttr("disabled");
        }
     });
   });

/**** disable save button in edit_tonerdetails_form ****/

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
/**** modal in edit_item_details_form ****/
$(document).ready(function(){
    $("#btn-back").click(function(){
        var model_no = $("#model_no").val()
        var serial_no = $("#serial_no").val()
        var tag_no = $("#tag_no").val()
        var issued_to = $("#issued_to").val()
        var employee_name = $("#employee_name").val()
        var employee_designation = $("#employe_designation").val()
        var status = $("#status").val()

        var model_no2 = $("#model_no2").val()
        var serial_no2 = $("#serial_no2").val()
        var tag_no2 = $("#tag_no2").val()
        var issued_to2 = $("#issued_to2").val()
        var employee_name2 = $("#employee_name2").val()
        var employee_designation2 = $("#employe_designation2").val()
        var status2 = $("#status2").val()
        if((model_no!=model_no2)||(serial_no!=serial_no2)||(tag_no!=tag_no2)||(issued_to!=issued_to2)||(employee_name!=employee_name2)
            ||(employee_designation!=employee_designation2)||(status!=status2))
            {
                $("#modal-confirm").trigger('click');
                return false;
            }

    });
});
/**** modal in edit_item_details_form ***/