
$(document).ready(function(){
       $("#btn-back2").click(function(){
        var employee_name = $("#employee_name").val()



        var employee_name2 = $("#employee_name2").val()


        if((employee_name != employee_name2))
            {
                $("#modal-confirm2").trigger('click');
                return false;
            }


    });
});
