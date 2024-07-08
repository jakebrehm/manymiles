// Create an object to represent the record timeline
var recordFrequency = {

    // Internal variables
    canvasId: "record-frequency",
    selectId: "record-frequency-period",
    endpoint: "/data/record-frequency",

    // Chart customizations
    title: null,
    xLabel: null,
    yLabel: "Average",

    // Placeholder variables
    chart: null,
    canvas: null,
    select: null,

    // Initialize the object
    initialize() {
        // Get a handle to the canvas that will be used for the visualization
        this.canvas = document.getElementById(this.canvasId);
        // Get a handle to the select that determines how much data to show
        this.select = document.getElementById(this.selectId);
    },

    // Method to pull data from the endpoint
    getData() {
        // Add necessary parameters to the endpoint
        const parameters = {"period": this.select.value};
        const endpointFinal = appendParameters(this.endpoint, parameters);
        // Asynchronously send a GET reqest to fetch the data
        return fetchData(endpointFinal);
    },

    // Create the chart
    createChart() {
        // Fetch the data
        const response = this.getData();

        // Get a reference to this
        var that = this;

        // Create the visualization using the promise
        response.then(function(data) {
            // If there aren't enough values, don't create the visualization
            if (!data["valid"]) {
                return
            }

            // Create the chart
            var ctx = that.canvas.getContext("2d");
            that.chart = new Chart(ctx, {
                type: "bar",
                data: {
                    labels: data["labels"],
                    datasets: [{
                        label: "Average",
                        data: data["averages"],
                        borderWidth: 2,
                        borderColor: cssVariable("--primary"),
                        backgroundColor: hslOpacity(cssVariable("--primary"), 0.15),
                    }],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: that.title !== null,
                            text: that.title,
                            color: cssVariable("--contrast"),
                            font: {
                                size: 20,
                            },
                            align: "start",
                            padding: {
                                bottom: 30,
                            },
                        },
                        legend: {
                            display: false,
                        },
                        tooltip: {
                            callbacks: {
                                label: (context) => {
                                    let i = context.dataIndex;
                                    let average = data["averages"][i];
                                    average = Math.round(average * 100) / 100;
                                    let total = data["counts"][i];
                                    return `Average: ${average}, Total: ${total}`;
                                },
                            },
                        },
                    },
                    scales: {
                        x: {
                            title: {
                                display: that.xLabel !== null,
                                text: that.xLabel,
                                color: cssVariable("--contrast"),
                                font: {
                                    size: 14,
                                },
                            },
                            grid: {
                                color: cssVariable("--muted-border-color"),
                            },
                        },
                        y: {
                            title: {
                                display: that.yLabel !== null,
                                text: that.yLabel,
                                color: cssVariable("--contrast"),
                                font: {
                                    size: 14,
                                },
                            },
                            grid: {
                                color: cssVariable("--muted-border-color"),
                            },
                        },
                    },
                },
            });
        })
    },

    // Destroy the chart
    destroyChart() {
        this.chart.destroy();
    },

    // Update the chart
    updateChart() {
        this.destroyChart();
        this.createChart();
    },

};

// Initialize and create the record timeline
recordFrequency.initialize();
recordFrequency.createChart();