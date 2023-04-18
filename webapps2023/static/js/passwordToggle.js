$(".togglePassword").click(function (e) {
      e.preventDefault();
      var type = $(this).parent().parent().find(".pwd").attr("type");    

      if(type == "password"){
          $("svg.showPwd").addClass("d-none");
          $("svg.hidePwd").removeClass("d-none");
          $(this).parent().parent().find(".pwd").attr("type","text");
      } else if(type == "text"){
            $("svg.showPwd").removeClass("d-none");
          $("svg.hidePwd").addClass("d-none");
          $(this).parent().parent().find(".pwd").attr("type","password");
      }
  });