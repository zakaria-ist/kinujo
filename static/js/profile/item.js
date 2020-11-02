function loadItemTableData() {
    $('#item-table').DataTable().destroy();
    $('#item-table').DataTable({
        "order": [[2, "asc"]],
        "pageLength": 25,
        "serverSide": true,
        "scrollX": true,
        //stateSave: true,
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

function prepareVarientTwoTable(json){
    let variety2 = json.varieties;
    let v_names2 = [];
    let v_jancodes2 = [];
    let v_stocks2 = [];
    let horizontals = [];
    let verticals = [];
    let v_selections2 = [];
    for (let i=0; i<variety2.length; i++) {
        v_jancodes2.push(variety2[i].jan_code);
        v_stocks2.push(variety2[i].stock);

        if (horizontals.indexOf(variety2[i].varieties[0].selection) === -1) {
            horizontals.push(variety2[i].varieties[0].selection);
        }
        if (verticals.indexOf(variety2[i].varieties[1].selection) === -1) {
            verticals.push(variety2[i].varieties[1].selection);
        }

        v_selections2.push({
            "X": variety2[i].varieties[0].selection, 
            "Y": variety2[i].varieties[1].selection
        });

        if (v_names2.indexOf(variety2[i].varieties[0].name) === -1) {
            v_names2.push(variety2[i].varieties[0].name);
        }
        if (v_names2.indexOf(variety2[i].varieties[1].name) === -1) {
            v_names2.push(variety2[i].varieties[1].name);
        }
    }

    let varietyTableTwo1 = document.getElementById('variety-table-two');
    let firstOfTwoVariantChoicesOriginal = horizontals;
    let lastOfTwoVariantChoicesOriginal = verticals;

    varietyTableTwo1.innerHTML = '';
    //if empty table
    if(varietyTableTwo1.innerHTML.trim() === ''){
        varietyTableTwo1.innerHTML = `
            <div class="col-md-2" style="max-width: 140px; min-width: 140px;">
                <div class="row" id="two-variant-title-left">
                <div class="variant-title variant-col"><span id="cell-name">${v_names2[0]} / ${v_names2[1]}</span></div>
                </div>
                <div class="row" id="two-variant-info-left">
                <!--place for second variable name choices -->
                </div>
            </div>
            <div class="col-md-8">
                <div class="row" id="two-variant-title-row">
                
                </div>
                
                <div class="row">

                <div class="col-md-12" id="addTwoItems">

                </div>

                </div>

            </div>
        `;

        
        if(lastOfTwoVariantChoicesOriginal.length > firstOfTwoVariantChoicesOriginal.length){

            for(let i = 0; i < lastOfTwoVariantChoicesOriginal.length; i++){
              let newTableFirstChoices = document.createElement('div'); 
              let newTableLastChoices = document.createElement('div');
              let infoRow = document.createElement('div');
              let lastChoicesValue = lastOfTwoVariantChoicesOriginal[i];
              let firstChoicesValue;
              if(firstOfTwoVariantChoicesOriginal[i] === undefined){
                firstOfTwoVariantChoicesOriginal[i] = 'empty';
                firstChoicesValue = 'empty';
                
              }else{
                firstChoicesValue = firstOfTwoVariantChoicesOriginal[i];
              }

              newTableLastChoices.innerHTML = `<div class="variant-title-left variant-col">${lastChoicesValue}</div>`;
              if (firstChoicesValue != 'empty') {
                newTableFirstChoices.innerHTML = `<div class="variant-title variant-title-top variant-col">${firstChoicesValue}</div>`;
              }
              infoRow.innerHTML = `<div class="row flex-wrap" id="two-variant-cont-row-${i}">
                    
                  </div>`;
  
              if(newTableLastChoices.firstChild){
                document.getElementById('two-variant-info-left').appendChild(newTableLastChoices.firstChild);
              }
              if(newTableFirstChoices.firstChild){
                document.getElementById('two-variant-title-row').appendChild(newTableFirstChoices.firstChild);
              }
  
              if(infoRow.firstChild){
                document.getElementById('addTwoItems').appendChild(infoRow.firstChild);
  
                for(let j = 0; j < firstOfTwoVariantChoicesOriginal.length; j++){
                    let janCode2;
                    let stocks2;
                    let indx = v_selections2.findIndex((item) => (item.X === firstOfTwoVariantChoicesOriginal[j] && item.Y === lastOfTwoVariantChoicesOriginal[i]));
                    if (indx !== -1) {
                        janCode2 = v_jancodes2[indx];
                        stocks2 = v_stocks2[indx];

                        let addInfoCol = document.createElement('div');
                        addInfoCol.innerHTML = `<div class="variant-info variant-col" style="display: grid;"><p class="table-p" id="cell-name-value-r${i}c${j}" style="display: none;">${firstOfTwoVariantChoicesOriginal[j]} / ${lastOfTwoVariantChoicesOriginal[i]}</p><p class="text-center table-p" id="jan-id-r${i}c${j}">${janCode2}</p><p class="text-center table-p" id="stock-id-r${i}c${j}">Stock:${stocks2}</p><p class="table-p" style="align-content: baseline;"><i class="far edit-btn" id="edit-id-r${i}c${j}" onclick="editBtn(this);">&#xf044;</i></p></div>`;
                    
                        let id = `two-variant-cont-row-${i}`;
                        if(addInfoCol.firstChild){
                            document.getElementById(id).appendChild(addInfoCol.firstChild);
                        }
                    }
                }
              }
            }
  
          }else{
            //if two choices are equal or  firstOfTwoVariantChoicesOriginal > lastOfTwoVariantChoicesOriginal
            for(let i = 0; i < firstOfTwoVariantChoicesOriginal.length; i++){
                let newTableFirstChoices = document.createElement('div'); 
                let newTableLastChoices = document.createElement('div');
                let infoRow = document.createElement('div');
                let firstChoicesValue = firstOfTwoVariantChoicesOriginal[i];
                let lastChoicesValue;
                if(lastOfTwoVariantChoicesOriginal[i] === undefined){
                    lastOfTwoVariantChoicesOriginal[i] = 'empty';
                    lastChoicesValue = 'empty';
                    
                }else{
                    lastChoicesValue = lastOfTwoVariantChoicesOriginal[i];
                }
                if (lastChoicesValue != 'empty') {
                    newTableLastChoices.innerHTML = `<div class="variant-title-left variant-col">${lastChoicesValue}</div>`;
                }
                newTableFirstChoices.innerHTML = `<div class="variant-title variant-title-top variant-col">${firstChoicesValue}</div>`;
                infoRow.innerHTML = `<div class="row flex-wrap" id="two-variant-cont-row-${i}">
                        
                    </div>`;
    
                if(newTableLastChoices.firstChild){
                    document.getElementById('two-variant-info-left').appendChild(newTableLastChoices.firstChild);
                }
                if(newTableFirstChoices.firstChild){
                    document.getElementById('two-variant-title-row').appendChild(newTableFirstChoices.firstChild);
                }
    
                if(infoRow.firstChild){
                    document.getElementById('addTwoItems').appendChild(infoRow.firstChild);
    
                    for(let j = 0; j < firstOfTwoVariantChoicesOriginal.length; j++){
                        let janCode2;
                        let stocks2;
                        let indx = v_selections2.findIndex((item) => (item.X === firstOfTwoVariantChoicesOriginal[j] && item.Y === lastOfTwoVariantChoicesOriginal[i]));
                        if (indx !== -1) {
                            janCode2 = v_jancodes2[indx];
                            stocks2 = v_stocks2[indx];
                            
                            let addInfoCol = document.createElement('div');
                            addInfoCol.innerHTML = `<div class="variant-info variant-col" style="display: grid;"><p class="table-p" id="cell-name-value-r${i}c${j}" style="display: none;">${firstOfTwoVariantChoicesOriginal[j]} / ${lastOfTwoVariantChoicesOriginal[i]}</p><p class="text-center table-p" id="jan-id-r${i}c${j}">${janCode2}</p><p class="text-center table-p" id="stock-id-r${i}c${j}">Stock:${stocks2}</p><p class="table-p" style="align-content: baseline;"><i class="far edit-btn" id="edit-id-r${i}c${j}" onclick="editBtn(this);">&#xf044;</i></p></div>`;
    
                            let id = `two-variant-cont-row-${i}`;
                            if(addInfoCol.firstChild){
                                document.getElementById(id).appendChild(addInfoCol.firstChild);
                            }
                        }
                    }
                }
          }
        }
    }

    varietyTableTwo1.style.height = '250px';

    // document.getElementById('firstOfTwoItemGroup').innerHTML = `
    //             <div class="form-group">
                
    //             <p style="width: 20px;" class="m-2"> </p>
    //             <p class="m-2 first-of-two-variant-counter" style="width: 20px;">1</p>
    //             <input type="text" class="form-control first-of-two-items-choices" id="message-text" placeholder="" style="width: 280px;">
                
    //             <p class="m-2" style="width: 10px; cursor: pointer; font-size: 1.3rem;"  onClick="if(document.getElementById('err-line-one')){if(document.getElementById('err-line-one').innerHTML === this.parentNode.getElementsByClassName('first-of-two-variant-counter')[0].innerHTML){document.getElementById('first-of-two-title-error').innerHTML = ''}}; deleteOptionsFirstOfTwo(this);"><i class="fas fa-trash-alt" style="color: #D08383;"></i> </p>
    //             </div>
    //             <div class="form-group">
    //             <p style="width: 20px;" class="m-2"> </p>
    //             <p class="m-2 first-of-two-variant-counter" style="width: 20px;">2</p>
    //             <input type="text" class="form-control first-of-two-items-choices" id="message-text" placeholder="" style="width: 280px;">
                
    //             <p class="m-2" style="width: 10px; cursor: pointer; font-size: 1.3rem;"  onClick="if(document.getElementById('err-line-one')){if(document.getElementById('err-line-one').innerHTML === this.parentNode.getElementsByClassName('first-of-two-variant-counter')[0].innerHTML){document.getElementById('first-of-two-title-error').innerHTML = ''}}; deleteOptionsFirstOfTwo(this);"><i class="fas fa-trash-alt" style="color: #D08383;"></i> </p>
    //             </div>
    //         `;
    // document.getElementById('lastOfTwoItemGroup').innerHTML = `
    //             <div class="form-group">
    //                 <p style="width: 20px;" class="m-2"> </p>
    //                 <p class="m-2 last-of-two-variant-counter" style="width: 20px;">1</p>
    //                 <input type="text" class="form-control last-of-two-items-choices" id="message-text" placeholder="" style="width: 280px;">
                    
    //                 <p class="m-2" style="width: 10px; cursor: pointer; font-size: 1.3rem;"  onClick="if(document.getElementById('err-line-two')){if(document.getElementById('err-line-two').innerHTML === this.parentNode.getElementsByClassName('last-of-two-variant-counter')[0].innerHTML){document.getElementById('last-of-two-title-error').innerHTML = ''}}; this.parentNode.parentNode.removeChild(this.parentNode); deleteOptionsLastOfTwo();"><i class="fas fa-trash-alt" style="color: #D08383;"></i> </p>
    //             </div>
                
    //             <div class="form-group">
    //                 <p style="width: 20px;" class="m-2"> </p>
    //                 <p class="m-2 last-of-two-variant-counter" style="width: 20px;">2</p>
    //                 <input type="text" class="form-control last-of-two-items-choices" id="message-text" placeholder="" style="width: 280px;">
                    
    //                 <p class="m-2" style="width: 10px; cursor: pointer; font-size: 1.3rem;"  onClick="if(document.getElementById('err-line-two')){if(document.getElementById('err-line-two').innerHTML === this.parentNode.getElementsByClassName('last-of-two-variant-counter')[0].innerHTML){document.getElementById('last-of-two-title-error').innerHTML = ''}};this.parentNode.parentNode.removeChild(this.parentNode); deleteOptionsLastOfTwo();"><i class="fas fa-trash-alt" style="color: #D08383;"></i> </p>
    //             </div>
    //             `;

    document.getElementById('variety-content').innerHTML = `<div class="col-md-12"><button id="two-items-btn" type="button" class="btn btn-secondary" data-toggle="modal" data-target="#twoItemsVariant" onclick="changeModalTwo();">+ Items / Options</button></div>`;
    //change add item button
    addItemBtnChange(document.getElementById('variety-table-two'), document.getElementById('two-items-btn'));
}


function prepareVarientOneTable(json){
    let variety1 = json.varieties;
    let v_name = '';
    let v_jancodes = [];
    let v_stocks = [];
    let v_selections = [];
    for (let i=0; i<variety1.length; i++) {
        v_jancodes.push(variety1[i].jan_code);
        v_stocks.push(variety1[i].stock);
        v_selections.push(variety1[i].varieties[0].selection);
        v_name = variety1[i].varieties[0].name;
    }

    const varietyTable1 = document.getElementById('variety-table');

    varietyTable1.innerHTML = '';

    //create table wrapper for the one item variant
    if(varietyTable1.innerHTML.trim() === ''){
      varietyTable1.innerHTML = `
      <div class="col-md-2" style="max-width: 140px; min-width: 140px"><div class="row" id="one-variant-title-left">
        <div class="variant-title variant-col"><sapn id="cell-name">${v_name}</sapn></div>
      </div>
      <div class="row" id="one-variant-info-left">
        <div class="variant-info variant-col"><h3>-</h3></div>
      </div>
      </div>
      <div class="col-md-8">
        <div class="row" id="scrollable">
          <div class="col-md-12">
            <div class="row" id="one-variant-title-row">
              
            </div>
          </div>
          <div class="col-md-12">
            <div class="row" id="one-variant-info-row">
              
            </div>
          </div>
        </div>
      </div>
      `
    }

    for(let i = 0; i < variety1.length; i++){
      let newTableChoices = document.createElement('div'); 
      let newTableContent = document.createElement('div'); 
      let choicesValue = v_selections[i];
      let janValue = v_jancodes[i];
      let stockValue = v_stocks[i];
      newTableChoices.innerHTML = `<div class="variant-title variant-col" id="cell-name-value-${i}">${choicesValue}</div>`;
      newTableContent.innerHTML = `<div class="variant-info variant-col" style="display: grid;"><p class="text-center table-p" id="jan-id-${i}">${janValue}</p><p class="text-center table-p" id="stock-id-${i}">Stock:${stockValue}</p><p class="table-p" style="align-content: baseline;"><i class="far edit-btn" id="edit-id-${i}" onclick="editBtn(this);">&#xf044;</i></p></div>`;
      
      
      if(newTableChoices.firstChild){
        document.getElementById('one-variant-title-row').appendChild(newTableChoices.firstChild);
      }

      if(newTableContent.firstChild){
        document.getElementById('one-variant-info-row').appendChild(newTableContent.firstChild);
      }

    }
    //make sure it's scroll able
    document.getElementById("scrollable").style.overflow= 'scroll';

    //reset modal form
    // document.getElementById('oneItemGroup').innerHTML = `
    //             <div class="form-group">
    //               <p style="width: 20px;" class="m-2"> </p>
    //               <p class="m-2 one-variant-counter" style="width: 20px;">1</p>
    //               <input value="" type="text" class="form-control one-item-choices" id="message-text" placeholder="" style="width: 160px;">
                  
    //               <input value="" type="text" class="form-control one-item-jan-code" id="message-text" placeholder="" style="width: 140px;">
                  
    //               <input value="" type="number" class="form-control one-item-stock" id="message-text" placeholder="" style="width: 70px;">
    //               <p class="m-2" style="width: 10px; cursor: pointer; font-size: 1.3rem;"  onClick="if(document.getElementById('errLine')){if(document.getElementById('errLine').innerHTML === this.parentNode.getElementsByClassName('one-variant-counter')[0].innerHTML){document.getElementById('title-error').innerHTML = ''}}; deleteOptions(this);"><i class="fas fa-trash-alt" style="color: #D08383;"></i> </p>
    //             </div>
    //             <div class="form-group">
    //               <p style="width: 20px;" class="m-2"> </p>
    //               <p class="m-2 one-variant-counter" style="width: 20px;">2</p>
    //               <input value=""  type="text" class="form-control one-item-choices" id="message-text" placeholder="" style="width: 160px;">
                  
    //               <input value=""  type="text" class="form-control one-item-jan-code" id="message-text" placeholder="" style="width: 140px;">
                  
    //               <input value=""  type="number" class="form-control one-item-stock" id="message-text" placeholder="" style="width: 70px;">
    //               <p class="m-2" style="width: 10px; cursor: pointer; font-size: 1.3rem;"  onClick="if(document.getElementById('errLine')){if(document.getElementById('errLine').innerHTML === this.parentNode.getElementsByClassName('one-variant-counter')[0].innerHTML){document.getElementById('title-error').innerHTML = ''}}; deleteOptions(this);"><i class="fas fa-trash-alt" style="color: #D08383;"></i> </p>
    //             </div>

    //           `;

    //change add item button
    document.getElementById('variety-content').innerHTML = `<div class="col-md-12"><button id="one-item-btn" type="button" class="btn btn-secondary" data-toggle="modal" data-target="#oneItemVariant" onclick="changeModalOne();">+ Item / Option</button></div>`;
    addItemBtnChange(document.getElementById('variety-table'), document.getElementById('one-item-btn'));
  }

var g_product_id = '';

Date.prototype.toDateInputValue = (function() {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0,10);
});

function showProductForm(product_id='') {
    $('#item_tab').html('');
    $.get("/profiles/templates/product_form/", function(data){
        $('#item_tab').html(data);
        deleteAny();
        var options = '';
        $.each(category_list, function(i, v) {
            options += "<option value='"+v[0]+"'>"+v[1]+"</option>";
        });
        $('#category').html(options);
        if (!$('#category').data('select2')) {
            $('#category').select2({});
        }
        $('#category').on("select2:open", function( event ){
            prefill_select2(event);
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
        } else {
            $('#none').click();
            $('#published').click();
            $('#new').click();
            $('#all-users').click();
            $('#opened_date').val(new Date().toDateInputValue());
        }
    });
}

function setEditFormInputs(json) {
    $('#name').val(json.name);
    $('#brand_name').val(json.brand_name);
    $('#description').val(json.description);
    $('#pr').val(json.pr);
    $('#url_str').val(json.url_str);
    $('#store_price').val(comma_format(json.store_price, 0) + ' ' + JPCUR);
    $('#price').val(comma_format(json.price, 0) + ' ' + JPCUR);
    $('#shipping_fee').val(comma_format(json.shipping_fee, 0) + ' ' + JPCUR);
    $('#category').val(json.category).trigger('change');
    $('#opened_date').val(json.opened_date).trigger('change');
    $("input[name=target]").val([json.target]);
    $("input[name=status]").val([json.is_opened]);
    $("input[name=is_used]").val([json.is_used]);
    $("input[name=variety]").val([json.variety]).trigger('change');
    
    for(let i=0; i<json.images.length; i++) {
        if (json.images[i].image_no == '1') {
            $('#img_image0').attr("src", json.images[i].url);
        } else if (json.images[i].image_no == '2') {
            $('#img_image1').attr("src", json.images[i].url);
        } else if (json.images[i].image_no == '3') {
            $('#img_image2').attr("src", json.images[i].url);
        } else if (json.images[i].image_no == '4') {
            $('#img_image3').attr("src", json.images[i].url);
        } else if (json.images[i].image_no == '5') {
            $('#img_image4').attr("src", json.images[i].url);
        }
    }

    if (json.variety == '0') {
        let vrty = json.varieties[0];
        $('#jan_code').val(vrty.jan_code);
        $('#stock').val(vrty.stock);
        deleteAny();
    } else if (json.variety == '1') {
        document.getElementById("none-div").style.display = "none";
        prepareVarientOneTable(json);
    } else if (json.variety == '2') {
        document.getElementById("none-div").style.display = "none";
        prepareVarientTwoTable(json);
    }
}

function saveProductInfo() {

    var is_valid = validateProductForm();

    if (is_valid) {
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
                "stock": document.getElementById('stock-id-'+i).innerHTML.split(':')[1].trim(),
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
                let stock = document.getElementById(stockId).innerHTML.split(':')[1].trim();

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
        data.append("price", pure_number($('#price').val()));
        data.append("store_price", pure_number($('#store_price').val()));
        data.append("shipping_fee", pure_number($('#shipping_fee').val()));
        data.append("opened_date", $('#opened_date').val());
        data.append("is_opened", $('input[name="status"]:checked').val());
        data.append("is_used", $('input[name="is_used"]:checked').val());
        data.append("is_draft", '0');
        data.append("variety", variety);
        data.append("varieties", JSON.stringify(varieties));

        // let imageLength = document.getElementsByClassName('images').length;
        // for(let i = 0; i < imageLength; i++){
        //     let fileId = `file-${i}`;  
        //     data.append("product_image", document.getElementById(fileId).files[0]);
        // }
        if ($('#product_image0').prop('files')[0] !== undefined) {
            data.append("product_image0", $('#product_image0').prop('files')[0]);
        }
        if ($('#product_image1').prop('files')[0] !== undefined) {
            data.append("product_image1", $('#product_image1').prop('files')[0]);
        }
        if ($('#product_image2').prop('files')[0] !== undefined) {
            data.append("product_image2", $('#product_image2').prop('files')[0]);
        }
        if ($('#product_image3').prop('files')[0] !== undefined) {
            data.append("product_image3", $('#product_image3').prop('files')[0]);
        }
        if ($('#product_image4').prop('files')[0] !== undefined) {
            data.append("product_image4", $('#product_image4').prop('files')[0]);
        }
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

function validateProductForm() {
    var is_valid = true;

    if ( $('#name').val() != '' ) {
        $('#name').removeClass('highlight-mandatory');
    } else {
        $('#name').addClass('highlight-mandatory');
        is_valid = false;
    }
    if ( $('#description').val() != '' ) {
        $('#description').removeClass('highlight-mandatory');
    } else {
        $('#description').addClass('highlight-mandatory');
        is_valid = false;
    }
    if ( $('#pr').val() != '' ) {
        $('#pr').removeClass('highlight-mandatory');
    } else {
        $('#pr').addClass('highlight-mandatory');
        is_valid = false;
    }
    if ( $('#url_str').val() != '' ) {
        $('#url_str').removeClass('highlight-mandatory');
    } else {
        $('#url_str').addClass('highlight-mandatory');
        is_valid = false;
    }
    if ( $('#category').val() != '' ) {
        $('#category').removeClass('highlight-mandatory');
    } else {
        $('#category').addClass('highlight-mandatory');
        is_valid = false;
    }
    if ( $('#price').val() != '' ) {
        $('#price').removeClass('highlight-mandatory');
    } else {
        $('#price').addClass('highlight-mandatory');
        is_valid = false;
    }
    if ( $('#store_price').val() != '' ) {
        $('#store_price').removeClass('highlight-mandatory');
    } else {
        $('#store_price').addClass('highlight-mandatory');
        is_valid = false;
    }
    if ( $('#shipping_fee').val() != '' ) {
        $('#shipping_fee').removeClass('highlight-mandatory');
    } else {
        $('#shipping_fee').addClass('highlight-mandatory');
        is_valid = false;
    }
    if ( $('#opened_date').val() != '' ) {
        $('#opened_date').removeClass('highlight-mandatory');
    } else {
        $('#opened_date').addClass('highlight-mandatory');
        is_valid = false;
    }
    if ( $('input[name="status"]:checked').val() != undefined && $('input[name="status"]:checked').val() != '' ) {
        $('#status-div').removeClass('highlight-mandatory');
    } else {
        $('#status-div').addClass('highlight-mandatory');
        is_valid = false;
    }
    if ( $('input[name="is_used"]:checked').val() != undefined && $('input[name="is_used"]:checked').val() != '' ) {
        $('#is_used-div').removeClass('highlight-mandatory');
    } else {
        $('#is_used-div').addClass('highlight-mandatory');
        is_valid = false;
    }
    if ( $('input[name="target"]:checked').val() != undefined && $('input[name="target"]:checked').val() != '' ) {
        $('#target-div').removeClass('highlight-mandatory');
    } else {
        $('#target-div').addClass('highlight-mandatory');
        is_valid = false;
    }
    // let imageLength = document.getElementsByClassName('images').length;
    // if ( imageLength > 0 ) {
    //     $('#img-wrapper').removeClass('highlight-mandatory');
    // } else {
    //     $('#img-wrapper').addClass('highlight-mandatory');
    //     is_valid = false;
    // }
    if ( $('input[name="variety"]:checked').val() != undefined && $('input[name="variety"]:checked').val() != '' ) {
        $('#variety-div').removeClass('highlight-mandatory');
        if ($('input[name="variety"]:checked').val() == '0') {
            if ( $('#jan_code').val() != '' ) {
                $('#jan_code').removeClass('highlight-mandatory');
            } else {
                $('#jan_code').addClass('highlight-mandatory');
                is_valid = false;
            }
            if ( $('#stock').val() != '' ) {
                $('#stock').removeClass('highlight-mandatory');
            } else {
                $('#stock').addClass('highlight-mandatory');
                is_valid = false;
            }
        } else {
            $('#jan_code').removeClass('highlight-mandatory');
            $('#stock').removeClass('highlight-mandatory');
            // check if varient table exist
            let variantTableCol = document.getElementsByClassName('variant-info');
            if (variantTableCol.length > 0) {
                $('#variety-div').removeClass('highlight-mandatory');
            } else {
                $('#variety-div').addClass('highlight-mandatory');
                is_valid = false;
            }
        }
    } else {
        $('#variety-div').addClass('highlight-mandatory');
        is_valid = false;
    }

     return is_valid;
}