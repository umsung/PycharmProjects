 {/*<script>*/}
        $(function () {
            error_check_password = false;
            error_check_username = false;
            error_check_upwd = false;
            error_check_checked = false;

            $('#uname').blur(function () {
                //账号框输入密码失去焦点时，调用检验账号的方法
                check_uname()
            });

            $('#upwd').blur(function () {
                check_upwd()  // 调用检验密码的方法
            })

            $('#spwd').blur(function () {
                //当重复输入密码框失去焦点时调用方法判断两次输入是否一直
                check_spwd()
            });

            $('#protocol').click(function () {
                check_checked()
            });


            function check_uname() {
                //判断用户名是否存在，是否合法
                var username = $('#uname').val();
                var len = username.length;
                console.log(username);
                console.log(isNaN(username));

                //用户名符合条件，发送给后台数据库进行对比是否已经注册
                if (isNaN(username) && (len > 6 && len < 18)) {
                    $('#uname').next().hide();

                    //post方法发送帐号给服务器，进行比对，
                    //第一个参数是url.第二个参数是发给服务器的post参数，第三个data是回调函数接收服务器返回的数据
                    $.post('/blog/check_name/', {'uname': username}, function (data) {
                        //
                        if (data.success == 0) {
                            $('#uname').next().html('用户名存在');
                            $('#uname').next().show();
                            error_check_username = false
                        }

                        else {
                            error_check_username = true
                            $('#uname').next().hide()
                        }
                    });

                } else {
                    //不满足条件提示用户
                    $('#uname').next().html('8-16位字符组成，不能是纯数字');
                    $('#uname').next().show();
                    error_check_username = false
                }
            }

            function check_upwd() {
                var upwd = $('#upwd').val();

                var re = /^[a-z0-9A-Z]{8,18}$/;  //正则

                if (re.test(upwd) && isNaN(upwd)) {
                    $('#upwd').next().hide()
                    error_check_upwd = true
                } else {
                    $('#upwd').next().html('密码为8-16位字母和数字组成')
                    $('#upwd').next().show()
                    error_check_upwd = false
                }
            }


            //判断用户两次输入的密码是否正确
            function check_spwd() {
                //获取两次输入密码
                var upwd = $('#upwd').val();
                var spwd = $('#spwd').val();
                //判断两次输入是否一直
                if (upwd != spwd) {
                    $('#spwd').next().html('两次输入的密码不一致');// 不一致的话显示
                    $('#spwd').next().show();
                    error_check_password = false;
                }
                else {
                    $('#spwd').next().hide();
                    error_check_password = true;

                }
            }

            //checked框，判断用户是否勾选协议
            function check_checked() {

                var start = $('#protocol').prop('checked');
                if (start) {
                    error_check_checked = true;
                    $('.protocol_error').hide()
                }
                else {
                    $('.protocol_error').html('请同意用户协议')
                    $('.protocol_error').show()
                    error_check_checked = false;
                }

            }

            //提交注册
            $(":submit").click(function () {

                //防止用户没有填写直接提交。
                check_uname()
                check_upwd()
                check_checked()
                check_spwd()

                console.log(error_check_password, error_check_username, error_check_checked, error_check_upwd)
                if (error_check_password && error_check_username && error_check_checked && error_check_upwd) {
                    // 如果全部条件都符合，那么提交表单数据
                    var username = $('#uname').val();
                    var upwd = $('#upwd').val();
                    $.post('/blog/register_user/', {'uname': username, 'upwd': upwd}, function (data) {
                        //注册成功 加载成功页面，或者重定向到其他页面
                        //window.href = 'http://www.baidu.com'
                        $('html').html(data)
                    })
                } else {
                    return false
                }
            })

        });


    // </script>