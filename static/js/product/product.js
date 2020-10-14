  
  //starts adding more image button
  let counter = 0;
  const imgWrapper = document.getElementById('img-wrapper');

  const loadFile = function(event) {
     
    const addImgBtn = document.getElementById(`add-img-btn-${counter}`);
    const image = document.getElementById(`images-${counter}`);

    if(imgWrapper.childElementCount < 6){ 
      image.innerHTML = `<img class="images" src="${URL.createObjectURL(event.target.files[0])}" width="120" /> 
                  <div class="overlay">
                    <div onClick="this.parentNode.parentNode.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode.parentNode.parentNode)" class="rmv-img-btn"><i class="fas fa-trash-alt" style="margin-top: 22%;margin-left: 10%; color: #9f111f;"></i> </div>
                  </div>
      `;
      addImgBtn.style.display = 'none';
      
      //increase counter for next
      counter ++;
      
      imgWrapper.innerHTML += `<div class="col-md-4"><div class="row img-h"><label for="file" id="add-img-btn-${counter}" class="btn btn-secondary text-center col-md-12 img-input" onclick="document.getElementById('file-${counter}').click()">
                  + 
                  <input type="file"  accept="image/*" name="image" id="file-${counter}"  onchange="loadFile(event)" style="display: none">
                </label>
                <div class="col-md-12 img-container" id="images-${counter}"> </div> </div></div>` 
    } else{
      document.getElementById(`file-${counter}`).value='';
      console.log(document.getElementById(`file-${counter}`).value);
      document.getElementById('max-img-btn').click();
    }

    
  };


  
  


  

    //ends image add button increase code


    //starts variant code
    const one = document.getElementById('one');
    const two = document.getElementById('two');
    const none = document.getElementById('none');

    const varietyContent = document.getElementById('variety-content');

    one.addEventListener('click', (event)=> {
      // event.preventDefault();
      varietyContent.innerHTML = `<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#oneItemVariant">+ Item / Option</button>`;
    })

    two.addEventListener('click', (event)=> {
      // event.preventDefault();
      varietyContent.innerHTML = `<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#twoItemsVariant">+ Items / Options</button>`;
    })

    none.addEventListener('click', (event)=> {
      // event.preventDefault();
      varietyContent.innerHTML = ``;
    })


    //modal for i item variant
    $('#oneItemsVariant').on('show.bs.modal', function (event) {
  // var button = $(event.relatedTarget) // Button that triggered the modal
  // var recipient = button.data('whatever') // Extract info from data-* attributes
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  // var modal = $(this)
  // modal.find('.modal-title').text(recipient)
  // modal.find('.modal-body input').val(recipient)
  })
  //modal for 2 items variable
    $('#twoItemsVariant').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var recipient = button.data('whatever') // Extract info from data-* attributes
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  // var modal = $(this)
  // modal.find('.modal-title').text(recipient)
  // modal.find('.modal-body input').val(recipient)
  })

  //one item variant code for adding more option
  let optCounter = 3
  document.getElementById('addToOneItemVariant').addEventListener('click', ()=>{
    document.getElementById('oneItemGroup').innerHTML += `<div class="form-group">
                  <p class="m-2" style="width: 20px;">${optCounter}</p>
                  <input type="text" class="form-control" id="message-text" placeholder="" style="width: 200px;">
                  
                  <input type="text" class="form-control" id="message-text" placeholder="" style="width: 100px;">
                  
                  <input type="text" class="form-control" id="message-text" placeholder="" style="width: 50px;">
                  <p class="m-2" style="width: 10px; cursor: pointer;"  onClick="this.parentNode.parentNode.removeChild(this.parentNode)"><i class="fas fa-trash-alt" style="color: #9f111f;"></i> </p>
                </div>`;
    optCounter++;
  })

    //ends variant code


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