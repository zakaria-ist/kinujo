var shipping_form = `<section class="panel">
                        <header class="panel-heading pb-5" style="font-size: 25px">
                            <strong>Shipping Information</strong>
                        </header>
                        <div class="col-lg-12">
                            <div class="form-group row">
                                <label for="destination_name" class="col-lg-2 control-label">Destination Name<span
                                        class="span-required">(*)</span></label>
                                <div class="col-lg-6">
                                    <input class="form-control trs-field" type="text"
                                        name="destination_name"
                                        id="destination_name">
                                </div>
                            </div>
                            <div class="form-group row">
                                <label for="full_name" class="col-lg-2 control-label">Full Name<span
                                        class="span-required">(*)</span></label>
                                <div class="col-lg-6">
                                    <input class="form-control trs-field" type="text"
                                        name="full_name"
                                        id="full_name">
                                </div>
                            </div>
                            <div class="form-group row">
                                <label for="zip_code" class="col-lg-2 control-label">Zip Code<span
                                        class="span-required">(*)</span></label>
                                <div class="col-lg-6">
                                    <input class="form-control trs-field" type="text"
                                        name="zip_code"
                                        id="zip_code"
                                        maxlength="8"
                                        placeholder="">
                                </div>
                            </div>
                            <div class="form-group row">
                                <label for="prefecture" class="col-lg-2 control-label">Prefecture<span
                                        class="span-required">(*)</span></label>
                                <div class="col-lg-6">
                                    <select name="prefecture" id="prefecture" class="form-control trs-field">
                                    </select>
                                </div>
                            </div>
                            <div class="form-group row">
                                <label for="address1" class="col-lg-2 control-label">Address One<span
                                        class="span-required">(*)</span></label>
                                <div class="col-lg-6">
                                    <input class="form-control trs-field" type="text"
                                        name="address1"
                                        id="address1"
                                        placeholder="">
                                </div>
                            </div>
                            <div class="form-group row">
                                <label for="address2" class="col-lg-2 control-label">Address Two<span
                                        class="span-required">(*)</span></label>
                                <div class="col-lg-6">
                                    <input class="form-control trs-field" type="text"
                                        name="address2"
                                        id="address2"
                                        placeholder="">
                                </div>
                            </div>
                            <div class="form-group row">
                                <label for="add_tel" class="col-lg-2 control-label">Phone Number<span
                                        class="span-required">(*)</span></label>
                                <div class="col-lg-6">
                                    <input class="form-control trs-field" type="text"
                                        name="add_tel"
                                        id="add_tel"
                                        placeholder="">
                                </div>
                            </div>
                            <div class="form-group form-check offset-lg-2 col-lg-6 pl-4" style="margin-top: 30px;">
                                <input type="checkbox" class="form-check-input checkbox-2x" name="default_checkbox" id="default_checkbox" checked>
                                <label class="form-check-label" for="active">Is Default</label>
                            </div>
                            <div class="form-group row">
                                <div class="text-center">
                                    <button type="button" onclick="saveShippingInfo()" name="btnAddressSave" id="btnAddressSave" class="btn btn-primary blue-btn">Save</button>
                                    <a class="btn btn-default gray-btn" onclick="cancelShippingForm()">Cancel</a>
                                </div>
                            </div>
                        </div>
                    </section>`;

var shipping_table = `<header class="panel-heading" style="font-size: 25px">
                    <strong>Shipping Information</strong>
                    </header>
                    <div class="table-section white-bg">
                    <div class="text-right pb-3">
                        <span class="">
                            <a type="button" class="btn btn-primary blue-btn" onclick="showShippingForm()"> 
                                <span>Add</span>
                            </a>
                        </span>
                    </div>
                    <div class="adv-table table-responsive">
                        <table class="display table table-bordered table-striped table-condensed"
                            id="shipping-table" style="width:100%">
                            <thead>
                            <tr>
                                <th>#</th>
                                <th>Address Name</th>
                                <th>Full Name</th>
                                <th>Address</th>
                                <th>Phone Number</th>
                                <th class="text-center" style="min-width:90px!important;">Options</th>
                            </tr>
                            </thead>
                        </table>
                    </div>
                    </div>`;

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
    $('#shipping_info_tab').html(shipping_form);
    var options = '';
    $.each(prefecture_list, function(i, v) {
        options += "<option value='"+v[0]+"'>"+v[1]+"</option>";
    });
    $('#prefecture').html(options);
    if (!$('#prefecture').data('select2')) {
        //$('#prefecture').select2('destroy');
        $('#prefecture').select2({});
    }
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
    // var is_valid = validate_shipping_form();
    var is_valid = true;
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

                $('#shipping_info_tab').html('');
                $('#shipping_info_tab').html(shipping_table);
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

function cancelShippingForm() {
    $('#shipping_info_tab').html('');
    $('#shipping_info_tab').html(shipping_table);
    loadShippingTableData();
}