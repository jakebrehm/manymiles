// Create an object to represent the record timeline
var recordTimeline = {

    // Internal variables
    canvasId: "record-timeline",
    selectId: "record-timeline-period",
    endpoint: "/data/record-timeline",

    // Chart customizations
    title: null,

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
        const parameters = {"period": this.timePeriod};
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
                type: "line",
                data: {
                    labels: data["labels"],
                    datasets: [{
                            label: "Mileage",
                            data: data["values"],
                            fill: false,
                            borderColor: cssVariable("--primary"),
                            lineTension: 0.1
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
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: "Date",
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
                                display: true,
                                text: "Mileage",
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

    // Update the values in the select
    updateSelectValues() {
        this.select;
    },

    // Get the selected time period
    get timePeriod() {
        return this.select.value;
    },

};

// Initialize and create the record timeline
recordTimeline.initialize();
recordTimeline.createChart();