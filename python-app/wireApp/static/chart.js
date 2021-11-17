$(document).ready(function(){
    var path = new URL(`${document.URL}`)
    id = path.pathname.split("/").slice(-1)
    $.ajax({
        // url:"/api/chart",
        url:`http://192.168.45.221:8080/api/experiment/${id}`,
        type:"GET",
        // data: {'button':button, "first":FirstName, "last":LastName, "email":Email, "mobile":Mobile},
        success: function(results) {
            console.log(results)
            const ctx = document.getElementById('myChart').getContext('2d');
            const myChart = new Chart(ctx, {
                type: 'scatter',
                data: {
                    labels: results.Name,
                    datasets: [{
                        label: 'Data',
                        data: results.Activity,
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
        }
    });
})