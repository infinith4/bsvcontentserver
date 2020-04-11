$(function(){
    var address = $('#address').text()
    var transaction_count_str = $('input#transaction_count').val()
    var transaction_count = parseInt(transaction_count_str)
    var percnt = 5
    var current_transaction_index = 5;

    var offset_bottom_loadnote = $('.bottom_loadnote').offset();
    var request_current_transaction_index_list = [];
    $(document).scroll(function() {
        var scrollTop = $(this).scrollTop()
        var diff_bottom_content = offset_bottom_loadnote.top - window.innerHeight
        if (diff_bottom_content <= scrollTop) {
            $('.bottom_loadnote').css('visibility', 'visible');
            if($.inArray(current_transaction_index, request_current_transaction_index_list) == -1) {
                request_current_transaction_index_list.push(current_transaction_index);
                maxpercnt = percnt;
                if(current_transaction_index + percnt >= transaction_count) {
                    maxpercnt = transaction_count;
                }

                console.log("current_transaction_index: " + current_transaction_index + ", maxpercnt: " + maxpercnt);
                if(current_transaction_index < transaction_count) {
                    requestApiTx(current_transaction_index, maxpercnt).done(function(jsondata) {
                        $.each( jsondata['textdata_list'], function( index, value ) {
                                content = '<div class="mt-1 mb-1 border-bottom" id="textdata_' + current_transaction_index + '"><p class="text-left">' + value + '</p></div>';
                                $('.textdata_list').append(content);
                                current_transaction_index += 1
                            });
                        console.log(current_transaction_index);
                    }).fail(function(jsondata) {
                        console.log("error");
                    });
                }
            }
            offset_bottom_loadnote = $('.bottom_loadnote').offset();
        }
    });

    $('#send_upload_text').click(function(){
        var mnemonic_words = $("input[name='mnemonic_words']").val();
        var message = $("textarea[name='message']").val();
        requestApiUploadText(mnemonic_words, message)
        .done(function(jsondata, textStatus){
                content = '<div class="mt-1 mb-1 border-bottom"><p class="text-left">' + message + '</p></div>';
                $('.upload_textdata_list').prepend(content);
                $("input[name='mnemonic_words']").val("");
              })
        .fail(function(jqXHR, textStatus, errorThrown){
                console.log("failed");
        });
    });

    var requestApiTx = function(current_transaction_index, percnt){
        return $.ajax({
            type: "GET",
            url: "/api/tx/" + address + "?start_index=" + current_transaction_index + "&cnt=" + percnt,
            dataType: "json",
        });
    };

    var requestApiUploadText = function(mnemonic_words, message){
        return $.ajax(
            {
              url:'/api/upload_text',
              type:'POST',
              data:JSON.stringify({'mnemonic_words': mnemonic_words, 'message': message}),
              dataType: 'json',
              contentType: 'application/json'
            });
    }
});