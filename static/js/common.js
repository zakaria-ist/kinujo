$(document).on('click', 'input[type="text"]', function(){
    $(this).select();
});

$(document).on('click', 'input[type="number"]', function(){
    $(this).select();
});

$(document).on('click', 'input[type="password"]', function(){
    $(this).select();
});

$('.fa-bars').click(function () {
    if ($('#sidebar > ul').is(":visible") === true) {
        $('#main-content').css({
            'margin-left': '0px'
        });
        $('#sidebar').css({
            'margin-left': '-245px'
        });
        try{
            $('.table').DataTable().columns.adjust();
        }
        catch(error){
            console.log(error);
        }
        $('#sidebar > ul').hide();
        $("#container").addClass("sidebar-closed");
    } else {
        $('#main-content').css({
            'margin-left': '245px'
        });
        try{
            $('.table').DataTable().columns.adjust();
        }
        catch(error){
            console.log(error);
        }
        $('#sidebar > ul').show();
        $('#sidebar').css({
            'margin-left': '0'
        });
        $("#container").removeClass("sidebar-closed");
    }
});