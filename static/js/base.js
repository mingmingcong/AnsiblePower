/**
 * Created by taoprogramer on 16/1/17.
 */
var Ansible = {
    init: function () {


        //ajax全局设置
        $.ajaxSetup({
            timeout: 30000,
            crossDomain: false,
            beforeSend: function (xhr, settings) {
                if (!Ansible.csrfSafeMethod(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", Ansible.getCsrftoken());
                }
            }

        });
    },
    /*
     获得浏览器cookie
     */
    getCookie: function (name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },
    /*
     Django csrftoken
     */
    getCsrftoken: function () {
        var csrftoken = this.getCookie('csrftoken');
        return csrftoken;
    },
    csrfSafeMethod: function (method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    },
};