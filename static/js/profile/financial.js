
// Update user's financial info 
$('#btnPaymentSave').on('click', function() {
    var is_valid = validate_finance_form();
    if (is_valid) {
        $.ajax({
            method: "POST",
            url: '/profiles/update_financial_info/',
            dataType: 'JSON',
            data: {
                'profile_id': profile_id,
                'bank_name': $('#bank_name').val(),
                'bank_code': $('#bank_code').val(),
                'branch_name': $('#branch_name').val(),
                'branch_code': $('#branch_code').val(),
                'account_holder': $('#account_holder').val(),
                'account_number': $('#account_number').val(),
                'account_type': $('#account_type').val(),
            },
            success: function (json) {
                $.confirm({
                    title: 'Update Successfull',
                    content: 'Account information is updated.',
                    buttons: {
                        Ok: {
                            btnClass: 'btn-success',
                            action: function(){}
                            }
                        }
                });
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
})

function load_financial_info() {
    $.ajax({
        method: "POST",
        url: '/profiles/get_financial_info/',
        dataType: 'JSON',
        data: {
            'profile_id': profile_id,
        },
        success: function (json) {
            $('#bank_name').val(json.bank_name);
            $('#bank_code').val(json.bank_code);
            $('#branch_name').val(json.branch_name);
            $('#branch_code').val(json.branch_code);
            $('#account_holder').val(json.account_holder);
            $('#account_number').val(json.account_number);
            $('#account_type').val(json.account_type).trigger('change');
        }
    });
}

function validate_finance_form() {
    var is_valid = true;

    if ( $('#bank_name').val() != '' ) {
        $('#bank_name').removeClass('highlight-mandatory');
        is_valid = true;
     } else {
        $('#bank_name').addClass('highlight-mandatory');
         is_valid = false;
     }
    if ( $('#bank_code').val() != '' ) {
        $('#bank_code').removeClass('highlight-mandatory');
        is_valid = true;
     } else {
        $('#bank_code').addClass('highlight-mandatory');
         is_valid = false;
     }
    if ( $('#branch_code').val() != '' ) {
        $('#branch_code').removeClass('highlight-mandatory');
        is_valid = true;
     } else {
        $('#branch_code').addClass('highlight-mandatory');
         is_valid = false;
     }
    if ( $('#branch_name').val() != '' ) {
        $('#branch_name').removeClass('highlight-mandatory');
        is_valid = true;
     } else {
        $('#branch_name').addClass('highlight-mandatory');
         is_valid = false;
     }
    if ( $('#account_number').val() != '' ) {
        $('#account_number').removeClass('highlight-mandatory');
        is_valid = true;
     } else {
        $('#account_number').addClass('highlight-mandatory');
         is_valid = false;
     }
    if ( $('#account_holder').val() != '' ) {
        $('#account_holder').removeClass('highlight-mandatory');
        is_valid = true;
     } else {
        $('#account_holder').addClass('highlight-mandatory');
         is_valid = false;
     }
    if ( $('#account_type').val() != '' ) {
        $('#account_type').removeClass('highlight-mandatory');
        is_valid = true;
     } else {
        $('#account_type').addClass('highlight-mandatory');
         is_valid = false;
     }

     return is_valid;
}