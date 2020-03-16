
  $(function(){
  //   $('a.dlink').click(function(){
  //     var commentid= $(this).attr('dataname')
  //     var cmt = $(this).parents('div.cmt-item')
  //     if (commentid){
  //         $.ajax({
  //             url:'/'+commentid+'/deleteCommentApi',
  //             data:{'md5_id':hex_md5(commentid)},
  //             type:'post',
  //             success:function(data){
  //                 // cmt.hide()
  //                 // cmt.next().hide()
  //                 alert(data.msg)
  //                 window.location.reload();
  //             },
  //             error:function(data){
  //                 alert('未知错误!')
  //             }
  //         })
  //     }
  // });

  // function delComment(){
  //     var commentid= $(this).attr('dataname')
  //     console.log(commentid,id)
  //     var cmt = $(this).parents('div.cmt-item')
  //     if (commentid){
  //         $.ajax({
  //             url:'/'+commentid+'/deleteCommentApi',
  //             data:{'md5_id':hex_md5(commentid)},
  //             type:'post',
  //             success:function(data){
  //                 // cmt.hide()
  //                 // cmt.next().hide()
  //                 alert(data.msg)
  //                 window.location.reload();
  //             },
  //             error:function(data){
  //                 alert('未知错误!')
  //             }
  //         })
  //     }
  //   };


    $('a.taction').click(function(){
      var id= $.trim($(this).attr('dataname'))
      var art = $(this).parents('article.post')
      if(confirm('Are you Sure?')){
        $.ajax({
          url:"/"+id+"/deleteApi",
          type:'post',
          // async:false,
          success:function(data){
            if(data){
              if(data.result =='false' && data.ErrorInfo == 'nologin'){
                window.location.href = "http://127.0.0.1:5000/auth/login?returnurl=" + encodeURIComponent(window.location.href);
              }
              else{
                // alert(data.msg)
                window.location.reload();
              }
              // art.hide()
              // art.next().hide()
              
            }
          },
          error:function(){
            alert('失败')
            window.location.reload();
          }
        })
      }
    })

    
    // error_username = false;
    // error_password = false;
    // $('#test #username').blur(function(){
    //     check_username()
    //   });
  
    // $('#test #password').blur(function(){
    //   check_password()
    // });
  
    // function check_username(){
    //   var username = $.trim($('#test #username').val());
    //   var password =$.trim($('#test #password').val());
    //   var len_username = username.length;
    //   var len_password = username.length;
    //   var name_error = $('username').next();
    //   // isNaN检验参数是否为非数字值
    //   if(username=='' || username==undefined){
    //     name_error.html('账号不能为空');
    //     name_error.show();
    //     error_username = false;
        
    //   }
    //   if(isNaN(username) && len_username>=6){
    //     $('#username').next().hide()

    //     // $.post('/auth/check_name',{'username':username},function(data){
    //     //   if(data.result){
    //     //     error_username = true;
    //     //     $('#username').next().hide() 
    //     //   }
    //     //   else{
    //     //     $('#username').next().html('账号已存在')
    //     //     $('#username').next().show() 
    //     //     error_username = false
    //     //   }
    //     // })
    //     // 执行ajax时return false的function 与onsubmit()不是同一个函数，所以无论return 什么都会直接执行submit()提交表单
    //     $.ajax({
    //       url:'/auth/check_name',
    //       data:{'username':username},
    //       type:"post",
    //       async: false,
    //       success: function(data){
    //         if(data.result == '1'){
    //           $('#test #username').next().html('账号已存在');
    //           $('#test #username').next().show();
    //           error_username = false;
    //         }
    //         else{
    //           error_username = true;
    //           $('#test #username').next().hide()
              
    //         }
    //       }
    //     }) //end ajax
    //   }
    //   else{
    //     $('#test #username').next().html('账号不能为纯数字，不能小于6位数')
    //     $('#test #username').next().show() 
    //     error_username = false
    //   }
      
    // };
  
    // function check_password(){
    //   var password = $('#test #password').val();
    //   re = /^[a-zA-Z0-9]{6,18}$/;
    //   if(re.test(password)){
    //     $('#test #password').next().hide();
    //     error_password=true;
    //   }
    //   else{
    //     $('#test #password').next().html('密码不能小于6位')
    //     $('#test #password').next().show();
    //     error_password=false;
    //   }
    // };
    
    // $('#aa').click(function(){
    //   ss();
    // }); 
    

    // function ss(){
    //     check_password()
    //     check_username()
    //     // return true
    //     console.log(error_username,error_password)
    //     if(error_username && error_password){
    //       return true;
    //     }
    //     else{
    //       return false;
    //     }
    //   }//end register






    
  });
