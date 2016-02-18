/**
 * Created by taoprogramer on 16/2/17.
 */
var Dashboard = {
    init: function () {

        this.loadDash();
        setInterval(Dashboard.loadDash,60000);

    },
    loadDash: function () {
        $.ajax({
            url: dashboard,
            type: 'GET',
            success: function (data, textStatus, XMLHttpRequest) {
                console.log(data);
                $("#groups").html(data.groups);
                $("#hosts").html(data.hosts);
                $("#commands").html(data.commands);
                $("#jobs").html(data.jobs);
                $("#playbooks").html(data.playbooks);

                Dashboard.loadCommandStatus(data.recent_commands);
                Dashboard.loadJobStatus(data.recent_jobs);
            }
        });
    },
    loadCommandStatus: function (data) {
        var myChart = echarts.init(document.getElementById('recent-command'));
        var option = {
            title: {
                //subtext: '纯属虚构'
            },
            tooltip: {
                trigger: 'axis'
            },
            xAxis: [
                {
                    type: 'category',
                    boundaryGap: false,
                    data: data.date
                }
            ],
            grid: {
                x: 50,
            },
            yAxis: [
                {
                    type: 'value',
                    axisLabel: {
                        formatter: '{value} '
                    }
                }
            ],
            series: [
                {
                    name: ' run commands',
                    type: 'line',
                    data: data.count,

                },
            ]
        };

        myChart.setOption(option);

    },
    loadJobStatus: function (data) {
        var myChart = echarts.init(document.getElementById('recent-job'));
        var option = {
            title: {
                //subtext: '纯属虚构'
            },
            tooltip: {
                trigger: 'axis'
            },
            xAxis: [
                {
                    type: 'category',
                    boundaryGap: false,
                    data: data.date
                }
            ],
            grid: {
                x: 50,
            },
            yAxis: [
                {
                    type: 'value',
                    axisLabel: {
                        formatter: '{value}'
                    }
                }
            ],
            series: [
                {
                    name: 'run jobs',
                    type: 'line',
                    data: data.count,
                    lineStyle:{
                        normal:{
                            color:'#61a0a8'
                        }
                    }
                },
            ]
        };

        myChart.setOption(option);
    },
    loadHostStatus: function () {

    }
}