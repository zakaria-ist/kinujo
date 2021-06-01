var JPCUR = '\u5186';
var JPCASE = '\u4EF6';

$(document).on('click', 'input[type="text"]', function(){
    $(this).select();
});

$(document).on('click', 'input[type="number"]', function(){
    $(this).select();
});

$(document).on('click', 'input[type="password"]', function(){
    $(this).select();
});

$(function() {
    $('#nav-accordion').dcAccordion({
        eventType: 'click',
        autoClose: true,
        saveState: true,
        disableLink: true,
        speed: 'slow',
        showCount: false,
        autoExpand: true,
//        cookie: 'dcjq-accordion-1',
        classExpand: 'dcjq-current-parent'
    });
});

var Script = function () {

//    sidebar dropdown menu auto scrolling

    jQuery('#sidebar .sub-menu > a').click(function () {
        var o = ($(this).offset());
        diff = 250 - o.top;
        if(diff>0)
            $("#sidebar").scrollTo("-="+Math.abs(diff),500);
        else
            $("#sidebar").scrollTo("+="+Math.abs(diff),500);
    });

//    sidebar toggle

    $(function() {
        function responsiveView() { 
            var wSize = $(window).width();
            if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)){
                wSize = 760;
            }
            
            if (wSize <= 768) {
                $('#container').addClass('sidebar-close');
                $('#sidebar > ul').hide();
            }

            if (wSize > 768) {
                $('#container').removeClass('sidebar-close');
                $('#sidebar > ul').show();
            }
        }
        $(window).on('load', responsiveView);
        $(window).on('resize', responsiveView);
    });

    $('.fa-bars').click(function () {
        if ($('#sidebar > ul').is(":visible") === true) {
            $('#main-content').css({
                'margin-left': '0px'
            });
            $('#sidebar').css({
                'display': 'none'
            });
            try{
                if ( $.fn.DataTable.isDataTable( '.table' ) ) {
                    $('.table').DataTable().columns.adjust();
                }
            }
            catch(error){
                console.log(error);
            }
            $('#sidebar > ul').hide();
            $("#container").addClass("sidebar-closed");
            window.sessionStorage.setItem('is_sidebar', '0');
        } else {
            $('#main-content').css({
                'margin-left': '250px'
            });
            try{
                if ( $.fn.DataTable.isDataTable( '.table' ) ) {
                    $('.table').DataTable().columns.adjust();
                }
            }
            catch(error){
                console.log(error);
            }
            $('#sidebar > ul').show();
            $('#sidebar').css({
                'display': 'block'
            });
            $("#container").removeClass("sidebar-closed");
            window.sessionStorage.setItem('is_sidebar', '1');
        }
    });

// custom scrollbar
//     $("#sidebar").niceScroll({styler:"fb",cursorcolor:"#e8403f", cursorwidth: '3', cursorborderradius: '10px', background: '#404040', spacebarenabled:false, cursorborder: ''});
//
//     $("html").niceScroll({styler:"fb",cursorcolor:"#e8403f", cursorwidth: '6', cursorborderradius: '10px', background: '#404040', spacebarenabled:false,  cursorborder: '', zindex: '1000'});

// widget tools

    jQuery('.panel .tools .fa-chevron-down').click(function () {
        var el = jQuery(this).parents(".panel").children(".panel-body");
        if (jQuery(this).hasClass("fa-chevron-down")) {
            jQuery(this).removeClass("fa-chevron-down").addClass("fa-chevron-up");
            el.slideUp(200);
        } else {
            jQuery(this).removeClass("fa-chevron-up").addClass("fa-chevron-down");
            el.slideDown(200);
        }
    });


    jQuery('.panel .tools .fa-times').click(function () {
        jQuery(this).parents(".panel").parent().remove();
    });


//    tool tips

    $('.tooltips').tooltip();

//    popovers

    $('.popovers').popover();



// custom bar chart

    if ($(".custom-bar-chart")) {
        $(".bar").each(function () {
            var i = $(this).find(".value").html();
            $(this).find(".value").html("");
            $(this).find(".value").animate({
                height: i
            }, 2000)
        })
    }

}();

jQuery.browser = {};
(function () {
    jQuery.browser.msie = false;
    jQuery.browser.version = 0;
    if (navigator.userAgent.match(/MSIE ([0-9]+)\./)) {
        jQuery.browser.msie = true;
        jQuery.browser.version = RegExp.$1;
    }
})();


function prefill_select2(event){
/** * Pre-fills the search box with the current text from the Label. * Executes when the dropdown is opened */
    if ($( event.target ).val() !== ''){
        var input = $( event.target ).select2('data');

        if (!input[0]) {
            var search = $(".select2-search__field");

            search.val( $( event.target ).find('option[value="0"]').html() );
            search.select();
        }
        else {
            var value = input[0].text;
    
            if ( value !== null && $.trim(value) !== ""){
                var search = $(".select2-search__field");
                if ( search.length > 0){
                    search.val( value );
                    search.select();
                }
            }
        }
    }
}


function comma_format( number, decimals = 2, dec_point = '.', thousands_sep = ',' ) {
	// http://kevin.vanzonneveld.net
	// +   original by: Jonas Raoni Soares Silva (http://www.jsfromhell.com)
	// +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
	// +	 bugfix by: Michael White (http://crestidg.com)
	// +	 bugfix by: Benjamin Lupton
	// +	 bugfix by: Allan Jensen (http://www.winternet.no)
	// +	revised by: Jonas Raoni Soares Silva (http://www.jsfromhell.com)	
	// *	 example 1: number_format(1234.5678, 2, '.', '');
	// *	 returns 1: 1234.57	 
 
	var n = number, c = isNaN(decimals = Math.abs(decimals)) ? 2 : decimals;
	var d = dec_point == undefined ? "," : dec_point;
	var t = thousands_sep == undefined ? "." : thousands_sep, s = n < 0 ? "-" : "";
	var i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "", j = (j = i.length) > 3 ? j % 3 : 0;
 
	return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
}

// returns float equivalent of a number string
function float_format(number_str) {
    if (number_str == '') {
        number_str = '0';
    }
    return parseFloat(String(number_str).replace(/,/g , ''));
}

// returns int equivalent of a number string
function int_format(number_str) {
    return parseInt(float_format(number_str));
}

$(document).on("input", ".jan-input", function() {
    let temp_str = this.value;
    if (temp_str.length > 13) {
        temp_str = temp_str.slice(0, -1);
    }
    this.value = temp_str;
});

$(document).on("input", ".numeric_qty", function() {
    let temp_str = this.value.replace(/[^0-9\.]/g,'');
    if (temp_str.split(".").length-1 > 1) {
        temp_str = temp_str.slice(0, -1);
    }
    if (temp_str.split(".").length > 1) {
        let temp_str_2 = temp_str.split(".")[1];
        if (temp_str_2.length > 2) {
            this.value = temp_str.split(".")[0] + '.' + temp_str_2.slice(0, -1)
        } else {
            this.value = temp_str;
        }
    } else {
        this.value = temp_str;
    }

});

$(document).on("input", ".numeric_price", function() {
    let price_str = this.value.replace(/[^0-9\.]/g,'');
    if (price_str.split(".").length-1 > 1) {
        price_str = price_str.slice(0, -1);
    }
    if (price_str.split(".").length > 1) {
        let price_str_2 = price_str.split(".")[1];
        if (price_str_2.length > 6) {
            this.value = price_str.split(".")[0] + '.' + price_str_2.slice(0, -1)
        } else {
            this.value = price_str;
        }
    } else {
        this.value = price_str;
    }
});

function pure_number(value){
    if (value !== '' || value !== undefined ) {
        return float_format(value.replace(',', '').replace(' ', '').replace(JPCUR, ''));
    } else {
        return 0;
    }
}

Date.prototype.toDateInputValue = (function() {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0,10);
});

function roundDecimal(value, precision) {
    var multiplier = Math.pow(10, precision || 0);
    var interm = (value * multiplier).toFixed(1);
    return Math.round(interm) / multiplier;
}

// Translation fuction
function get_translate(e){
    try{
        let current_lang = "en";
        if(permanentStorage.getItem("language")){
            current_lang = permanentStorage.getItem("language");
        }

        if (current_lang == "ja") {
            if (translation_dict[e]) {
                return translation_dict[e];
            } else {
                return e;
            }
        } else if (current_lang == "en") {
            if (Object.keys(translation_dict).find(key => translation_dict[key] === e)) {
                return Object.keys(translation_dict).find(key => translation_dict[key] === e);
            } else {
                return e;
            }
        } else {
            return e;
        }
    } catch(error){
        console.log(error);
        return e;
    }
}

var translation_dict = {
    "Yes": "OK",
    "Save": "保存する",
    "Cancel": "キャンセル",
    "Warning": " ",
    "Error": "エラー",
    "Are you sure?": "削除しますか？",
    "Are you sure want to delete?": "削除してもよろしいですか？",
    "* If you delete the option, the registered JAN code and inventory information": "※選択肢を削除すると、登録済のJANコード・在庫情報も削除されます。",
    "* After you have deleted or edited your choices, click the Save button.": "※選択肢を削除・編集した後は、保存ボタンを押してください。",
    "Wrong Quantity!": "数量が間違っています！",
    "Order quantity must be greater than Zero": "注文数量は0より大きくなければなりません",
    "Please fill in the required fields": "必須フィールドを入力してください",
    "Order quantity cannot be greater than stock quantity": "注文数量は在庫数量を超えることはできません",
    "Choices field": "選択肢",
    "can't be empty": "を入力してください",
    "Do you want to update the stock?": "在庫を更新しますか？",
    "Do you want to update the price?": "価格を更新しますか？",
    "Success": "成功",
    "Confirmation Dialog": "確認ダイアログ",
    "Update Successful": "更新に成功しました",
    "Delete Successful": "削除に成功",
    "Account information is updated.": "アカウント情報が更新されます。",
    "Product information is updated.": "製品情報を更新しました。",
    "Product information is deleted.": "製品情報が削除されます。",
    "Salon information is updated.": "サロン情報を更新しました。",
    "Salon information is deleted.": "サロン情報を削除します。",
    "Shipping information is updated.": "配送情報を更新しました。",
    "Shipping information is deleted.": "配送情報が削除されます。",
    "URL String is duplicate": "URL文字列が重複しています",
    "JAN code / inventory editing": "JANコード/在庫編集",
    "JAN code can't be empty": "JANコードを入力してください",
    "Stock should contain only number": "在庫には数字のみを含める必要があります",
    "Tracking number is duplicate": "追跡番号が重複しています",
    " is in use. Try a new one. It must be unique": "は既に使われているため、使用できません。",
    'The number of stocks will change during editing. When changing, increase or decrease the absolute value such as "+1" or "-1" Please enter (If you want to change the entire stock quantity, enter "100" etc. as a numerical value) If the stock quantity field is blank, the stock quantity will not be changed.': "在庫数は編集中に変更されます。変更する場合は、「+ 1」や「-1」などの絶対値を増減してください（在庫量全体を変更する場合は、数値として「100」などを入力してください）。空白の場合、在庫数は変更されません。",
    "add / edit / delete items": "項目の追加・編集・削除",
    "Enter Jancode": "JANコードを入力",
    "Enter Stock": "在庫を入力",
    "Jan Code": "JANコード",
    "Stock Quantity": "在庫数",
    "Stock:": "在庫:",
    "Confirm": "はい",
    "Cancel": "キャンセル",
    "Item / Option": "項目・選択肢登録",
    "Items / Option": "項目・選択肢登録",
    "Code is Sent!": "コードが送信されました。",
    "A verification code is sent to your number.": "あなたの番号に認証コードが送信されます。",
    "Wrong number!": "間違った番号です。",
    "Please check your number and try again.": "番号をご確認の上、再度お試しください。",
    "The user is not registered.": "ユーザーが登録されていません。",
    "Vericication Successful": "検証成功",
    "Please enter new password to log in.": "新しいパスワードを入力してログインしてください。",
    "Wrong Code": "不正なコード",
    "Please check your verification code again.": "もう一度認証コードを確認してください。"

};