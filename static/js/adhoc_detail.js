var AdhocDetail = {
    globals: {
        interval_id: 0
    },
    init: function () {
        this.globals.interval_id = setInterval(this.loadTask, 1000);
        $(document).on('click', ".task-log", AdhocDetail.loadLog);
    },
    loadTask: function () {
        var hosts_body = $("#hosts_body")
        var task_id = hosts_body.attr('task_id');
        $.ajax({
            url: '/adhoc/' + task_id + '/',
            type: 'GET',
            success: function (data, textStatus, XMLHttpRequest) {
                hosts_body.html(data.result)
                if (data.finish == 1) {
                    clearInterval(AdhocDetail.globals.interval_id);
                    $("#hosts_heading").html("<i class='fa fa-desktop'></i> Hosts");
                }
            }
        });
    },
    loadLog: function (e) {
        var adhoc_task_id = $(this).attr('adhoc_task_id');
        $.ajax({
            url: adhoc_log,
            type: 'GET',
            data: {
                adhoc_task_id: adhoc_task_id
            },
            success: function (data, textStatus, XMLHttpRequest) {
                $("#stdout").html(data.result.stdout);
                $("#stderr").html(data.result.stderr);
                $("#log-title").html(data.result.task_host);

            }
        });
    }

}