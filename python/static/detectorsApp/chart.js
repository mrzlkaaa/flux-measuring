$(document).ready(function(){
    var path = new URL(`${document.URL}`)
    console.log(path)
    id = path.pathname.split("/").slice(-1)
    $.ajax({
        url:`http://109.123.162.90:8080/api/experiment/${id}`,
        type:"GET",
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