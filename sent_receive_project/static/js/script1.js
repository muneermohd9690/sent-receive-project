/***  for adding to cart ***/
function getCartData(detailId, action){
  console.log(detailId)
  console.log(action)
  console.log(user)
  if (user === 'AnonymousUSer'){
    addCookieItem()
  }else {
    updateUserOrder(detailId,action)

  }
}

function addCookieItem(detailId,action){
    console.log('Not logged in')
}

function updateUserOrder(detailId,action){
    console.log('User is logged in,sending data')
    var url='/sent_items/update_items/'
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'detailId':detailId,'action':action})
    })
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('data:',data)
        location.reload()
    })
}
/***  for adding to cart ***/

<!---------------------------- disable addtodispatch button --------------------------------->
$(document).ready(function(){
    var java_content_type_id = $("#content_type_id").data("value");
    var java_joined_ids = $("#joined_ids").data("value");
    var buttons=$(".addtodispatch");
    var java_detailId=[];
    var java_detailId_content_type_id=[];
    for(x=0;x<buttons.length;x++)
    {
    $('button.addtodispatch').each(function() {
        java_detailId[x++]= parseInt($(this).attr("data-detail"));
    });

    }
    for(y=0;y<java_detailId.length;y++)
    {
        java_detailId_content_type_id[y]=[java_detailId[y],java_content_type_id]
    }
    for(let i = 0; i<java_detailId_content_type_id.length; i++)
    {
        for(let j = 0; j<java_joined_ids.length; j++)
        {
                if(JSON.stringify(java_detailId_content_type_id[i])==JSON.stringify(java_joined_ids[j]))
                {
                    $(`button[data-detail="${java_detailId_content_type_id[i][i-i]}"]`).attr("disabled", true)
                    break;
                } else
                    {
                            $(`button[data-detail="${java_detailId_content_type_id[i][i-i]}"]`).attr("disabled", false)
                    }
        }
    }
});

<!---------------------------- Ajax bulk delete --------------------------------------------->

    $(document).ready(function(){
            $('.bulk_delete').click(function(){
                var id=[];
                var item_id=$("#item_id").data("value");
                var currentURL = window.location.href;
                var csrf=$('input[name=csrfmiddlewaretoken]').val();
                $(':checkbox:checked').each(function(i){
                        id[i]=$(this).val()
                 })
                    if(id.length===0){
                           swal("Error!", "Please select the toners to Delete", "error");
                    }
                    else{ swal({
                                  title: "Are you sure?",
                                  text: "You will not be able to recover this record!",
                                  icon: "warning",
                                  buttons: [
                                    'No, cancel it!',
                                    'Yes, I am sure!'
                                  ],
                                  dangerMode: true,
                                }).then(function(isConfirm) {
                                  if (isConfirm) {
                                    if (currentURL.indexOf("view_tonerdetails") !== -1)
                                       {
                                            $.ajax({
                                            url:'' + item_id +'/view_tonerdetails_bulk_delete' ,
                                            method:"POST",
                                            data:{
                                                id:id,
                                                csrfmiddlewaretoken:csrf
                                            },

                                            success:function(response){
                                                for(var i=0;i<id.length;i++){
                                                    $('tr#'+id[i]+'').css('background-color','#ccc');
                                                    $('tr#'+id[i]+'').fadeOut('slow');

                                                }

                                            }
                                            })
                                       }
                                    else
                                        {

                                            $.ajax({
                                            url:'' + item_id +'/view_itemdetails_bulk_delete' ,
                                            method:"POST",
                                            data:{
                                                id:id,
                                                csrfmiddlewaretoken:csrf
                                            },

                                            success:function(response){
                                                for(var i=0;i<id.length;i++){
                                                    $('tr#'+id[i]+'').css('background-color','#ccc');
                                                    $('tr#'+id[i]+'').fadeOut('slow');

                                                }

                                            }
                                            })
                                        }
                                    swal({
                                      title: 'Deleted!',
                                      text: 'Records are successfully deleted!',
                                      icon: 'success'
                                    })

                                  } else {
                                    swal("Cancelled", "Your records are safe", "error");
                                  }
                                });

                    }
            })
    })

<!---------------------------- Ajax bulk delete --------------------------------------------->



<!--------------------------------------- Paginator and keyup Search ----------------------------->

$(document).ready(function ()
    {
            var currentURL = window.location.href;
            if (currentURL.indexOf("view_sent_items") !== -1)
                {
                    var table = $('#myTable').DataTable
                        ({
                                paging: true,
                                pageLength: 10,
                                lengthChange: false,
                                bInfo: false,
                                bSort: false,
                                order:[],
                                dom: 'ltiBfrp',
                                buttons:[
                                   {
                                        extend: 'excel',
                                        text:   '<i class="fas fa-file-excel"></i>',
                                        className:  'btn-exporttocsv',
                                        titleAttr:  'Excel',

                                    },
                               ]
                        });
                }
            else
                {
                     var table = $('#myTable').DataTable
                        ({
                                paging: true,
                                pageLength: 10,
                                lengthChange: false,
                                bInfo: false,
                                bSort: false,
                                order:[]
                        });

                }
            $('#search').on( 'keyup', function ()
            {
                table.search( this.value ).draw();
            });
    });

<!---------------------------- Ajax bulk add to dispatch --------------------------------------------->

        $(document).ready(function() {
            $("#btn-bulkdispatch").click(function() {
                var selectedIds = [];
                var csrf=$('input[name=csrfmiddlewaretoken]').val();
                $(':checkbox:checked').each(function() {
                    selectedIds.push($(this).val());
                });

                $.ajax({
                    type: "POST",
                    url:'/sent_items/bulk_update_items/',
                    data: { selected_ids: selectedIds,
                            csrfmiddlewaretoken:csrf
                     },
                    success: function(response) {
                        window.location.reload();
                    },
                    error: function(xhr, errmsg, err) {
                        console.log(xhr.status + ": " + xhr.responseText);
                    }
                });
            });
        });

<!------------------------------------------------- Date picker --------------------------------------------------------------->

    $(document).ready(function(){
        $("#date_dispatched").datepicker({

            format: 'yyyy-mm-dd',
            todayBtn : 'linked',
            todayHighlight: true,
            autoclose: true,
            orientation: 'auto bottom'
        });

    });


$(document).ready(function(){
        $('.dropdown-menu a.dropdown-toggle').on('click', function(e) {
          if (!$(this).next().hasClass('show')) {
            $(this).parents('.dropdown-menu').first().find('.show').removeClass("show");
          }
          var $subMenu = $(this).next(".dropdown-menu");
          $subMenu.toggleClass('show');


          $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function(e) {
            $('.dropdown-submenu .show').removeClass("show");
          });


          return false;
        });
});

<!---------------------------- Ajax remove selected from dispatch --------------------------------------------->

        $(document).ready(function()
        {
            $("#btn-selectremove").click(function()
            {
                var selectedIds = [];
                var csrf=$('input[name=csrfmiddlewaretoken]').val();
                $(':checkbox:checked').each(function(i){
                        selectedIds[i]=$(this).val()
                })
                if(selectedIds.length==0)
                {
                           swal("Error!", "Please select the items to Remove", "error");
                }
                else
                {           swal
                              ({
                                      title: "Are you sure?",
                                      text: "You will remove selected items from dispatch!",
                                      icon: "warning",
                                      buttons: [
                                        'No, cancel it!',
                                        'Yes, I am sure!'
                                      ],
                                      dangerMode: true,
                              }).then(function(isConfirm)
                              {
                                  if (isConfirm)
                                  {
                                                    $.ajax({
                                                    type: "POST",
                                                    url:'select_remove_from_cart/',
                                                    data: { selected_ids: selectedIds,
                                                            csrfmiddlewaretoken:csrf
                                                     },
                                                    success: function(response)
                                                    {
                                                        for(var i=0;i<selectedIds.length;i++)
                                                        {
															$('tr#'+selectedIds[i]+'').css('background-color','#ccc');
															$('tr#'+selectedIds[i]+'').fadeOut('slow');

														}

                                                    },
                                                    error: function(xhr, errmsg, err)
                                                    {
                                                        console.log(xhr.status + ": " + xhr.responseText);
                                                    }
                                                });
                                                swal
                                                ({
                                                      title: 'Removed!',
                                                      text: selectedIds.length+' Items are successfully removed!',
                                                      icon: 'success'
                                                }).then((willReload)=>{
                                                    if (willReload){
                                                        window.location.reload();
                                                    }
                                                });

                                  }
                                  else
                                  {
                                    swal("Cancelled",selectedIds.length+" Items still in dispatch", "error");
                                  }
                              });
                }
            });
        });

<!---------------------------- Ajax selected dispatch --------------------------------------------->

        $(document).ready(function() {
            $("#btn-selectdispatch").click(function() {
                var selectedIds = [];
                var csrf=$('input[name=csrfmiddlewaretoken]').val();
                $(':checkbox:checked').each(function() {
                    selectedIds.push($(this).val());
                });
                if(selectedIds.length==0)
                {
                           swal("Error!", "Please select the items to Dispatch", "error");
                }
                else
                {           swal
                              ({
                                      title: "Are you sure?",
                                      text: "You will dispatch the selected items!",
                                      icon: "warning",
                                      buttons: [
                                        'No, cancel it!',
                                        'Yes, I am sure!'
                                      ],
                                      dangerMode: true,
                              }).then(function(isConfirm)
                              {
                                  if (isConfirm)
                                  {
                                        $.ajax({
                                            type: "POST",
                                            url:'select_dispatch/',
                                            data: { selected_ids: selectedIds,
                                                    csrfmiddlewaretoken:csrf
                                             },
                                            success: function(response)
                                            {
                                                for(var i=0;i<selectedIds.length;i++)
                                                {
                                                    $('tr#'+selectedIds[i]+'').css('background-color','#ccc');
                                                    $('tr#'+selectedIds[i]+'').fadeOut('slow');

                                                }
                                            },
                                            error: function(xhr, errmsg, err) {
                                                console.log(xhr.status + ": " + xhr.responseText);
                                            }
                                        });
                                        swal
                                        ({
                                            title: 'Dispatched!',
                                            text: selectedIds.length+' Items are successfully dispatched!',
                                            icon: 'success'
                                        }).then((willReload)=>{
                                                if (willReload){
                                                  window.location.reload();
                                                }
                                        });
                                  }
                                  else
                                  {
                                    swal("Cancelled",selectedIds.length+" Items still in dispatch", "error");
                                  }
                              });
                }
            });
        });
