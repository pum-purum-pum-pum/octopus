// Place all the behaviors and hooks related to the matching controller here.
// All this logic will automatically be available in application.js.
// You can use CoffeeScript in this file: http://coffeescript.org/
//= require Chart.min

let first_color = 'hsla(0, 49%, 48%, 1)'//'hsla(1, 57%, 35%, 1)'
let second_color = 'hsla(215, 57%, 47%, 1)'//'hsla(239, 43%, 42%, 1)';
let first_color_transparent = 'hsla(0, 49%, 48%, 0.3)';
let second_color_transparent = 'hsla(215, 57%, 47%, 0.3)';


function drawPieChart(canvas, data, names) {
    new Chart(canvas, {
        type: 'pie',
        data: {
            labels: names,
            datasets:[{
                data: data.data,
                backgroundColor: [
                    first_color, second_color
                ],
            }]
        }
    })
}

function drawRadarChart(canvas, data, names) {
    new Chart(canvas, {
        type: 'radar',
        data: {
            labels: data.legend.axis,
            datasets:[{
                label: names[0],
                data: data.data[0],
                backgroundColor: first_color_transparent,
                borderColor: first_color,
                pointBorderColor: "#fff",
                pointHoverBackgroundColor: "#fff",
            }, {
                label: names[1],
                data: data.data[1],
                backgroundColor: second_color_transparent,
                borderColor: second_color,
                pointBorderColor: "#fff",
                pointHoverBackgroundColor: "#fff",
            }]
        },
        options: {
            scale: {
                ticks: {
                    display: false,
                    min: 0,
                    max: 1
                }
            }
        }
    })
}

function drawSideToSideChart(canvas, data, names) {
    new Chart(canvas, {
        type: 'horizontalBar',
        data: {
            labels: data.legend.axis,
            datasets:[{
                label: names[0],
                data: data.data[0],
                backgroundColor: first_color,
            }, {
                label: names[1],
                data: data.data[1],
                backgroundColor: second_color,
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    ticks: {
                        min: 0,
                        max: 1,
                    }
                }]
            }
        }
    })
}