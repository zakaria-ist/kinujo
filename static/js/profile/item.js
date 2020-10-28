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
                "profile_id": profile_id,
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
                    return '<img src="'+row.image_path+'"  width="50px" height="50px">';
                }
            },
            {"data": "name"},
            {"data": "jan_code", "orderable": false},
            {
                "orderable": false,
                "render": function(data, type, row){
                    return row.varieties.split(",").join("<br/>");
                }
            },
            {"data": "stock", "orderable": false},
            {"data": "opened_date", "orderable": false},
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
    $("#comfirmDeleteProductModal").modal("show");
    $("#product_btn_delete").attr("onclick", "deleteProductConfirm("+ id +")");
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

function setEditFormInputs(json) {
    $('#name').val(json.name);
    $('#brand_name').val(json.brand_name);
    $('#description').val(json.description);
    $('#pr').val(json.pr);
    $('#url_str').val(json.url_str);
    $('#store_price').val(json.store_price);
    $('#price').val(json.price);
    $('#shipping_fee').val(json.shipping_fee);
    $('#category').val(json.category).trigger('change');
    $('#opened_date').val(json.opened_date).trigger('change');
    $("input[name=target]").val([json.target]);
    $("input[name=status]").val([json.is_opened]);
    $("input[name=is_used]").val([json.is_used]);
    $("input[name=variety]").val([json.variety]).trigger('change');
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
                setEditFormInputs(json);
            }
        });
    }
}


function saveProductInfo() {

    let varieties = [];
    let variety = $('input[name="variety"]:checked').val();
    if (variety == '0') { //None
        varieties.push({
            "jan_code": $('#jan_code').val(),
            "stock": $('#stock').val(),
            "varieties": []
            })
    }
    else if (variety == '1') { // 1 Item
      let name = document.getElementById('cell-name').innerHTML;
      let variantTableTitle = document.getElementsByClassName('variant-title');
      let variantTableCol = document.getElementsByClassName('variant-info');
      // crate varieties
      for(let i = 0; i < variantTableCol.length; i++) {
          try{
            varieties.push({
            "jan_code": document.getElementById('jan-id-'+i).innerHTML,
            "stock": document.getElementById('stock-id-'+i).innerHTML,
            "varieties": [
                {
                    "name": name,
                    "selection": variantTableTitle[i+1].innerHTML,
                    "vertical_and_horizontal": "1"
                }
            ]
            })
        } catch(e){

        }
      }
    }
    else if (variety == '2') { // 2 Items
        let preservedData = [];
        let variantTableCol = document.getElementsByClassName('variant-info');

        for(let i = 0; i < variantTableCol.length; i++){
                //get id num
            let idNum = variantTableCol[i].firstChild.id.split('-')[3];

            //get jancode
            let janId = `jan-id-${idNum}`;
            let jancode = document.getElementById(janId).innerHTML;

            //get stock
            let stockId = `stock-id-${idNum}`;
            let stock = document.getElementById(stockId).innerHTML;

            let dataToken = variantTableCol[i].firstChild.innerHTML.split('/').map((item) => item.trim()).join('_');
            
            preservedData.push({
                jancode: jancode,
                stock: stock,
                token: dataToken
            })
        }
        
        //second cell name
        let twoItemCellName = document.getElementById('cell-name');
        // crate varieties
        for(let i = 0; i < preservedData.length; i++){
            varieties.push({
                "jan_code": preservedData[i].jancode,
                "stock": preservedData[i].stock,
                "varieties": [
                    {
                        "name": twoItemCellName.innerHTML.split('/')[0].trim(),
                        "selection": preservedData[i].token.split('_')[0].trim(),
                        "vertical_and_horizontal": "0"
                    },
                    {
                        "name": twoItemCellName.innerHTML.split('/')[1].trim(),
                        "selection": preservedData[i].token.split('_')[1].trim(),
                        "vertical_and_horizontal": "1"
                    },
                ]
            })
        }
        
    }

    var data = new FormData();
    data.append("profile_id", profile_id);
    data.append("product_id", g_product_id);
    data.append("name", $('#name').val());
    data.append("brand_name", $('#brand_name').val());
    data.append("description", $('#description').val());
    data.append("pr", $('#pr').val());
    data.append("url_str", $('#url_str').val());
    data.append("category", $('#category').val());
    data.append("target", $('input[name="target"]:checked').val());
    data.append("price", $('#price').val());
    data.append("store_price", $('#store_price').val());
    data.append("shipping_fee", $('#shipping_fee').val());
    data.append("opened_date", $('#opened_date').val());
    data.append("is_opened", $('input[name="status"]:checked').val());
    data.append("is_used", $('input[name="is_used"]:checked').val());
    data.append("is_draft", '0');
    data.append("variety", variety);
    data.append("varieties", JSON.stringify(varieties));

    // Need to done
    // for(let j = 0; j < 5; j++){

    //     $(".images")[j].files[0], function(i, file) {
    //         data.append("product_image", file);
    //     };
    // }


    let imageLength = document.getElementsByClassName('images').length;
    //let fileInputs = document.querySelectorAll('input[type=file]');
    for(let i = 0; i < imageLength; i++){
        let fileId = `file-${i}`;  
        data.append("product_image", document.getElementById(fileId).files[0]);

    }

    
        
    


    
    var is_valid = true;
    if (is_valid) {
        $.ajax({
            method: "POST",
            url: '/products/add_update_product/',
            data: data,
            processData: false,
            contentType: false,
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