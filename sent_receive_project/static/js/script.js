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



