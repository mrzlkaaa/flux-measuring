$(document).ready(function(){
    var myOpt = document.getElementsByClassName("form-select");
    var $select = $(".form-select");
    $.ajax({
        url:"http://109.123.162.90:8080/api/detector_params",
        type:"GET",
        success: function(results) {
            console.log(results)
            $.each(results, function() {
                // $select.append($("<option />").val(this.Cross_section).text(this.Nuclide))
                console.log(myOpt[0].value)
                if (myOpt[0].value != this.Nuclide) {
                    $select.append('<option value="' + this.Nuclide + '">' + this.Nuclide + '</option>');
                }
            })
            
        }
    });
})