/**
 * Created by taoprogramer on 16/1/28.
 */
var Adhoc = {
    init: function () {
        $(".retry").on('click', Adhoc.retryAdhoc)
    },
    retryAdhoc: function () {
        var adhoc_id = $(this).attr('adhoc_id');
        bootbox.confirm("Retry ?", function (res) {
            if (res) {
                $.ajax({
                    url: adhoc_add,
                    type: 'post',
                    data: {
                        adhoc_id: adhoc_id
                    },
                    success: function (data, textStatus, XMLHttpRequest) {
                        location.href = '/adhoc/' + data.result.adhoc_id + '/';
                    }
                });
            }
        })

    },
}