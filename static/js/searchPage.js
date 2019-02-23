$('document').ready(function() {
	$('.lds-roller').hide();
	$('#noData').hide();

});
$('#searchButton').click(function() {
	$('#chartContainer').hide();
	var val = $('input#searchbox').val();
	if (val != "" && val != null) {

		$('.lds-roller').show();
		$.ajax({
			type : 'POST',
			url : 'result',
			data : {
				param : $('input#searchbox').val(),
				csrfmiddlewaretoken : '{{ csrf_token }}'
			}, //passing some input here
			dataType : 'json',
			success : function(response) {
				$('.lds-roller').hide();
				var listNames = response.nameList;
				var pos = response.positive;
				var neg = response.negative;
				var neu = response.neutral;
				if (pos == 0 && neg == 0 && neu == 0) {

					$('#noData').slideDown();
				} else {

					chart = doughnut(pos, neg, neu);
					 sigmaJSDisplay(listNames);
					$('.lds-roller').hide();
					$('#chartContainer').show();
					chart.render();
				
				}
			}
		});

	}
});
	
function doughnut(pos, neg, neu) {
	var chart = new CanvasJS.Chart("chartContainer", {
		animationEnabled : true,
		title : {
			text : "Sentimental analysis"
		},
		backgroundColor : "#D3D3D3",
		borderColor : "black",
		data : [ {
			type : "doughnut",
			startAngle : 60,
			innerRadius : 75,
			indexLabelFontSize : 17,
			indexLabel : "{label} - #percent%",
			indexLabelFontColor : "black",
			toolTipContent : "<b>{label}:</b> {y} (#percent%)",
			toolTiofontCOlor : 'white',
			dataPoints : [ {
				y : pos,
				label : "Positive",
				color : "rgb(124,252,0)",
				markerBorderColor : "black"

			}, {
				y : neg,
				label : "Negative",
				color : "rgb(250,125,114)",
				markerBorderColor : "black"
			}, {
				y : neu,
				label : "Neutral",
				color : "rgb(135,206,235)",
				markerBorderColor : "black"
			}, ]
		} ]
	});
	return chart
}
function sigmaJSDisplay(listNames) {
	count = listNames.length;
	var g = {
		nodes : [],
		edges : []
	}
	for (i = 1; i <= count; i++) {

		g.nodes.push({
			id : 'n' + i,
			label : listNames[i - 1],
			x : Math.random() + 4,
			y : Math.random() + 4,
			size : 1,
			color : "#00FF00"
		});

	}
	for (i = 1; i <= count; i++) {
		for (j = count; j > i; j--) {
			g.edges.push({
				id : 'e' + i + '' + j,
				source : 'n' + i,
				target : 'n' + j,
				type : 'curve',
				size : 1,
				color : '#FFF'
			});
		}
	}
	s = new sigma({
		graph : g,
		container : 'sigmaChart',
		settings : {

			drawLabels : true
		}
	});
	$('#sigmaChart').show();
	s.refresh();
}