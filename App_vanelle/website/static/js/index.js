var maturity = [0.5,0.75,1.0,3.5,4.0,5.5,6,7];
var curve = [4,4.1,6,9,14,16,16.1,16.1];

function display() {
    var ctx = document.getElementById("myChart");
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: maturity,
            datasets:[{
                label: 'yield',
                data:curve,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        }
    })
}