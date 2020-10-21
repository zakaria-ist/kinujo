function loadClientTableData(filter_str='[]') {
    $('#client-table').DataTable().destroy();
    $('#client-table').DataTable({
        "order": [[2, "asc"]],
        "serverSide": true,
        "scrollX": true,
        stateSave: true,
        "ajax": {
            "url": "/profiles/client_list_json/",
            "data": {
                "profile_id": profile_id,
                "filter_str": filter_str
            }
        },
        "columns": [
            {"data": "no", "orderable": false},
            {"data": "type", "orderable": false},
            {"data": "nickname"},
            {"data": "created", "orderable": false},
            
            {
                "sClass": "text-center",
                "orderable": false,
                "data": null,
                "render": function (data, type, row, meta) {
                    var btn =
                            '<div class="btn-group">' +
                            '<a class="btn-group-item" href="/profiles/profile_edit/' + row.id + '/' + '"><i class="fas fa-pencil-alt fa-2x text-info"></i></a>' +
                            '</div>';
                    return btn;
                }
            }
        ],
        "drawCallback": function(settings) {
            update_total_customer(settings.json.recordsFiltered); 
         },
    });
}

function update_total_customer(recordsFiltered) {
    $('#recordsFiltered').text(recordsFiltered);
}

var filter_list = [];
    $('input[type="checkbox"]').click(function(){
        filter_list.length = 0;
        if($('#store_client_check').prop("checked") == true){
            filter_list.push(4); // 4 is store authority id 
        }
        if($('#general_client_check').prop("checked") == true){
            filter_list.push(5); // 5 is general authority id 
        }

        filter_str = JSON.stringify(filter_list);

        loadClientTableData(filter_str);
    });