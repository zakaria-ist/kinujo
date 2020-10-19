function loadClientTableData() {
    $('#client-table').DataTable().destroy();
    $('#client-table').DataTable({
        "order": [[2, "asc"]],
        "serverSide": true,
        "scrollX": true,
        stateSave: true,
        "ajax": {
            "url": "/profiles/profile_list_json/",
            "data": {
                "filter_str": '[]'
            }
        },
        "columns": [
            {"data": "no", "orderable": false},
            {"data": "type", "orderable": false},
            {"data": "nickname", "orderable": false},
            {"data": "store_total", "orderable": false},
            {"data": "user_total", "orderable": false},
            
            {
                "sClass": "text-center",
                "orderable": false,
                "data": null,
                "render": function (data, type, row, meta) {
                    var btn =
                            '<div class="btn-group">' +
                            '<a class="btn-group-item" href="/profiles/profile_edit/' + row.id + '/' + '"><i class="fas fa-pencil-alt fa-2x text-info"></i></a>' + 
                            '<a class="btn-group-item" onclick="deleteProfile(' + row.id + ')"><i class="fas fa-trash-alt fa-2x text-danger"></i></a>' + 
                            '</div>';
                    return btn;
                }
            }
        ]
    });
}