
function loadSalonTableData() {
    $('#salon-table').DataTable().destroy();
    $('#salon-table').DataTable({
        "order": [[2, "asc"]],
        "serverSide": true,
        "scrollX": true,
        stateSave: true,
        "ajax": {
            "url": "/salons/salon_list_json/",
            "data": {
                "user_id": profile_id
            }
        },
        "columns": [
            {"data": "no", "orderable": false},
            {"data": "name"},
            {"data": "pic_name"},
            {"data": "address", "orderable": false},
            {"data": "pic_tel"},
            
            {
                "sClass": "text-center",
                "orderable": false,
                "data": null,
                "render": function (data, type, row, meta) {
                    var btn =
                            '<div class="btn-group">' +
                            '<a class="btn-group-item pointer" onclick="showSalonForm('+ row.id +')"><i class="fas fa-pencil-alt fa-2x text-info"></i></a>' + 
                            '<a class="btn-group-item pointer" onclick="deleteSalon(' + row.id + ')"><i class="fas fa-trash-alt fa-2x text-danger"></i></a>' + 
                            '</div>';
                    return btn;
                }
            }
        ]
    });

    setTimeout(() => {
        $('#salon-table').DataTable().columns.adjust();
    }, 300);
}

function deleteSalon(id) {
    $("#comfirmDeleteAllModal").modal("show");
    $("#modal_btn_delete").attr("onclick", "deleteSalonConfirm("+ id +")");
}

function deleteSalonConfirm(id) {
    $.ajax({
        method: "POST",
        url: '/salons/delete_salon_info/',
        dataType: 'JSON',
        data: {
            'salon_id': id,
        },
        success: function (json) {
            g_salon_id = '';
            $.confirm({
                title: get_translate('Delete Successful'),
                content: get_translate('Salon information is deleted.'),
                buttons: {
                    Ok: {
                        btnClass: 'btn-success',
                        action: function(){}
                        }
                    }
            });
            loadSalonTableData();
        },
        error: function (e) {
            $.confirm({
                title: get_translate('Error'),
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


var g_salon_id = '';
function showSalonForm(salon_id='') {
    $('#salon_info_tab').html('');
    $.get("/profiles/templates/salon_form/", function(data){
        $('#salon_info_tab').html(data);
        var options = '';
        $.each(prefecture_list, function(i, v) {
            options += "<option value='"+v[0]+"'>"+v[1]+"</option>";
        });
        $('#salon_prefecture').html(options);
        if (!$('#salon_prefecture').data('select2')) {
            $('#salon_prefecture').select2({});
        }
        $('#salon_prefecture').on("select2:open", function( event ){
            prefill_select2(event);
        });
    
        if (salon_id != '') {
            g_salon_id = salon_id;
            $.ajax({
                method: "POST",
                url: '/salons/get_salon_info/',
                dataType: 'JSON',
                data: {
                    'salon_id': salon_id,
                },
                success: function (json) {
                    $('#salon_name').val(json.name);
                    $('#pic_name').val(json.pic_name);
                    $('#salon_zip_code').val(json.zip1);
                    $('#salon_prefecture').val(json.prefecture).trigger('change');
                    $('#salon_address1').val(json.address1);
                    $('#salon_address2').val(json.address2);
                    $('#pic_tel').val(json.pic_tel);
                }
            });
        }
    });
}


function saveSalonInfo() {
    // var is_valid = validate_salon_form();
    var is_valid = true;
    if (is_valid) {
        $.ajax({
            method: "POST",
            url: '/salons/update_salon_info/',
            dataType: 'JSON',
            data: {
                'profile_id': profile_id,
                'salon_id': g_salon_id,
                'name': $('#salon_name').val(),
                'pic_name': $('#pic_name').val(),
                'zip_code': $('#salon_zip_code').val(),
                'address1': $('#salon_address1').val(),
                'address2': $('#salon_address2').val(),
                'pic_tel': $('#pic_tel').val(),
                'prefecture': $('#salon_prefecture').val(),
            },
            success: function (json) {
                $.confirm({
                    title: get_translate('Update Successful'),
                    content: get_translate('Salon information is updated.'),
                    buttons: {
                        Ok: {
                            btnClass: 'btn-success',
                            action: function(){}
                            }
                        }
                });

                cancelSalonForm();
            },
            error: function (e) {
                $.confirm({
                    title: get_translate('Error'),
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
            title: get_translate('Warning'),
            content: get_translate('Please fill in the required fields'),
            buttons: {
                Ok: {
                    btnClass: 'btn-success',
                    action: function(){}
                    }
                }
        });
    }
}

function cancelSalonForm() {
    $('#salon_info_tab').html('');
    $.get("/profiles/templates/salon_table/", function(data){
        $('#salon_info_tab').html(data);
        loadSalonTableData();
    });
    
}