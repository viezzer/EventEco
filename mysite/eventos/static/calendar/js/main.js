$(function() {

  rome(inline_cal, { 
    time: false, 
    weekdayFormat: 'short', 
    inputFormat: 'DD-MM-YYYY',
    initialValue: new Date().toLocaleDateString('pt-br')
  });

  rome(inline_cal).on('data', function (value) {
    result.innerText = value;
  })
});