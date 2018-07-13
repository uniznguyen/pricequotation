
$(document).ready(function(){
  $("#searchbox").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $(".myTable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });

  $('tbody').sortable();


  $('.select_all_cat').click(function (e) {
    $(this).closest('table').find('td input:checkbox').prop('checked', this.checked);
  });

  $("#select_all_master").click(function() {
    if ($(this).text() == 'Select All'){
        $("input:checkbox").prop('checked', true);
        $(this).text('Unselect All').removeClass("btn-primary").addClass("btn-default");
    } else {
          $("input:checkbox").prop('checked', false);
          $(this).text('Select All').removeClass("btn-default").addClass("btn-primary");
    }
  });

});



