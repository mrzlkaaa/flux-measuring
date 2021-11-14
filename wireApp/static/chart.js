$(document).ready(function(){
    $.ajax({
        url:"/api/chart",
        type:"GET",
        // data: {'button':button, "first":FirstName, "last":LastName, "email":Email, "mobile":Mobile},
        success: function(results) {
            obj = JSON.parse(results)
            console.log(obj.ID);
            const ctx = document.getElementById('myChart').getContext('2d');
            const myChart = new Chart(ctx, {
                type: 'scatter',
                data: {
                    labels: obj.ID,
                    datasets: [{
                        label: 'Data',
                        data: obj.Activity,
                        backgroundColor: [
                            'rgba(54, 162, 235, 0.5)',
                        ],
                        borderColor: [
                            'rgba(54, 162, 235, 1)',
                        ],
                        borderWidth: 1,
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                        },
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'Distribution of neutron radiation',
                        },
                    }
                }
            });
            // $('#response').html(results);
        }
    });
})