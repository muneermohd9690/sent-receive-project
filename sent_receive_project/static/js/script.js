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
$("#employee_name, #employee_name2").on("keyup",function(event) {
    $(".btn-action2").prop("disabled",false);
    if( ($("#employee_name").val()) == ($("#employee_name2").val())) {
        $(".btn-action2").prop("disabled",true);
    }
});