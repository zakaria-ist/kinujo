function loadItemTableData() {
    $('#item-table').DataTable().destroy();
    $('#item-table').DataTable({
        "order": [[2, "asc"]],
        "serverSide": true,
        "scrollX": true,
        stateSave: true,
        "ajax": {
            "url": "/products/product_list_json/",
            "data": {
                "filter_str": '[]'
            }
        },
        "columns": [
            {"data": "no", "orderable": false},
            {
                "sClass": "text-center",
                "orderable": false,
                "data": null,
                "render": function (data, type, row, meta) {
                    return '<img src="'+row.image_path+'">';
                }
            },
            {"data": "name"},
            {"data": "jan_code", "orderable": false},
            {"data": "stock", "orderable": false},
            {
                "sClass": "text-center",
                "orderable": false,
                "data": null,
                "render": function (data, type, row, meta) {
                    var btn =
                            '<div class="btn-group">' +
                            '<a class="btn-group-item pointer" onclick="showProductForm(' + row.id + ')"><i class="fas fa-pencil-alt fa-2x text-info"></i></a>' + 
                            '<a class="btn-group-item pointer" onclick="deleteProduct(' + row.id + ')"><i class="fas fa-trash-alt fa-2x text-danger"></i></a>' + 
                            '</div>';
                    return btn;
                }
            }
        ]
    });
}

function deleteProduct(id) {
    $("#comfirmDeleteAllModal").modal("show");
    $("#modal_btn_delete").attr("onclick", "deleteProductConfirm("+ id +")");
}

function deleteProductConfirm(id) {
    $.ajax({
        method: "POST",
        url: '/products/delete_product/',
        dataType: 'JSON',
        data: {
            'product_id': id,
        },
        success: function (json) {
            g_product_id = '';
            $.confirm({
                title: 'Delete Successfull',
                content: 'Product information is deleted.',
                buttons: {
                    Ok: {
                        btnClass: 'btn-success',
                        action: function(){}
                        }
                    }
            });
            loadItemTableData();
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

var g_product_id = '';
function showProductForm(product_id='') {
    $('#item_tab').html('');
    $.get("/profiles/templates/product_form/", function(data){
        $('#item_tab').html(data);
        // var options = '';
        // $.each(category_list, function(i, v) {
        //     options += "<option value='"+v[0]+"'>"+v[1]+"</option>";
        // });
        // $('#category').html(options);
        // if (!$('#category').data('select2')) {
        //     $('#category').select2({});
        // }
    });
    if (product_id != '') {
        g_product_id = product_id;
        $.ajax({
            method: "POST",
            url: '/products/get_product_info/',
            dataType: 'JSON',
            data: {
                'product_id': product_id,
            },
            success: function (json) {
                
            }
        });
    }
}


function saveProductInfo() {
    // var is_valid = validate_salon_form();
    var is_valid = true;
    if (is_valid) {
        $.ajax({
            method: "POST",
            url: '/products/add_update_product/',
            dataType: 'JSON',
            data: {
                'profile_id': profile_id,
                'product_id': g_product_id, // empty if new product
                
            },
            success: function (json) {
                $.confirm({
                    title: 'Update Successfull',
                    content: 'Product information is updated.',
                    buttons: {
                        Ok: {
                            btnClass: 'btn-success',
                            action: function(){}
                            }
                        }
                });

                cancelProductForm();
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

function cancelProductForm() {
    $('#salon_info_tab').html('');
    $.get("/profiles/templates/product_list_page/", function(data){
        $('#item_tab').html(data);
        loadItemTableData();
    });
    
}