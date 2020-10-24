
function loadShippingTableData() {
    $('#shipping-table').DataTable().destroy();
    $('#shipping-table').DataTable({
        "order": [[2, "asc"]],
        "serverSide": true,
        "scrollX": true,
        stateSave: true,
        "ajax": {
            "url": "/profiles/shipping_list_json/",
            "data": {
                "user_id": profile_id
            }
        },
        "columns": [
            {"data": "no", "orderable": false},
            {"data": "address_name"},
            {"data": "name"},
            {"data": "address", "orderable": false},
            {"data": "tel"},
            
            {
                "sClass": "text-center",
                "orderable": false,
                "data": null,
                "render": function (data, type, row, meta) {
                    var btn =
                            '<div class="btn-group">' +
                            '<a class="btn-group-item pointer" onclick="showShippingForm('+ row.id +')"><i class="fas fa-pencil-alt fa-2x text-info"></i></a>' + 
                            '<a class="btn-group-item pointer" onclick="deleteAddress(' + row.id + ')"><i class="fas fa-trash-alt fa-2x text-danger"></i></a>' + 
                            '</div>';
                    return btn;
                }
            }
        ]
    });

    setTimeout(() => {
        $('#shipping-table').DataTable().columns.adjust();
    }, 300);
}

function deleteAddress(id) {
    $("#comfirmDeleteAllModal").modal("show");
    $("#modal_btn_delete").attr("onclick", "deleteShipping("+ id +")");
}

function deleteShipping(id) {
    $.ajax({
        method: "POST",
        url: '/profiles/delete_shipping_info/',
        dataType: 'JSON',
        data: {
            'shipping_id': id,
        },
        success: function (json) {
            g_shipping_id = '';
            $.confirm({
                title: 'Delete Successfull',
                content: 'Shipping information is deleted.',
                buttons: {
                    Ok: {
                        btnClass: 'btn-success',
                        action: function(){}
                        }
                    }
            });
            loadShippingTableData();
        },
        error: function (e) {
            $.confirm({
                title: 'Error',
                content: e.message,
                buttons: {
                    Ok: {
                        btnClass: 'btn-success',
                        action: function(){}
                        }
                    }
            });
        }
    });
}

var g_shipping_id = '';
function showShippingForm(shipping_id='') {
    $('#shipping_info_tab').html('');
    $.get("/profiles/templates/shipping_form/", function(data){
        $('#shipping_info_tab').html(data);
        // render prefecture
        var options = '';
        $.each(prefecture_list, function(i, v) {
            options += "<option value='"+v[0]+"'>"+v[1]+"</option>";
        });
        $('#prefecture').html(options);
        if (!$('#prefecture').data('select2')) {
            //$('#prefecture').select2('destroy');
            $('#prefecture').select2({});
        }
    });
    if (shipping_id != '') {
        g_shipping_id = shipping_id;
        $.ajax({
            method: "POST",
            url: '/profiles/get_shipping_info/',
            dataType: 'JSON',
            data: {
                'shipping_id': shipping_id,
            },
            success: function (json) {
                $('#destination_name').val(json.destination_name);
                $('#full_name').val(json.full_name);
                $('#zip_code').val(json.zip_code);
                $('#prefecture').val(json.prefecture).trigger('change');
                $('#address1').val(json.address1);
                $('#address2').val(json.address2);
                $('#add_tel').val(json.add_tel);
                if(json.is_default == '1') {
                    $('#default_checkbox').prop('checked', true);
                } else {
                    $('#default_checkbox').prop('checked', false);
                }
            }
        });
    }
}

function saveShippingInfo() {
    var is_valid = validate_shipping_form();
    if (is_valid) {
        is_default = 0;
        if($('#default_checkbox').prop("checked") == true) {
            is_default = 1;
        }
        $.ajax({
            method: "POST",
            url: '/profiles/update_shipping_info/',
            dataType: 'JSON',
            data: {
                'profile_id': profile_id,
                'shipping_id': g_shipping_id,
                'address_name': $('#destination_name').val(),
                'name': $('#full_name').val(),
                'zip_code': $('#zip_code').val(),
                'address1': $('#address1').val(),
                'address2': $('#address2').val(),
                'add_tel': $('#add_tel').val(),
                'prefecture': $('#prefecture').val(),
                'is_default': is_default
            },
            success: function (json) {
                $.confirm({
                    title: 'Update Successfull',
                    content: 'Shipping information is updated.',
                    buttons: {
                        Ok: {
                            btnClass: 'btn-success',
                            action: function(){}
                            }
                        }
                });

                cancelShippingForm();
            },
            error: function (e) {
                $.confirm({
                    title: 'Error',
                    content: e.message,
                    buttons: {
                        Ok: {
                            btnClass: 'btn-success',
                            action: function(){}
                            }
                        }
                });
            }
        });
    } else {
        $.confirm({
            title: 'Warning',
            content: 'Please fill in the required fields',
            buttons: {
                Ok: {
                    btnClass: 'btn-success',
                    action: function(){}
                    }
                }
        });
    }
}

function cancelShippingForm() {
    $('#shipping_info_tab').html('');
    $.get("/profiles/templates/shipping_table/", function(data){
        $('#shipping_info_tab').html(data);
        loadShippingTableData();
    });
}

function validate_shipping_form() {
    var is_valid = true;

    if ( $('#destination_name').val() != '' ) {
        $('#destination_name').removeClass('highlight-mandatory');
        is_valid = true;
     } else {
        $('#destination_name').addClass('highlight-mandatory');
         is_valid = false;
     }
    if ( $('#full_name').val() != '' ) {
        $('#full_name').removeClass('highlight-mandatory');
        is_valid = true;
     } else {
        $('#full_name').addClass('highlight-mandatory');
         is_valid = false;
     }
    if ( $('#zip_code').val() != '' ) {
        $('#zip_code').removeClass('highlight-mandatory');
        is_valid = true;
     } else {
        $('#zip_code').addClass('highlight-mandatory');
         is_valid = false;
     }
    if ( $('#prefecture').val() != '' ) {
        $('#prefecture').removeClass('highlight-mandatory');
        is_valid = true;
     } else {
        $('#prefecture').addClass('highlight-mandatory');
         is_valid = false;
     }
    if ( $('#address1').val() != '' ) {
        $('#address1').removeClass('highlight-mandatory');
        is_valid = true;
     } else {
        $('#address1').addClass('highlight-mandatory');
         is_valid = false;
     }
    if ( $('#add_tel').val() != '' ) {
        $('#add_tel').removeClass('highlight-mandatory');
        is_valid = true;
     } else {
        $('#add_tel').addClass('highlight-mandatory');
         is_valid = false;
     }

     return is_valid;
}