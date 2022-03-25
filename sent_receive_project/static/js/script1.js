/**** to disbale save button if no changes in edit forms ****/
$("#toner_model, #toner_model2").on("keyup",function(){
    $(".btn-action1").prop("disabled",false);
    if(($("#toner_model").val())==($("#toner_model2").val())){
        $(".btn-action1").prop("disabled",true);
    }
});
/**** to disbale save button if no changes in edit forms ****/
