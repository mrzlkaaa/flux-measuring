$(document).ready(function(){
    var type = document.getElementById("foil-type").textContent;
    var existing_value = document.getElementsByClassName("form-select");
    var $select = $(".form-select");
    $.ajax({
        // url:`http://localhost:8080/api/foil_detectors/${type}`,
        url:`http://109.123.162.90:8080/api/foil_detectors/${type}`,
        type:"GET",
        success: function(results) {
            console.log(results)
            $.each(results, function() {
                // $select.append($("<option />").val(this.Cross_section).text(this.Nuclide))
                if (existing_value[0].value != this.Name) {
                    $select.append(`<option value="${this.Name}-${this.Nucleus_number}">${this.Name}</option>`);
                }
            })
        }
    });
})