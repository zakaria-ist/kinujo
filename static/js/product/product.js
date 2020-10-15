  
  
    function loadProductTableData() {
        $('#product-table').DataTable().destroy();
        $('#product-table').DataTable({
            "order": [[2, "asc"]],
            "serverSide": true,
            "scrollX": true,
            stateSave: true,
            "ajax": {
                "url": "/products/product_list_json/",
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
                                '<a class="btn-group-item pointer" onclick="showProductForm('+ row.id +')"><i class="fas fa-pencil-alt fa-2x text-info"></i></a>' + 
                                '<a class="btn-group-item pointer" onclick="deleteProduct(' + row.id + ')"><i class="fas fa-trash-alt fa-2x text-danger"></i></a>' + 
                                '</div>';
                        return btn;
                    }
                }
            ]
        });
    
        setTimeout(() => {
            $('#product-table').DataTable().columns.adjust();
        }, 300);
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
                    content: 'product information is deleted.',
                    buttons: {
                        Ok: {
                            btnClass: 'btn-success',
                            action: function(){}
                            }
                        }
                });
                // loadProductTableData();
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
            var options = '';
            $.each(category_list, function(i, v) {
                options += "<option value='"+v[0]+"'>"+v[1]+"</option>";
            });
            $('#category').html(options);
            if (!$('#category').data('select2')) {
                $('#category').select2({});
            }
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
    
    
    function saveproductInfo() {
        // var is_valid = validate_product_form();
        var is_valid = true;
        if (is_valid) {
            $.ajax({
                method: "POST",
                url: '/products/add_update_product/',
                dataType: 'JSON',
                data: {
                    'product_id': g_product_id,
                },
                success: function (json) {
                    $.confirm({
                        title: 'Update Successfull',
                        content: 'product information is updated.',
                        buttons: {
                            Ok: {
                                btnClass: 'btn-success',
                                action: function(){}
                                }
                            }
                    });
    
                    cancelproductForm();
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
                title: 'Error',
                content: 'Enter mandatory fileds',
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
        $('#item_tab').html('');
        $.get("/profiles/templates/product_list_page/", function(data){
            $('#item_tab').html(data);
            // loadProductTableData();
        });
        
    }