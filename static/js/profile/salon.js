
var salon_form = `<section class="panel">
                    <header class="panel-heading pb-5" style="font-size: 25px">
                        <strong>Salon Information</strong>
                    </header>
                    <div class="col-lg-12">
                        <div class="form-group row">
                            <label for="salon_name" class="col-lg-2 control-label">Salon Name<span
                                    class="span-required">(*)</span></label>
                            <div class="col-lg-6">
                                <input class="form-control trs-field" type="text"
                                    name="salon_name"
                                    id="salon_name">
                            </div>
                        </div>
                        <div class="form-group row">
                            <label for="pic_name" class="col-lg-2 control-label">Representative Name<span
                                    class="span-required">(*)</span></label>
                            <div class="col-lg-6">
                                <input class="form-control trs-field" type="text"
                                    name="pic_name"
                                    id="pic_name">
                            </div>
                        </div>
                        <div class="form-group row">
                            <label for="salon_zip_code" class="col-lg-2 control-label">Zip Code<span
                                    class="span-required">(*)</span></label>
                            <div class="col-lg-6">
                                <input class="form-control trs-field" type="text"
                                    name="salon_zip_code"
                                    id="salon_zip_code"
                                    maxlength="8"
                                    placeholder="">
                            </div>
                        </div>
                        <div class="form-group row">
                            <label for="salon_prefecture" class="col-lg-2 control-label">Prefecture<span
                                    class="span-required">(*)</span></label>
                            <div class="col-lg-6">
                                <select name="salon_prefecture" id="salon_prefecture" class="form-control trs-field">
                                </select>
                            </div>
                        </div>
                        <div class="form-group row">
                            <label for="salon_address1" class="col-lg-2 control-label">Address One<span
                                    class="span-required">(*)</span></label>
                            <div class="col-lg-6">
                                <input class="form-control trs-field" type="text"
                                    name="salon_address1"
                                    id="salon_address1"
                                    placeholder="">
                            </div>
                        </div>
                        <div class="form-group row">
                            <label for="salon_address2" class="col-lg-2 control-label">Address Two<span
                                    class="span-required">(*)</span></label>
                            <div class="col-lg-6">
                                <input class="form-control trs-field" type="text"
                                    name="salon_address2"
                                    id="salon_address2"
                                    placeholder="">
                            </div>
                        </div>
                        <div class="form-group row">
                            <label for="pic_tel" class="col-lg-2 control-label">Phone Number<span
                                    class="span-required">(*)</span></label>
                            <div class="col-lg-6">
                                <input class="form-control trs-field" type="text"
                                    name="pic_tel"
                                    id="pic_tel"
                                    placeholder="">
                            </div>
                        </div>
                        <div class="form-group row">
                            <div class="text-center">
                                <button type="button" onclick="saveSalonInfo()" name="btnSalonSave" id="btnSalonSave" class="btn btn-primary blue-btn">Save</button>
                                <a class="btn btn-default gray-btn" onclick="cancelSalonForm()">Cancel</a>
                            </div>
                        </div>
                    </div>
                    </section>`;

var salon_table = `<header class="panel-heading" style="font-size: 25px">
                    <strong>Salon Information</strong>
                    </header>
                    <div class="table-section white-bg">
                    <div class="text-right pb-3">
                        <span class="">
                            <a type="button" class="btn btn-primary blue-btn" onclick="showSalonForm()"> 
                                <span>Add</span>
                            </a>
                        </span>
                    </div>
                    <div class="adv-table table-responsive">
                        <table class="display table table-bordered table-striped table-condensed"
                            id="salon-table" style="width:100%">
                            <thead>
                            <tr>
                                <th>#</th>
                                <th>Salon Name</th>
                                <th>Representative's Name</th>
                                <th>Address</th>
                                <th>Phone Number</th>
                                <th class="text-center" style="min-width:90px!important;">Options</th>
                            </tr>
                            </thead>
                        </table>
                    </div>
                    </div>`;

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
                title: 'Delete Successfull',
                content: 'Salon information is deleted.',
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


var g_salon_id = '';
function showSalonForm(salon_id='') {
    $('#salon_info_tab').html('');
    $('#salon_info_tab').html(salon_form);
    // $.get("../../templates/salon_form.html", function(data){
    //     $('#salon_info_tab').html(data);
    // });
    var options = '';
    $.each(prefecture_list, function(i, v) {
        options += "<option value='"+v[0]+"'>"+v[1]+"</option>";
    });
    $('#salon_prefecture').html(options);
    if (!$('#salon_prefecture').data('select2')) {
        //$('#prefecture').select2('destroy');
        $('#salon_prefecture').select2({});
    }
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
                    title: 'Update Successfull',
                    content: 'Salon information is updated.',
                    buttons: {
                        Ok: {
                            btnClass: 'btn-success',
                            action: function(){}
                            }
                        }
                });

                $('#salon_info_tab').html('');
                $('#salon_info_tab').html(salon_table);
                loadSalonTableData();
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

function cancelSalonForm() {
    $('#salon_info_tab').html('');
    $('#salon_info_tab').html(salon_table);
    loadSalonTableData();
}