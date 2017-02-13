$("input[type='text']").click(function(){
  var $this=$(this);
  $this.attr("placeholder","");
  $this.parent().find("label").addClass("label-top");
});