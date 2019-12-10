window.onload = function () {
    $.ajax({
        url: '/getListData',
        type: 'GET',
        success: function (data) {
            var data_obj = JSON.parse(data)
            /*
            * The parameter of Year scatter
            */
            var year_list = {
                mode: 'markers',
                x: Object.keys(data_obj[0]),
                y: Object.values(data_obj[0]),
                type: 'scatter',
                marker: {
                    color: 'rgba(93,109,196,0.95)',

                    symbol: 'circle',
                    size: 16
                }
            };
            /*
            * The parameter of Region pie
            */
            var region_list = [{
                values: Object.values(data_obj[1]),
                labels: Object.keys(data_obj[1]),
                type: 'pie',
                title: 'Region'
            }];

            var region_layout = {
                height: 500,
                width: 720
            };

            /*
            * The parameter of Species pie
            *
            * */
            var species_list = [{
                values: Object.values(data_obj[2]),
                labels: Object.keys(data_obj[2]),
                type: 'pie',
                title: 'Species',
            }];
            var species_layout = {
                height: 500,
                width: 720
            };

            Plotly.newPlot('Year', [year_list]);
            Plotly.newPlot('Region', region_list, region_layout);
            Plotly.newPlot('Species', species_list, species_layout);


            /*
            * Filtrate
            * */
            for (var y in data_obj[0]) {
                $('#Filtrate .Year').append('<option>' + y.toString() + '</option>')
            }
            for (var y in data_obj[1]) {
                $('#Filtrate .Region').append('<option>' + y.toString() + '</option>')
            }
            for (var y in data_obj[2]) {
                $('#Filtrate .Species').append('<option>' + y.toString() + '</option>')
            }
        },
    })
    //Method for loading data into a data-table
    var init_table = function (Filter = ['', '', '', '']) {
        $.ajax({
            url: '/getLogData',
            type: 'POST',
            data: {
                data: JSON.stringify(
                    Filter
                ),
            },
            success: function (data) {

                $('#DataTable').innerHTML = ''

                var data_obj = JSON.parse(data)
                var headers = ['Year', 'Quarter', 'Region', 'Species', 'Grade', 'Pond_Value', 'Number_of_Quotes']
                var new_data = []

                for (var h = 0; h < 7; h++) {
                    new_data[h] = []
                }

                for (var r in data_obj) {
                    for (var h = 0; h < 7; h++) {
                        new_data[h].push(data_obj[r][headers[h]])
                    }
                }
                var table_data = [{
                    type: 'table',
                    header: {
                        values: headers,
                        align: "center",
                        line: {width: 1, color: 'black'},
                        fill: {color: "grey"},
                    },
                    cells: {
                        values: new_data,
                        align: "center",
                        line: {color: "black", width: 1},
                    }
                }]

                Plotly.plot('DataTable', table_data);
            }
        })
    }
    //loads data
    init_table()

    //Listen for filter button events
    $('#Filtrate input').click(function () {
        var Filter = ['', '', '', '']
        //These are the options selected
        if ($('#Filtrate .Year').val())
            Filter[0] = $('#Filtrate .Year').val()
        if ($('#Filtrate .Region').val())
            Filter[1] = $('#Filtrate .Region').val()
        if ($('#Filtrate .Species').val())
            Filter[2] = $('#Filtrate .Species').val()
        if ($('#Filtrate .Limit').val())
            Filter[3] = $('#Filtrate .Limit').val()
        init_table(Filter)
    })
}