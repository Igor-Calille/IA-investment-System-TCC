document.addEventListener('DOMContentLoaded', async () => {
    const stockSymbol = 'AAPL';

    const fetchDataAndRenderChart = async () => {
        try {
            const response = await fetch(`http://localhost:8000/stock-fetcher-service/stock-historicaldata/?symbol=${stockSymbol}&start_date=2014-01-01`);
            const data = await response.json();

            console.log('Dados recebidos:', data);  // Adicione este log para verificar os dados recebidos

            // Verifique a estrutura dos dados recebidos
            if (data && Array.isArray(data)) {
                // Converte as datas para objetos Date do JavaScript, lidando com o timezone offset
                const series = data.map(entry => ({
                    x: new Date(entry.date),
                    y: [entry.open, entry.high, entry.low, entry.close]
                }));

                console.log('Série:', series);  // Verifique a série de dados

                const options = {
                    series: [{
                        name: 'Stock Prices',
                        data: series
                    }],
                    chart: {
                        type: 'candlestick',
                        height: 350
                    },
                    title: {
                        text: `Stock Data for ${stockSymbol}`,
                        align: 'left'
                    },
                    xaxis: {
                        type: 'datetime'
                    },
                    yaxis: {
                        tooltip: {
                            enabled: true
                        }
                    }
                };

                const chart = new ApexCharts(document.querySelector("#chart"), options);
                chart.render();

                console.log('ApexCharts inicializado:', chart);  // Verifique se o gráfico foi inicializado
            } else {
                console.error('Estrutura de dados inesperada:', data);
            }
        } catch (error) {
            console.error('Error fetching stock data:', error);
        }
    };

    // Call the function to fetch data and render the chart
    fetchDataAndRenderChart();
});
