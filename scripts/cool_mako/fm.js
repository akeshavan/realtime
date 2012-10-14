// flotter.js

$(function () {
    var options = {
        lines: { show: true },
	legend: { position: 'nw' }
    };
    var data1 = {'active': {}, 'reference': {}};
    var data2 = {'active': {}, 'reference': {}};
    var data3 = {'active': {}, 'reference': {}};
    var data4 = {'active': {}, 'reference': {}};
    var data5 = {'active': {}, 'reference': {}};
    var data6 = {'active': {}, 'reference': {}};

    var iteration = 0;
    function fetchData() {
        ++iteration;

	function onDataReceived4(jsondata) {
	    var jlen = jsondata.data.length;
	    data4[jsondata.label] = jsondata;
            $('#rtcaption4').text(jlen + ' TRs.');
            $.plot($('#rtgraph4'), [data4['active'], data4['reference']], options);
	}
	$.getJSON('subjects/pilot17/session1/data/run004_active.json',{}, onDataReceived4);
	$.getJSON('subjects/pilot17/session1/data/run004_reference.json',{}, onDataReceived4);
	function onDataReceived1(jsondata) {
	    var jlen = jsondata.data.length;
	    data1[jsondata.label] = jsondata;
            $('#rtcaption1').text(jlen + ' TRs.');
            $.plot($('#rtgraph1'), [data1['active'], data1['reference']], options);
	}
	$.getJSON('subjects/pilot17/session1/data/run001_active.json',{}, onDataReceived1);
	$.getJSON('subjects/pilot17/session1/data/run001_reference.json',{}, onDataReceived1);
	function onDataReceived2(jsondata) {
	    var jlen = jsondata.data.length;
	    data2[jsondata.label] = jsondata;
            $('#rtcaption2').text(jlen + ' TRs.');
            $.plot($('#rtgraph2'), [data2['active'], data2['reference']], options);
	}
	$.getJSON('subjects/pilot17/session1/data/run002_active.json',{}, onDataReceived2);
	$.getJSON('subjects/pilot17/session1/data/run002_reference.json',{}, onDataReceived2);
	function onDataReceived3(jsondata) {
	    var jlen = jsondata.data.length;
	    data3[jsondata.label] = jsondata;
            $('#rtcaption3').text(jlen + ' TRs.');
            $.plot($('#rtgraph3'), [data3['active'], data3['reference']], options);
	}
	$.getJSON('subjects/pilot17/session1/data/run003_active.json',{}, onDataReceived3);
	$.getJSON('subjects/pilot17/session1/data/run003_reference.json',{}, onDataReceived3);
	function onDataReceived5(jsondata) {
	    var jlen = jsondata.data.length;
	    data5[jsondata.label] = jsondata;
            $('#rtcaption5').text(jlen + ' TRs.');
            $.plot($('#rtgraph5'), [data5['active'], data5['reference']], options);
	}
	$.getJSON('subjects/pilot17/session1/data/run005_active.json',{}, onDataReceived5);
	$.getJSON('subjects/pilot17/session1/data/run005_reference.json',{}, onDataReceived5);
	function onDataReceived6(jsondata) {
	    var jlen = jsondata.data.length;
	    data6[jsondata.label] = jsondata;
            $('#rtcaption6').text(jlen + ' TRs.');
            $.plot($('#rtgraph6'), [data6['active'], data6['reference']], options);
	}
	$.getJSON('subjects/pilot17/session1/data/run006_active.json',{}, onDataReceived6);
	$.getJSON('subjects/pilot17/session1/data/run006_reference.json',{}, onDataReceived6);

    //     if (iteration < 3000)
    //         setTimeout(fetchData, 500);
    }

    $(function() {
	setInterval(fetchData, 1000);
    });

    // setTimeout(fetchData, 500);
});
