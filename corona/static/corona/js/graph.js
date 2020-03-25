$(function(){

$('td.country_wise_case').on('click',function(e){
    var country_name= $(this).data('country');
    $.ajax({
            url: '/corona/country_change',
            data: {'country': country_name},
            type: "GET",
        success: function(resp){
            $('div#myDiv').html(resp['data']);
            $('span.total_confirmed_cases').text(resp['total_confirmed']);
            $('span.total_death_cases').text(resp['total_deaths']);
            $('span.total_recovered_cases').text(resp['total_recovered']);
        }
    });

});

})
