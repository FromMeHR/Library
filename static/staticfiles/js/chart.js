$(document).ready(function () {
    const ctx = document.getElementById("chart").getContext('2d');
    let myChart;

    $("#month-btn, #year-btn").click(function () {
        const timeframe = $(this).data('timeframe');
        const chartUrl = $(this).data('controller-url');
        updateChart(chartUrl, timeframe);
    });

    $("#submit-btn").click(function () {
        const startDate = $("#start-date").val();
        const endDate = $("#end-date").val();
        const chartUrl = $("#month-btn").data('controller-url');

        $.ajax({
            type: "GET",
            url: chartUrl,
            data: {
                timeframe: 'custom',
                start_date: startDate,
                end_date: endDate,
            },
            success: function (data) {
                if (myChart) {
                    myChart.destroy();
                }

                myChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: 'Частота бронювань',
                            backgroundColor: 'rgba(161, 198, 247, 1)',
                            borderColor: 'rgb(47, 128, 237)',
                            data: data.data,
                        }]
                    },
                    options: {
                        scales: {
                            yAxes: [{
                                ticks: {
                                    beginAtZero: true,
                                }
                            }]
                        }
                    },
                });
            },
            error: function (data) {
                console.log("Error");
            },
        });
    });

    const initialUrl = $("#month-btn").data('controller-url') + '?timeframe=month';
    updateChart(initialUrl, 'month');

    function updateChart(url, timeframe) {
        $.ajax({
            type: "GET",
            url: url,
            data: {
                timeframe: timeframe,
            },
            success: function (data) {
                if (myChart) {
                    myChart.destroy();
                }

                myChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: 'Частота бронювань',
                            backgroundColor: 'rgba(161, 198, 247, 1)',
                            borderColor: 'rgb(47, 128, 237)',
                            data: data.data,
                        }]
                    },
                    options: {
                        scales: {
                            yAxes: [{
                                ticks: {
                                    beginAtZero: true,
                                }
                            }]
                        }
                    },
                });
            },
            error: function (data) {
                console.log("Error");
            },
        });
    }
});
