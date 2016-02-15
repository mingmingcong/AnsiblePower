var JobDetail = {
    globals: {
        interval_id: 0
    },
    init: function () {
        this.globals.interval_id = setInterval(this.loadTask, 500);
        $(document).on('click', ".task-log", JobDetail.loadLog);
    },
    loadTask: function () {
        var hosts_body = $("#hosts_body")
        var task_id = hosts_body.attr('job_id');
        $.ajax({
            url: '/job/' + task_id + '/',
            type: 'GET',
            success: function (data, textStatus, XMLHttpRequest) {
                hosts_body.html(data.result)
                if (data.finish == 1) {
                    clearInterval(JobDetail.globals.interval_id);
                    $("#hosts_heading").html("<i class='fa fa-desktop'></i> Hosts");
                }
            }
        });
    },
    loadLog: function (e) {
        var job_id = $("#hosts_body").attr('job_id');
        var host = $(this).attr('host');
        $.ajax({
            url: job_log,
            type: 'GET',
            data: {
                job_id: job_id,
                host: host
            },
            success: function (data, textStatus, XMLHttpRequest) {
                $("#log-table").html(data.result);
                $("#log-title").html(data.host);
            }
        });
    }

}