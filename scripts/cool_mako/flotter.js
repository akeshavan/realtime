// flotter.js

$(function () {
    var options = {
        lines: { show: true },
	legend: { position: 'nw' }
    };
    data1 = [];
    data2 = [];
    data3 = [];
    data4 = [];
    data5 = [];
    data6 = [];
    function onDataReceived1(jsondata) {
        data1.push(jsondata);
        $.plot($('#rtgraph1'), data1, options);   
	var jlen = jsondata.data.length
	$('#rtcaption1').append('<strong>' + jsondata.label + '</strong>: ' + jlen + ' TRs. ');
    }
    function onDataReceived2(jsondata) {
        data2.push(jsondata);
        $.plot($('#rtgraph2'), data2, options);   
	var jlen = jsondata.data.length
	$('#rtcaption2').append('<strong>' + jsondata.label + '</strong>: ' + jlen + ' TRs. ');
    }
    function onDataReceived3(jsondata) {
        data3.push(jsondata);
        $.plot($('#rtgraph3'), data3, options);   
	var jlen = jsondata.data.length
	$('#rtcaption3').append('<strong>' + jsondata.label + '</strong>: ' + jlen + ' TRs. ');
    }
    function onDataReceived4(jsondata) {
        data4.push(jsondata);
        $.plot($('#rtgraph4'), data4, options);   
	var jlen = jsondata.data.length
	$('#rtcaption4').append('<strong>' + jsondata.label + '</strong>: ' + jlen + ' TRs. ');
    }
    function onDataReceived5(jsondata) {
        data5.push(jsondata);
        $.plot($('#rtgraph5'), data5, options);   
	var jlen = jsondata.data.length
	$('#rtcaption5').append('<strong>' + jsondata.label + '</strong>: ' + jlen + ' TRs. ');
    }
    function onDataReceived6(jsondata) {
        data6.push(jsondata);
        $.plot($('#rtgraph6'), data6, options);   
	var jlen = jsondata.data.length
	$('#rtcaption6').append('<strong>' + jsondata.label + '</strong>: ' + jlen + ' TRs. ');
    }

    $(function () {
        // reset data
        data = [];
	alreadyFetched = {'active': 0, 'reference':0};
        $.plot($('#rtgraph6'), data, options);

        var iteration = 0;
	latest = {'active': {}, 'reference': {}}
        function fetchData() {
            ++iteration;
            function onDataReceived(series) {
                // we get all the data in one go, if we only got partial data, we could merge it with what we already got
		var jlen = series.data.length
		if (jlen > alreadyFetched[series.label]) {
		    alreadyFetched[series.label] = jlen;
		    latest[series.label] = series;
		    $('#rtcaption6').text(jlen + ' TRs.');
		}
                $.plot($("#rtgraph6"), [latest['active'], latest['reference']], options);
            }        
	    $.getJSON('subjects/pilot17/session1/data/run006_active.json',{}, onDataReceived);
	    $.getJSON('subjects/pilot17/session1/data/run006_reference.json',{}, onDataReceived);

            if (iteration < 70)
                setTimeout(fetchData, 5000);
            else {
                data = [];
            }
        }
	setTimeout(fetchData, 1000);
    });
    $.getJSON('subjects/pilot17/session1/data/run001_active.json',{}, onDataReceived1);
    $.getJSON('subjects/pilot17/session1/data/run001_reference.json',{}, onDataReceived1);
    $.getJSON('subjects/pilot17/session1/data/run002_active.json',{}, onDataReceived2);
    $.getJSON('subjects/pilot17/session1/data/run002_reference.json',{}, onDataReceived2);
    $.getJSON('subjects/pilot17/session1/data/run003_active.json',{}, onDataReceived3);
    $.getJSON('subjects/pilot17/session1/data/run003_reference.json',{}, onDataReceived3);
    $.getJSON('subjects/pilot17/session1/data/run004_active.json',{}, onDataReceived4);
    $.getJSON('subjects/pilot17/session1/data/run004_reference.json',{}, onDataReceived4);
    $.getJSON('subjects/pilot17/session1/data/run005_active.json',{}, onDataReceived5);
    $.getJSON('subjects/pilot17/session1/data/run005_reference.json',{}, onDataReceived5);
    $.getJSON('subjects/pilot17/session1/data/run006_active.json',{}, onDataReceived6);
    $.getJSON('subjects/pilot17/session1/data/run006_reference.json',{}, onDataReceived6);
});


