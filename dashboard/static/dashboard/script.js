// script.js
document.addEventListener('DOMContentLoaded', function() {
    async function fetchData() {
        try {
            const response = await fetch('/api/futures-data/');
            const result = await response.json();

            if (result.status !== 'success') {
                console.error('Failed to fetch data');
                return;
            }

            const data = result.data;
            const latestChange = result.percentage_change;
            console.log('Latest Change:', latestChange);

            // Update percentage display
            const changeElement = document.getElementById('percentageChange');
            changeElement.textContent = `${latestChange}%`;
            
            // Add color class based on value
            changeElement.classList.toggle('negative', parseFloat(latestChange) < 0);

            // Chart creation
            const labels = data.map(entry => entry.date);
            const prices = data.map(entry => parseFloat(entry.average_price));
            
            const ctx = document.getElementById('futuresChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Average Price (€)',
                        data: prices,
                        borderColor: 'rgba(52, 107, 167, 0.8)',
                        tension: 0,
                        borderWidth: 2,
                        fill: false,
                        pointBackgroundColor: 'white',
                        pointBorderColor: 'rgba(52, 107, 167, 0.8)',
                    }]
                },
                options: {
                    maintainAspectRatio: false,
                    responsive: true,
                    layout: {
                        padding: {
                            top: 10,
                            bottom: 20,
                            left: 10,
                            right: 10
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                    },
                    scales: {
                        x: {
                            title: {
                                display: false
                            },
                            ticks: {
                                padding: 10,
                                autoSkip: true,
                                maxRotation: 0,
                                minRotation: 0
                            }
                        },
                        y: {
                            title: {
                                display: false
                            },
                            beginAtZero: false,
                            ticks: {
                                padding: 10
                            }
                        }
                    }
                }
            });
        } catch (error) {
            console.error('Error:', error);
        }
    }

    fetchData();
});