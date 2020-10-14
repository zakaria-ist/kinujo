  
  //starts adding more image button
  let counter = 0;
  const imgWrapper = document.getElementById('img-wrapper');

  const loadFile = function(event) {
     
    const addImgBtn = document.getElementById(`add-img-btn-${counter}`);
    const image = document.getElementById(`images-${counter}`);

    if(imgWrapper.childElementCount < 6){ 
      image.innerHTML = `<img class="images" src="${URL.createObjectURL(event.target.files[0])}" width="120" /> 
                  <div class="overlay">
                    <div onClick="this.parentNode.parentNode.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode.parentNode.parentNode)" class="rmv-img-btn"><i class="fas fa-trash-alt" style="font-size: 2rem;margin-top: 20%;margin-left: 10%; color: #9f111f;"></i> </div>
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
      varietyContent.innerHTML = `<button type="button" class="btn btn-secondary" data-toggle="modal" data-target="#oneItemVariant">+ Item / Option</button>`;
    })

    two.addEventListener('click', (event)=> {
      // event.preventDefault();
      varietyContent.innerHTML = `<button type="button" class="btn btn-secondary" data-toggle="modal" data-target="#twoItemsVariant">+ Items / Options</button>`;
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
  function deleteOptions(){
    console.log('deleted');

    let optionArray = document.getElementsByClassName('one-variant-counter');

    for(let i = 0; i < optionArray.length; i++){
      optionArray[i].innerHTML = i + 1;
    }

  }
  
  document.getElementById('addToOneItemVariant').addEventListener('click', ()=>{
    let optionArray = document.getElementsByClassName('one-variant-counter');
    let optCounter = optionArray.length + 1;

    let newContent = document.createElement('div');
    newContent.innerHTML = `<div class='form-group'>
                  <p style="width: 20px;" class="m-2"> </p>
                  <p class="m-2 one-variant-counter" style="width: 20px;">${optCounter}</p>
                  <input type="text" class="form-control" id="message-text" placeholder="" style="width: 160px;">
                  
                  <input type="text" class="form-control" id="message-text" placeholder="" style="width: 100px;">
                  
                  <input type="number" class="form-control" id="message-text" placeholder="" style="width: 70px;">
                  <p class="m-2" style="width: 10px; cursor: pointer; font-size: 1rem;"  onClick="this.parentNode.parentNode.removeChild(this.parentNode); deleteOptions();"><i class="fas fa-trash-alt" style="color: #D08383;"></i> </p>
                  </div>`;
    
    while (newContent.firstChild) {
      document.getElementById('oneItemGroup').appendChild(newContent.firstChild);
    }

   
  })

  //two item variants

  //first of two items variant
  function deleteOptionsFirstOfTwo(){
    console.log('deleted');

    let firstOfTwooptionArray = document.getElementsByClassName('first-of-two-variant-counter');

    for(let i = 0; i < firstOfTwooptionArray.length; i++){
      firstOfTwooptionArray[i].innerHTML = i + 1;
    }

  }

  document.getElementById('addToFirstOfTwoItemVariant').addEventListener('click', ()=>{
    let firstOfTwooptionArray = document.getElementsByClassName('first-of-two-variant-counter');
    let firstOfTwoOptCounter = firstOfTwooptionArray.length + 1;

    let firstOfTwoNewContent = document.createElement('div');
    firstOfTwoNewContent.innerHTML = `<div class='form-group'>
                  <p style="width: 20px;" class="m-2"> </p>
                  <p class="m-2 first-of-two-variant-counter" style="width: 20px;">${firstOfTwoOptCounter}</p>
                  <input type="text" class="form-control" id="message-text" placeholder="" style="width: 280px;">
                  
                  <p class="m-2" style="width: 10px; cursor: pointer; font-size: 1.3rem;"  onClick="this.parentNode.parentNode.removeChild(this.parentNode); deleteOptionsFirstOfTwo();"><i class="fas fa-trash-alt" style="color: #D08383;"></i> </p>
                  </div>`;
    
    while (firstOfTwoNewContent.firstChild) {
      document.getElementById('firstOfTwoItemGroup').appendChild(firstOfTwoNewContent.firstChild);
    }

   
  })


  //last of two items variant
  function deleteOptionsLastOfTwo(){
    console.log('deleted');

    let lastOfTwooptionArray = document.getElementsByClassName('last-of-two-variant-counter');

    for(let i = 0; i < lastOfTwooptionArray.length; i++){
      lastOfTwooptionArray[i].innerHTML = i + 1;
    }

  }

  document.getElementById('addToLastOfTwoItemVariant').addEventListener('click', ()=>{
    let lastOfTwooptionArray = document.getElementsByClassName('last-of-two-variant-counter');
    let lastOfTwoOptCounter = lastOfTwooptionArray.length + 1;

    let lastOfTwoNewContent = document.createElement('div');
    lastOfTwoNewContent.innerHTML = `<div class='form-group'>
                  <p style="width: 20px;" class="m-2"> </p>
                  <p class="m-2 last-of-two-variant-counter" style="width: 20px;">${lastOfTwoOptCounter}</p>
                  <input type="text" class="form-control" id="message-text" placeholder="" style="width: 280px;">
                  
                  <p class="m-2" style="width: 10px; cursor: pointer; font-size: 1.3rem;"  onClick="this.parentNode.parentNode.removeChild(this.parentNode); deleteOptionsLastOfTwo();"><i class="fas fa-trash-alt" style="color: #D08383;"></i> </p>
                  </div>`;
    
    while (lastOfTwoNewContent.firstChild) {
      document.getElementById('lastOfTwoItemGroup').appendChild(lastOfTwoNewContent.firstChild);
    }

   
  })

    //ends variant code
  

  /*
  *
  *save variant data to the form 
  *
  */

  function saveOneItemData(){
    console.log('clicked 1')
}

  function saveTwoItemsData(){

    console.log('clicked 2')

  }

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