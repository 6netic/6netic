
function displayPopupDuringThreeSeconds(response) {
    // This function displays a message during 3 seconds

            setTimeout(function () { 
                    $("#popup-response").css("display", "block"); 
                }, 0);
            
            $("#popup").html(response);
            setTimeout(function () { 
                    $("#popup-response").css("display", "none"); 
                }, 3000); 
}
       
function saving(new_barcode){
    // This function saves a product using Ajax
        
    $.ajax({
        url: 'saveprd',
        type: 'GET',
        data: 'former_barcode='+"{{ search_prd.barcode }}"+'&new_barcode='+new_barcode,
        dataType: 'html',
        success: function(response, statut){ 
                    displayPopupDuringThreeSeconds(response);
                    /* The page could be refreshed immediately but it is optional
                    setTimeout(function() { location.reload(false); }, 2950);*/
        },
        error: function(result, status, error){
                    displayPopupDuringThreeSeconds(response);
        },
    });
}    
    