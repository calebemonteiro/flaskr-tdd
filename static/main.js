console.log('App JQuery Ready.'); // sanity check

$(function() {
  // console.log('fading componente: ', $('.flash')); // debug fadeout
  $('div.flash').delay(3000).fadeOut();
});

$('.deleteRow').on('click', function() {
  var entry = $(this).parents('tr');
  $.ajax({
    type:'GET',
    url: '/delete' + '/' + this.id,
    context: entry,
    success:function(result) {
      if(result.status === 1) {
        entry.remove();
        console.log(result);
      }
    }
  });
});


