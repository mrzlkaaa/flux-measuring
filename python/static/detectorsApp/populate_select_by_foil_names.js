$(document).ready(function(){
    var type = document.getElementById("foil-type").textContent;
    console.log(type);
    var $select = $(".form-select");
    $.ajax({
        url:`http://localhost:8080/api/foil_detectors/${type}`,
        type:"GET",
        success: function(results) {
            console.log(results)
            $.each(results, function() {
                // $select.append($("<option />").val(this.Cross_section).text(this.Nuclide))
                    $select.append(`<option value="${this.Name}-${this.Nucleus_number}">${this.Name}</option>`);
            })
        }
    });
})