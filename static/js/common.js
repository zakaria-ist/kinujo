var JPCUR = '\u5186';

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
            // if ($('#sidebar').is(":visible") === true) {
                var wSize = $(window).width();
                if (wSize <= 768) {
                    $('#container').addClass('sidebar-close');
                    $('#sidebar > ul').hide();
                }

                if (wSize > 768) {
                    $('#container').removeClass('sidebar-close');
                    $('#sidebar > ul').show();
                }
            // }
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
                'margin-left': '310px'
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
    return float_format(value.replace(',', '').replace(' ', '').replace(JPCUR, ''))
}