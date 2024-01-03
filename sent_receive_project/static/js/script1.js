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
        $("#purchased_date").datepicker({

            format: 'yyyy-mm-dd',
            todayBtn : 'linked',
            todayHighlight: true,
            autoclose: true,
            orientation: 'auto bottom'
        });
   });
     $(document).ready(function(){
        $("#date_dispatched").daterangepicker({

            singleDatePicker: true,
            opens: 'left',  // Adjust this based on your preference

            "showDropdowns": true,
            ranges: {
                'Today': [moment(), moment()],

            },
            autoUpdateInput: true,  // auto-updating the input field
            minYear: 2022,

            locale: {
            format: 'YYYY-MM-DD', // Format of the selected date
            cancelLabel: 'Clear' // Label for the "Clear" button
            }

        });

          // Update the save button when the date picker values change
        $("#date_dispatched").on('apply.daterangepicker', function (ev, picker) {
            var selectedDate = picker.startDate.format('YYYY-MM-DD');
            var originalDate = $("#date_dispatched2").val();

            if (selectedDate === originalDate) {
                $(".btn-action-ETDF").prop("disabled", true);
                $(".btn-action-EIDF").prop("disabled", true);
            } else {
                $(".btn-action-ETDF").prop("disabled", false);
                $(".btn-action-EIDF").prop("disabled", false);
            }
        });

         // Clear the input field when "Clear" is clicked
         $("#date_dispatched").on('cancel.daterangepicker', function () {
            $(this).val('');
            $(".btn-action-ETDF").prop("disabled", true);
            $(".btn-action-EIDF").prop("disabled", true);
        });
    });


<!---------------------------- Date range picker on toner status chart --------------------------------------------->
     $(document).ready(function() {
        // Initialize the date picker
        $("#datepicker").daterangepicker({
            opens: 'left',  // Adjust this based on your preference
            "showDropdowns": true,
            "linkedCalendars": false,
            autoUpdateInput: false,  // Prevent auto-updating the input field

        });

        // Update the chart when the date picker values change
        $("#datepicker").on('apply.daterangepicker', function(ev, picker) {
            var start_date = picker.startDate.format('YYYY-MM-DD');
            var end_date = picker.endDate.format('YYYY-MM-DD');

            // Redirect to the same page with updated date range as a query parameter
            window.location.href = window.location.pathname + '?start_date=' + start_date + '&end_date=' + end_date;
        });
    });

<!---------------------------- Dropdown menus --------------------------------------------->
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

<!---------------------------- Ajax print selected items sent invoice --------------------------------------------->

        $(document).ready(function() {
            $(".select_print_sent_items_invoice").click(function(e) {
                e.preventDefault();
                var selectedIds = [];
                var csrf=$('input[name=csrfmiddlewaretoken]').val();
                var id=$("#cart_id").data("value");
                $(':checkbox:checked').each(function() {
                    selectedIds.push($(this).val());
                });
                if (selectedIds.length > 0) {
                        var url = '/forms/select_print_sent_items_invoice/';
                        fetch(url, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': csrf,
                            },
                            body: JSON.stringify({
                                'selected_ids': selectedIds,  // Use underscore instead of camelCase
                                'id': id
                            })
                        })
                        .then((response) => response.blob())
                        .then(blob => {
                                var blobUrl = URL.createObjectURL(blob);
                                window.open(blobUrl, '_blank');
                        })
                        .catch(error => {
                                console.error('Error:', error);
                        });
                } else {
                        $("#pdf-generation-status").text("Please select items to generate PDF.");
                }
            });
        });



       /* $(document).ready(function() {
            $(window).on('beforeunload', function() {
                $.ajax({
                    url: '/login/',  // Replace with your logout URL
                    type: 'GET',
                    async: false,  // Ensure the request completes before the page unloads
                });
            });
        });*/


    document.addEventListener("DOMContentLoaded", function() {
        var expandButtons = document.querySelectorAll('.expand-btn');

        expandButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                var modalId = this.dataset.bsTarget;
                var modal = new bootstrap.Modal(document.getElementById(modalId));
                modal.show();
            });
        });
    });



function showNoPdfAlert() {
                                Swal.fire({
                                    icon: 'info',
                                    title: 'No PDF file',
                                    text: 'There is no PDF file uploaded for this contract.',
                                    confirmButtonText: 'OK'
                                });
}



