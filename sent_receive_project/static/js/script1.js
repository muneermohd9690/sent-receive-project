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
    var content_type_id = $("#content_type_id")?.data("value");
    var joined_ids = $("#joined_ids")?.data("value");

    // Debug logs
    console.log('content_type_id:', content_type_id);
    console.log('joined_ids:', joined_ids);

    // Only proceed if joined_ids is defined and is an array
    if (joined_ids && Array.isArray(joined_ids)) {
        var joinedIdsSet = new Set(joined_ids.map(item => JSON.stringify(item)));

        $('.addtodispatch').each(function() {
            var detailId = parseInt($(this).attr("data-detail"));
            var detailContentTypePair = JSON.stringify([detailId, content_type_id]);

            if (joinedIdsSet.has(detailContentTypePair)) {
                $(this).attr("disabled", true);
            } else {
                $(this).attr("disabled", false);
            }
        });
    } else {
        console.warn('joined_ids is not available or not an array, skipping addtodispatch logic');
    }
});

<!---------------------------- Ajax bulk delete --------------------------------------------->

$(document).ready(function(){
    // Define a global array to store selected bulk delete item IDs
    var selectedBulkDeleteIds = [];

    // Update the array when a bulk delete checkbox is clicked
    $('body').on('change', 'input[name="detail_id[]"]', function() {
        var itemId = $(this).val();
        if ($(this).is(':checked')) {
            // Add to the array if the bulk delete checkbox is checked
            selectedBulkDeleteIds.push(itemId);
        } else {
            // Remove from the array if the bulk delete checkbox is unchecked
            selectedBulkDeleteIds = selectedBulkDeleteIds.filter(id => id !== itemId);
        }
    });

    $('.bulk_delete').click(function(){
        var item_id = $("#item_id").data("value");
        var csrf = $('input[name=csrfmiddlewaretoken]').val();
        var currentURL = window.location.href;
        if (selectedBulkDeleteIds.length === 0) {
            swal("Error!", "Please select the items to delete", "error");
        } else {
            swal({
                title: "Are you sure?",
                text: "You will not be able to recover these records!",
                icon: "warning",
                buttons: [
                    'No, cancel it!',
                    'Yes, I am sure!'
                ],
                dangerMode: true,
            }).then(function(isConfirm) {
                if (isConfirm) {
                    // Determine the correct AJAX URL based on your conditions
                    var ajaxURL = (currentURL.indexOf("view_tonerdetails") !== -1) ?
                        item_id + '/view_tonerdetails_bulk_delete' :
                        item_id + '/view_itemdetails_bulk_delete';

                    $.ajax({
                        url: ajaxURL,
                        method: "POST",
                        data: {
                            id: selectedBulkDeleteIds,
                            csrfmiddlewaretoken: csrf
                        },
                        success: function(response) {
                            for (var i = 0; i < selectedBulkDeleteIds.length; i++) {
                                $('tr#' + selectedBulkDeleteIds[i] + '').css('background-color', '#ccc');
                                $('tr#' + selectedBulkDeleteIds[i] + '').fadeOut('slow');
                            }
                        },
                        error: function(xhr, errmsg, err) {
                            console.log(xhr.status + ": " + xhr.responseText);
                        }
                    });

                    swal({
                        title: 'Deleted!',
                        text: + selectedBulkDeleteIds.length + ' Records are successfully deleted!',
                        icon: 'success'
                    }).then((willReload) => {
                        if (willReload) {
                            window.location.reload();
                        }
                    });

                } else {
                    swal("Cancelled", "Your records are safe", "error");
                }
            });
        }
    });
});

<!---------------------------- Ajax bulk delete --------------------------------------------->



<!--------------------------------------- Paginator and keyup Search ----------------------------->

var table;
$(document).ready(function ()
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


            $('#search').on( 'keyup', function ()
            {
                table.search( this.value ).draw();
            });
    });

<!---------------------------- Ajax bulk add to dispatch --------------------------------------------->

// Define a global array to store selected bulk dispatch item IDs
var selectedBulkDispatchIds = [];

$(document).ready(function() {
    // Update the array when a bulk dispatch checkbox is clicked
    $('body').on('change', 'input[name="detail_id[]"]', function() {
        var itemId = $(this).val();
        if ($(this).is(':checked')) {
            // Add to the array if the bulk dispatch checkbox is checked
            selectedBulkDispatchIds.push(itemId);
        } else {
            // Remove from the array if the bulk dispatch checkbox is unchecked
            selectedBulkDispatchIds = selectedBulkDispatchIds.filter(id => id !== itemId);
        }
    });

    // Handle bulk dispatching for all selected items
    $("#btn-bulkdispatch").click(function() {
        var csrf = $('input[name=csrfmiddlewaretoken]').val();

        if (selectedBulkDispatchIds.length == 0) {
            swal("Error!", "Please select the items for bulk dispatch", "error");
        } else {
            $.ajax({
                type: "POST",
                url: '/sent_items/bulk_update_items/',
                data: {
                    selected_ids: selectedBulkDispatchIds,
                    csrfmiddlewaretoken: csrf
                },
                success: function(response) {
                    window.location.reload();
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            });
        }
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

// Define a global array to store selected removal item IDs
var selectedRemoveIds = [];

$(document).ready(function() {
    // Update the array when a remove checkbox is clicked
    $('body').on('change', 'input[name="item_id[]"]', function() {
        var itemId = $(this).val();
        if ($(this).is(':checked')) {
            // Add to the array if the remove checkbox is checked
            selectedRemoveIds.push(itemId);
        } else {
            // Remove from the array if the remove checkbox is unchecked
            selectedRemoveIds = selectedRemoveIds.filter(id => id !== itemId);
        }
    });

    // Handle removing for all selected removal items
    $("#btn-selectremove").click(function() {
        var csrf = $('input[name=csrfmiddlewaretoken]').val();

        if (selectedRemoveIds.length == 0) {
            swal("Error!", "Please select the items to Remove", "error");
        } else {
            swal({
                title: "Are you sure?",
                text: "You will remove selected items from dispatch!",
                icon: "warning",
                buttons: [
                    'No, cancel it!',
                    'Yes, I am sure!'
                ],
                dangerMode: true,
            }).then(function(isConfirm) {
                if (isConfirm) {
                    $.ajax({
                        type: "POST",
                        url: 'select_remove_from_cart/',
                        data: {
                            selected_ids: selectedRemoveIds,
                            csrfmiddlewaretoken: csrf
                        },
                        success: function(response) {
                            for (var i = 0; i < selectedRemoveIds.length; i++) {
                                $('tr#' + selectedRemoveIds[i] + '').css('background-color', '#ccc');
                                $('tr#' + selectedRemoveIds[i] + '').fadeOut('slow');
                            }
                        },
                        error: function(xhr, errmsg, err) {
                            console.log(xhr.status + ": " + xhr.responseText);
                        }
                    });
                    swal({
                        title: 'Removed!',
                        text: selectedRemoveIds.length + ' Items are successfully removed!',
                        icon: 'success'
                    }).then((willReload) => {
                        if (willReload) {
                            window.location.reload();
                        }
                    });
                } else {
                    swal("Cancelled", selectedRemoveIds.length + " Items still in dispatch", "error");
                }
            });
        }
    });
});


<!---------------------------- Ajax selected dispatch --------------------------------------------->

    // Define a global array to store selected dispatch item IDs
var selectedDispatchIds = [];

$(document).ready(function() {
    // Update the array when a dispatch checkbox is clicked
    $('body').on('change', 'input[name="item_id[]"]', function() {
        var itemId = $(this).val();
        if ($(this).is(':checked')) {
            // Add to the array if the dispatch checkbox is checked
            selectedDispatchIds.push(itemId);
        } else {
            // Remove from the array if the dispatch checkbox is unchecked
            selectedDispatchIds = selectedDispatchIds.filter(id => id !== itemId);
        }
    });

    // Handle dispatching for all selected dispatch items
    $("#btn-selectdispatch").click(function() {
        var csrf = $('input[name=csrfmiddlewaretoken]').val();

        if (selectedDispatchIds.length == 0) {
            swal("Error!", "Please select the items to Dispatch", "error");
        } else {
            swal({
                title: "Are you sure?",
                text: "You will dispatch the selected items!",
                icon: "warning",
                buttons: [
                    'No, cancel it!',
                    'Yes, I am sure!'
                ],
                dangerMode: true,
            }).then(function(isConfirm) {
                if (isConfirm) {
                    $.ajax({
                        type: "POST",
                        url: 'select_dispatch/',
                        data: {
                            selected_ids: selectedDispatchIds,
                            csrfmiddlewaretoken: csrf
                        },
                        success: function(response) {
                            for (var i = 0; i < selectedDispatchIds.length; i++) {
                                $('tr#' + selectedDispatchIds[i] + '').css('background-color', '#ccc');
                                $('tr#' + selectedDispatchIds[i] + '').fadeOut('slow');
                            }
                        },
                        error: function(xhr, errmsg, err) {
                            console.log(xhr.status + ": " + xhr.responseText);
                        }
                    });
                    swal({
                        title: 'Dispatched!',
                        text: selectedDispatchIds.length + ' Items are successfully dispatched!',
                        icon: 'success'
                    }).then((willReload) => {
                        if (willReload) {
                            window.location.reload();
                        }
                    });
                } else {
                    swal("Cancelled", selectedDispatchIds.length + " Items still in dispatch", "error");
                }
            });
        }
    });
});


<!---------------------------- Ajax print selected items sent invoice --------------------------------------------->

var selectedIds = [];

$(document).ready(function() {
    // Update the array when a checkbox is clicked
    $('body').on('change', 'input[name="item_id[]"]', function() {
        var itemId = $(this).val();
        if ($(this).is(':checked')) {
            // Add to the array if the checkbox is checked
            selectedIds.push(itemId);
        } else {
            // Remove from the array if the checkbox is unchecked
            selectedIds = selectedIds.filter(id => id !== itemId);
        }
    });

    // Handle invoicing for all selected checkboxes
    $(".select_print_sent_items_invoice").click(function(e) {
        e.preventDefault();
        var csrf = $('input[name=csrfmiddlewaretoken]').val();
        var id = $("#cart_id").data("value");

        if (selectedIds.length > 0) {
            var url = '/forms/select_print_sent_items_invoice/';
            fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrf,
                    },
                    body: JSON.stringify({
                        'selected_ids': selectedIds,
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


<!---------------------------- Contracts pdf show message no pdf available --------------------------------------------->
function showNoPdfAlert() {
                                Swal.fire({
                                    icon: 'info',
                                    title: 'No PDF file',
                                    text: 'There is no PDF file uploaded for this contract.',
                                    confirmButtonText: 'OK'
                                });
}

<!---------------------------- Logic to show edit item details modal, swal message, highlight edited row letters ------->
/*
var pageIdentifier = 'edit_item_details';

function handleFormSubmission(event) {
    event.preventDefault();
    var currentRowId = $("#item_id").data("value");


    Swal.fire({
        title: 'Confirm Changes',
        text: 'Are you sure you want to save changes?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, save it!'
    }).then((result) => {
        if (result.isConfirmed) {
            submitForm();
            $('#editItemDetailsModal').modal('hide');
            console.log('Applying visual effect to row:', currentRowId);
        } else {
            swal("Cancelled", "No changes were made", "error");
            $('#editItemDetailsModal').modal('hide');
        }
    });
}

function submitForm() {
    var formData = $('#editItemDetailsForm').serialize();
    var currentRowId = $("#item_id").data("value");


    $.ajax({
        type: 'POST',
        url: 'edit_item_details_save',
        data: formData,
        success: function (data) {
            applyVisualEffectAndStore(currentRowId);
            Swal.fire({
                title: 'Changes Saved',
                text: 'Your changes have been successfully saved.',
                icon: 'success'
            }).then(() => {
                                location.reload();
            });
//            table.ajax.reload();
        },
        error: function (error) {
            console.error('Error saving data:', error);
            // Handle errors if needed
        }
    });
}

function applyVisualEffectAndStore(currentRowId) {
    console.log('Applying visual effect to row:', currentRowId);
    var $row = $('#' + currentRowId);
    $row.find('td:not(:last-child)').each(function () {
        var $cell = $(this);
        var originalText = $cell.text();
        var highlightedText = '<span class="highlight">' + originalText + '</span>';
        $cell.html(highlightedText);
    });

//    localStorage.setItem('currentHighlightedRow', currentRowId);
    sessionStorage.setItem('currentHighlightedRow', currentRowId);
    setTimeout(function () {
        console.log('Removing visual effect from row:', currentRowId);
        $row.find('td:not(:last-child)').each(function () {
            var $cell = $(this);
            $cell.html($cell.find('.highlight').text());
        });
    }, 5000);
}

function checkAndApplyHighlight() {
//    var currentHighlightedRow = localStorage.getItem('currentHighlightedRow');
    var currentHighlightedRow = sessionStorage.getItem('currentHighlightedRow');
    if (currentHighlightedRow) {
        // Check if the current page URL contains the specified substring
        if (currentPageUrl.includes(pageIdentifier)) {
            applyVisualEffectAndStore(currentHighlightedRow);
            sessionStorage.removeItem('currentHighlightedRow');
        }
    }
}
var currentPageUrl = window.location.href;
$(document).ready(function () {
    checkAndApplyHighlight();
    $('body').on('submit', '#editItemDetailsForm', handleFormSubmission);
});

function openModal(detailId) {
    var modalId = '#editItemDetailsModal';

    // Set modal title
    $(modalId + 'Label').text('Edit Item Details - ' + detailId);

    // Set modal body content
    $.ajax({
        url: 'edit_item_details_modal/',
        type: 'GET',
        data: { detail_id: detailId },
        success: function (response) {
            $(modalId + ' .modal-body').html(response);

            // Show the modal
            $(modalId).modal('show');
        },
        error: function (error) {
            console.error('Error fetching data:', error);
        }
    });
}

// Listen for the modal being shown
$(document).on('shown.bs.modal', '#editItemDetailsModal', function () {
    // Initialize date picker after the modal is shown
    $(".datepicker").daterangepicker({
        singleDatePicker: true,
        opens: 'left',
        "showDropdowns": true,
        ranges: {
            'Today': [moment(), moment()],
        },
        autoUpdateInput: true,
        minYear: 2022,
        locale: {
            format: 'YYYY-MM-DD',
            cancelLabel: 'Clear'
        }
    });
});
*/
//Edit item details page

//Edit item details page server side processing------------------------------------------------------------------------
//var pageIdentifier = 'edit_item_details';
//
//function handleFormSubmission(event) {
//    event.preventDefault();
//    var currentRowId = $("#item_id").data("value");
//
//    Swal.fire({
//        title: 'Confirm Changes',
//        text: 'Are you sure you want to save changes?',
//        icon: 'warning',
//        showCancelButton: true,
//        confirmButtonColor: '#3085d6',
//        cancelButtonColor: '#d33',
//        confirmButtonText: 'Yes, save it!'
//    }).then((result) => {
//        if (result.isConfirmed) {
//            submitForm();
//            $('#editItemDetailsModal').modal('hide');
//        } else {
//            Swal.fire("Cancelled", "No changes were made", "error");
//            $('#editItemDetailsModal').modal('hide');
//        }
//    });
//}
//
//function submitForm() {
//    var formData = $('#editItemDetailsForm').serialize();
//    var currentRowId = $("#item_id").data("value");
//
//    $.ajax({
//        type: 'POST',
////        url: 'edit_item_details_save/',
//        url: "{% url 'edit_item_details_save' %}",
//        data: formData,
//        success: function (data) {
//            applyVisualEffectAndStore(currentRowId);
//            Swal.fire({
//                title: 'Changes Saved',
//                text: 'Your changes have been successfully saved.',
//                icon: 'success'
//            }).then(() => {
//                $('#itemDetailsTable').DataTable().ajax.reload();
//            });
//        },
//        error: function (error) {
//            console.error('Error saving data:', error);
//            Swal.fire('Error', 'Failed to save changes.', 'error');
//        }
//    });
//}
//
//function applyVisualEffectAndStore(currentRowId) {
//    console.log('Applying visual effect to row:', currentRowId);
//    var $row = $('#itemDetailsTable').find(`tr[data-id="${currentRowId}"]`);
//    $row.find('td:not(:last-child)').each(function () {
//        var $cell = $(this);
//        var originalText = $cell.text();
//        var highlightedText = '<span class="highlight">' + originalText + '</span>';
//        $cell.html(highlightedText);
//    });
//
//    sessionStorage.setItem('currentHighlightedRow', currentRowId);
//    setTimeout(function () {
//        console.log('Removing visual effect from row:', currentRowId);
//        $row.find('td:not(:last-child)').each(function () {
//            var $cell = $(this);
//            $cell.html($cell.find('.highlight').text());
//        });
//    }, 5000);
//}
//
//function checkAndApplyHighlight() {
//    var currentHighlightedRow = sessionStorage.getItem('currentHighlightedRow');
//    if (currentHighlightedRow && currentPageUrl.includes(pageIdentifier)) {
//        applyVisualEffectAndStore(currentHighlightedRow);
//        sessionStorage.removeItem('currentHighlightedRow');
//    }
//}
//
//var currentPageUrl = window.location.href;
//
//function openModal(detailId) {
//    var modalId = '#editItemDetailsModal';
//    $(modalId + 'Label').text('Edit Item Details - ' + detailId);
//
//    $.ajax({
//        url: 'edit_item_details_modal/',
//        type: 'GET',
//        data: { detail_id: detailId },
//        success: function (response) {
//            $(modalId + ' .modal-body').html(response);
//            $(modalId).modal('show');
//            $('.select2').select2({
//                ajax: {
//                    url: 'search_dropdown_options/',
//                    dataType: 'json',
//                    delay: 250,
//                    data: function (params) {
//                        return {
//                            q: params.term || '',
//                            model: $(this).attr('name').replace('_no', '')
//                        };
//                    },
//                    processResults: function (data) {
//                        return {
//                            results: data.results
//                        };
//                    },
//                    cache: true
//                },
//                minimumInputLength: 1,
//                placeholder: 'Search...',
//                allowClear: true
//            });
//        },
//        error: function (error) {
//            console.error('Error fetching data:', error);
//            Swal.fire('Error', 'Failed to load modal content.', 'error');
//        }
//    });
//}
//
//$(document).ready(function () {
//    checkAndApplyHighlight();
//    $('body').on('submit', '#editItemDetailsForm', handleFormSubmission);
//    var csrf = $('input[name=csrfmiddlewaretoken]').val();
//    // Initialize DataTables with server-side processing
//    var table =$('#itemDetailsTable').DataTable({
//        processing: true,
//        serverSide: true,
//
//        ajax: {
//            url: '/items/item_details_datatable/',  // this is the same view you use now
//            type: 'POST',
//            headers: {
//                    'X-CSRFToken':csrftoken,
//            },
//        },
//        columns: [
//            { data: 'model_no' },
//            { data: 'serial_no' },
//            { data: 'tag_no' },
//            { data: 'room_tag' },
//            { data: 'issued_to' },
//            { data: 'date_dispatched' },
//            { data: 'employee_name' },
//            { data: 'employee_designation' },
//            { data: 'lpo_no' },
//            { data: 'action'},
//        ],
//        pageLength: 10,
//        responsive: true,
//        bSort: false,
//        scrollX: true,
//        autoWidth: false,
//          // Default sort by date_dispatched descending
//    });
//    // Attach the search box
//    $('#search').on('keyup', function () {
//        table.search(this.value).draw();
//    });
//});
//
//$(document).on('shown.bs.modal', '#editItemDetailsModal', function () {
//    $(".datepicker").daterangepicker({
//        singleDatePicker: true,
//        opens: 'left',
//        showDropdowns: true,
//        ranges: {
//            'Today': [moment(), moment()],
//        },
//        autoUpdateInput: true,
//        minYear: 2022,
//        locale: {
//            format: 'YYYY-MM-DD',
//            cancelLabel: 'Clear'
//        }
//    });
//});
//var pageIdentifier = 'edit_item_details';
//var currentPageUrl = window.location.href;
//
//// 1. Updated Submission Handler
//function handleFormSubmission(event) {
//    event.preventDefault();
//
//    // Grab the form and the unique ID for the item being edited
//    var $form = $(event.target);
//    var currentRowId = $form.find('input[name="detail_id"]').val(); // Use the hidden input
//
//    Swal.fire({
//        title: 'Confirm Changes',
//        text: 'Are you sure you want to save changes?',
//        icon: 'warning',
//        showCancelButton: true,
//        confirmButtonColor: '#e91e63', // Your Pink Color
//        cancelButtonColor: '#d33',
//        confirmButtonText: 'Yes, save it!'
//    }).then((result) => {
//        if (result.isConfirmed) {
//            submitForm($form, currentRowId); // Pass context to submitForm
//        } else {
//            // Optional: Don't hide modal on cancel if user just wants to go back to editing
//            // $('#editItemDetailsModal').modal('hide');
//        }
//    });
//}
//
//// 2. Updated Submit Function (Fixed URL 404 issue)
//function submitForm($form, currentRowId) {
//    // FormData handles both text AND files automatically
//    var formData = new FormData($form[0]);
//    formData.append("is_ajax", "true");// Manually force the flag
//    var saveUrl = $form.attr('action');
//
//    $.ajax({
//        type: 'POST',
//        url: saveUrl,
//        data: formData,
//        processData: false, // Tell jQuery not to process the data
//        contentType: false, // Tell jQuery not to set contentType
//        success: function (response) {
//            applyVisualEffectAndStore(currentRowId);
//            $form.closest('.modal').modal('hide');
//
//            Swal.fire({
//                title: 'Saved!',
//                text: data.message,
//                icon: 'success',
//                confirmButtonColor: '#e91e63'
//            }).then(() => {
//                // STEP C: Reload table. drawCallback will handle the highlight automatically
//                if ($.fn.DataTable.isDataTable('#itemDetailsTable')) {
//                    $('#itemDetailsTable').DataTable().ajax.reload(null, false);
//                }
//            });
//        },
//        error: function (xhr) {
//            Swal.fire('Error', 'Failed to save changes.', 'error');
//        }
//    });
//}
//
//// 3. Highlight Effect Logic
//function applyVisualEffectAndStore(currentRowId) {
//    // We search for the row by data-id attribute (Ensure your DataTable rows have this)
//    var $row = $('#itemDetailsTable').find(`tr[data-id="${currentRowId}"]`);
//
//    if ($row.length > 0) {
//        $row.addClass('table-info'); // Use Bootstrap class for immediate feedback
//        $row.find('td:not(:last-child)').each(function () {
//            var $cell = $(this);
//            $cell.wrapInner('<span class="highlight"></span>');
//        });
//
//        sessionStorage.setItem('currentHighlightedRow', currentRowId);
//
//        setTimeout(function () {
//            $row.removeClass('table-info');
//            $row.find('.highlight').contents().unwrap();
//        }, 5000);
//    }
//}
//
//// 4. Modal Open Logic (Added dynamic ID handling)
//function openModal(detailId) {
//    var modalSelector = '#editItemDetailsModal'; // Use base modal ID
//
//    $.ajax({
//        url: '/items/edit_item_details_modal/',
//        type: 'GET',
//        data: { detail_id: detailId },
//        success: function (response) {
//            $(modalSelector + ' .modal-body').html(response);
//            $(modalSelector).modal('show');
//
//            // Re-initialize plugins inside the new content
//            $('.select2').select2({
//                dropdownParent: $(modalSelector), // Critical for Select2 inside Modals
//                ajax: {
//                    url: 'search_dropdown_options/',
//                    dataType: 'json',
//                    delay: 250,
//                    data: function (params) {
//                        return {
//                            q: params.term || '',
//                            model: $(this).attr('name').replace('_no', '')
//                        };
//                    }
//                }
//            });
//        },
//        error: function (error) {
//            Swal.fire('Error', 'Failed to load data.', 'error');
//        }
//    });
//}
//
//// 5. Document Ready & Global Listeners
//$(document).ready(function () {
//    checkAndApplyHighlight();
//
//    // Listen for form submission inside ANY modal
//    $('body').on('submit', '#editItemDetailsForm', handleFormSubmission);
//
//    // DataTable definition...
//    var table = $('#itemDetailsTable').DataTable({
//        // ... your settings ...
//        createdRow: function(row, data, dataIndex) {
//            // CRITICAL: This adds the ID to the row so the highlight knows where to go
//            $(row).attr('data-id', data.id);
//        }
//    });
//});
//var currentPageUrl = window.location.href;
//
//function openModal(detailId) {
//    // We use a constant ID for the container, but the form inside can be dynamic
//    var modalSelector = '#editItemDetailsModal';
//
//    // Update label to show which item we are editing
//    $(modalSelector + 'Label').text('Edit Item Details - ' + detailId);
//
//    $.ajax({
//        // Leading slash ensures it works from any sub-page
//        url: '/items/edit_item_details_modal/',
//        type: 'GET',
//        data: { detail_id: detailId },
//        success: function (response) {
//            // Inject the form HTML into the modal body
//            $(modalSelector + ' .modal-body').html(response);
//            $(modalSelector).modal('show');
//
//            // Initialize Select2 AFTER the HTML is injected
//            $('.select2').select2({
//                // CRITICAL: This allows Select2 to work inside a Bootstrap Modal
//                dropdownParent: $(modalSelector),
//                ajax: {
//                    url: '/items/search_dropdown_options/',
//                    dataType: 'json',
//                    delay: 250,
//                    data: function (params) {
//                        return {
//                            q: params.term || '',
//                            // Extracts 'model' or 'room' etc from the field name
//                            model: $(this).attr('name').replace('_no', '')
//                        };
//                    },
//                    processResults: function (data) {
//                        return { results: data.results };
//                    },
//                    cache: true
//                },
//                minimumInputLength: 1,
//                placeholder: 'Search...',
//                allowClear: true
//            });
//        },
//        error: function (error) {
//            console.error('Error fetching data:', error);
//            Swal.fire({
//                title: 'Error',
//                text: 'Failed to load item data.',
//                icon: 'error',
//                confirmButtonColor: '#e91e63' // Pink theme
//            });
//        }
//    });
//}
//
//$(document).ready(function () {
//    // 1. Correctly grab the CSRF token
//    var csrftoken = $('input[name=csrfmiddlewaretoken]').val();
//
//    // 2. Initialize DataTable
//    var table = $('#itemDetailsTable').DataTable({
//        processing: true,
//        serverSide: true,
//        ajax: {
//            url: '/items/item_details_datatable/',
//            type: 'POST',
//            headers: {
//                'X-CSRFToken': csrftoken, // Use the variable defined above
//            },
//        },
//        // 3. Add the ID to each row so we can find it for highlighting
//        createdRow: function(row, data, dataIndex) {
//            $(row).attr('data-id', data.id);
//        },
//        // 4. Re-apply highlight every time the table draws
//        drawCallback: function(settings) {
//            var highlightedId = sessionStorage.getItem('currentHighlightedRow');
//            if (highlightedId) {
//                applyVisualEffectAndStore(highlightedId);
//            }
//        },
//        columns: [
//            { data: 'model_no' },
//            { data: 'serial_no' },
//            { data: 'tag_no' },
//            { data: 'room_tag' },
//            { data: 'issued_to' },
//            { data: 'date_dispatched' },
//            { data: 'employee_name' },
//            { data: 'employee_designation' },
//            { data: 'lpo_no' },
//            { data: 'action' },
//        ],
//        pageLength: 10,
//        responsive: true,
//        bSort: false,
//        scrollX: true,
//        autoWidth: false
//    });
//
//    // Handle searching
//    $('#search').on('keyup', function () {
//        table.search(this.value).draw();
//    });
//
//    // Check highlight on initial page load
//    checkAndApplyHighlight();
//
//    // Form submission listener
//    $('body').on('submit', '#editItemDetailsForm', handleFormSubmission);
//});
//
//// Handle Datepicker specifically when modal is fully visible
//$(document).on('shown.bs.modal', '#editItemDetailsModal', function () {
//    $(".datepicker").daterangepicker({
//        singleDatePicker: true,
//        opens: 'left',
//        showDropdowns: true,
//        autoUpdateInput: true,
//        minYear: 2022,
//        locale: {
//            format: 'YYYY-MM-DD',
//            cancelLabel: 'Clear'
//        }
//    });
//});

var pageIdentifier = 'edit_item_details';
var currentPageUrl = window.location.href;

// 1. Updated Submission Handler
function handleFormSubmission(event) {
    event.preventDefault();
    event.stopPropagation(); // Stop event bubbling

    var $form = $(event.target);
    var currentRowId = $form.find('input[name="detail_id"]').val();

    Swal.fire({
        title: 'Confirm Changes',
        text: 'Are you sure you want to save changes?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#e91e63',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, save it!'
    }).then((result) => {
        if (result.isConfirmed) {
            submitForm($form, currentRowId);
        }
    });
}

// 2. Updated Submit Function (Handles redirection & triggers highlight via Draw)
function submitForm($form, currentRowId) {
    var formData = new FormData($form[0]);
    formData.append("is_ajax", "true"); // Explicit flag for your Django View

    var saveUrl = $form.attr('action');

    $.ajax({
        type: 'POST',
        url: saveUrl,
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            // STEP A: Store the ID in storage FIRST
            sessionStorage.setItem('currentHighlightedRow', currentRowId);

            // STEP B: Close Modal
            $form.closest('.modal').modal('hide');

            Swal.fire({
                title: 'Saved!',
                text: response.message, // Uses message from your JsonResponse
                icon: 'success',
                confirmButtonColor: '#e91e63'
            }).then(() => {
                // STEP C: Reload table. drawCallback will handle the highlight automatically
                if ($.fn.DataTable.isDataTable('#itemDetailsTable')) {
                    $('#itemDetailsTable').DataTable().ajax.reload(null, false);
                }
            });
        },
        error: function (xhr) {
            Swal.fire('Error', 'Failed to save changes. Ensure all fields are valid.', 'error');
        }
    });
}

// 3. Highlight Effect Logic (Simplified to just apply visuals)
function applyVisualEffectAndStore(currentRowId) {
    var $row = $('#itemDetailsTable').find(`tr[data-id="${currentRowId}"]`);

    if ($row.length > 0) {
        $row.addClass('table-info highlight-fade'); // Custom class for animation

        // Remove highlight after 5 seconds and clear storage
        setTimeout(function () {
            $row.removeClass('table-info highlight-fade');
            sessionStorage.removeItem('currentHighlightedRow');
        }, 5000);
    }
}

// 4. Modal Open Logic
function openModal(detailId) {
    var modalSelector = '#editItemDetailsModal';
    $(modalSelector + 'Label').text('Edit Item Details - ' + detailId);

    $.ajax({
        url: '/items/edit_item_details_modal/',
        type: 'GET',
        data: { detail_id: detailId },
        success: function (response) {
            $(modalSelector + ' .modal-body').html(response);
            $(modalSelector).modal('show');

            $('.select2').select2({
                dropdownParent: $(modalSelector),
                ajax: {
                    url: '/items/search_dropdown_options/',
                    dataType: 'json',
                    delay: 250,
                    data: function (params) {
                        return {
                            q: params.term || '',
                            model: $(this).attr('name').replace('_no', '')
                        };
                    },
                    processResults: function (data) {
                        return { results: data.results };
                    }
                },
                minimumInputLength: 1,
                placeholder: 'Search...',
                allowClear: true
            });
        },
        error: function (error) {
            Swal.fire('Error', 'Failed to load item data.', 'error');
        }
    });
}

// 5. Document Ready & Global Listeners
$(document).ready(function () {
    var csrftoken = $('input[name=csrfmiddlewaretoken]').val();

    var table = $('#itemDetailsTable').DataTable({
        processing: true,
        serverSide: true,
        ajax: {
            url: '/items/item_details_datatable/',
            type: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
        },
        createdRow: function(row, data, dataIndex) {
            $(row).attr('data-id', data.id); // Injects ID for highlighting
        },
        drawCallback: function(settings) {
            // This runs every time the table is drawn (search, page, reload)
            var highlightedId = sessionStorage.getItem('currentHighlightedRow');
            if (highlightedId) {
                applyVisualEffectAndStore(highlightedId);
            }
        },
        columns: [
            { data: 'model_no' },
            { data: 'serial_no' },
            { data: 'tag_no' },
            { data: 'room_tag' },
            { data: 'issued_to' },
            { data: 'date_dispatched' },
            { data: 'employee_name' },
            { data: 'employee_designation' },
            { data: 'lpo_no' },
            { data: 'action' },
        ],
        pageLength: 10,
        responsive: true,
        bSort: false,
        scrollX: true
    });

    $('#search').on('keyup', function () {
        table.search(this.value).draw();
    });

    // Use .off().on() to prevent multiple event bindings
    $('body').off('submit', '#editItemDetailsForm').on('submit', '#editItemDetailsForm', handleFormSubmission);
});

// Datepicker Initialization
$(document).on('shown.bs.modal', '#editItemDetailsModal', function () {
    $(".datepicker").daterangepicker({
        singleDatePicker: true,
        showDropdowns: true,
        autoUpdateInput: true,
        locale: { format: 'YYYY-MM-DD' }
    });
});

//Edit item details page server side processing------------------------------------------------------------------------

// Sent items views using lazy loading
$(document).ready(function () {
    var csrf = $('input[name=csrfmiddlewaretoken]').val();
    var table = $('#LazyLoading').DataTable({
        processing: true,
        serverSide: true,
        ajax: {
            url: '/sent_items/sent_items_ajax/',  // this is the same view you use now
            type: 'POST',
            headers: {
                    'X-CSRFToken':csrftoken,
            },
        },
        columns: [
            { data: 'no' },
            { data: 'send_date' },
            { data: 'send_to' },
            { data: 'product_description' },
            { data: 'model_no' },
            { data: 'serial_no' },
            { data: 'received_by' },
            { data: 'action'},
        ],
        lengthChange: false,
        bSort: false,

        scrollX: true,
        autoWidth: false,

    });

    // Attach the search box
    $('#search').on('keyup', function () {
        table.search(this.value).draw();
    });

});




