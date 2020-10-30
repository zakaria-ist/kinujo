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