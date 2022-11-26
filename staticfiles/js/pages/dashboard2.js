//[Dashboard Javascript]

//Project:	Specie Admin
//Primary use:   Used only for the main dashboard (index.html)


$(function () {

  'use strict';
	if ($('#webticker-3').length) {   
			$("#webticker-3").webTicker({
				height:'auto', 
				duplicate:true, 
				startEmpty:false, 
				rssfrequency:5
			});
		}
	
	//-----amchart3
var chart = AmCharts.makeChart( "chartdiv3", {
  "type": "gauge",
  "theme": "black",
  "startDuration": 0.3,
  "marginTop": 25,
  "marginBottom": 5,
  "axes": [ {
    "axisAlpha": 0.3,
    "endAngle": 360,
    "endValue": 12,
    "minorTickInterval": 0.2,
    "showFirstLabel": false,
    "startAngle": 0,
    "axisThickness": 1,
    "valueInterval": 1
  } ],
  "arrows": [ {
    "radius": "50%",
    "innerRadius": 0,
    "clockWiseOnly": true,
    "nailRadius": 10,
    "nailAlpha": 1
  }, {
    "nailRadius": 0,
    "radius": "80%",
    "startWidth": 6,
    "innerRadius": 0,
    "clockWiseOnly": true
  }, {
    "color": "#3e47ee",
    "nailRadius": 4,
    "startWidth": 3,
    "innerRadius": 0,
    "clockWiseOnly": true,
    "nailAlpha": 1
  } ],
  "export": {
    "enabled": true
  }
} );

// update each second
setInterval( updateClock, 1000 );

// update clock
function updateClock() {
  if(chart.arrows.length > 0){
    // get current date
    var date = new Date();
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var seconds = date.getSeconds();

    if(chart.arrows[ 0 ].setValue){
      // set hours
      chart.arrows[ 0 ].setValue( hours + minutes / 60 );
      // set minutes
      chart.arrows[ 1 ].setValue( 12 * ( minutes + seconds / 60 ) / 60 );
      // set seconds
      chart.arrows[ 2 ].setValue( 12 * date.getSeconds() / 60 );
      }
  }
}	
	
	
}); // End of use strict



	//-----amchart
//----------------chartdiv21

var chartData = [];
generateChartData();

function generateChartData() {
  var firstDate = new Date( 2022, 0, 1 );
  firstDate.setDate( firstDate.getDate() - 500 );
  firstDate.setHours( 0, 0, 0, 0 );

  for ( var i = 0; i < 500; i++ ) {
    var newDate = new Date( firstDate );
    newDate.setDate( newDate.getDate() + i );

    var a = Math.round( Math.random() * ( 40 + i ) ) + 100 + i;
    var b = Math.round( Math.random() * 100000000 );

    chartData.push( {
      "date": newDate,
      "value": a,
      "volume": b
    } );
  }
}

var chart = AmCharts.makeChart( "chartdiv21", {
  "type": "stock",
  "theme": "light",
  "dataSets": [ {
    "color": "#fbae1c",
    "fieldMappings": [ {
      "fromField": "value",
      "toField": "value"
    }, {
      "fromField": "volume",
      "toField": "volume"
    } ],
    "dataProvider": chartData,
    "categoryField": "date",
    // EVENTS
    "stockEvents": [ {
      "date": new Date( 2020, 8, 19 ),
      "type": "sign",
      "backgroundColor": "#fc00ff",
      "graph": "g1",
      "text": "S",
      "description": "This is description of an event"
    }, {
      "date": new Date( 2020, 10, 19 ),
      "type": "flag",
      "backgroundColor": "#FFFFFF",
      "backgroundAlpha": 0.5,
      "graph": "g1",
      "text": "F",
      "description": "Some longer\ntext can also\n be added"
    }, {
      "date": new Date( 2020, 11, 10 ),
      "showOnAxis": true,
      "backgroundColor": "#85CDE6",
      "type": "pin",
      "text": "X",
      "graph": "g1",
      "description": "This is description of an event"
    }, {
      "date": new Date( 2020, 11, 26 ),
      "showOnAxis": true,
      "backgroundColor": "#85CDE6",
      "type": "pin",
      "text": "Z",
      "graph": "g1",
      "description": "This is description of an event"
    }, {
      "date": new Date( 2021, 0, 3 ),
      "type": "sign",
      "backgroundColor": "#85CDE6",
      "graph": "g1",
      "text": "U",
      "description": "This is description of an event"
    }, {
      "date": new Date( 2021, 1, 6 ),
      "type": "sign",
      "graph": "g1",
      "text": "D",
      "description": "This is description of an event"
    }, {
      "date": new Date( 2021, 3, 5 ),
      "type": "sign",
      "graph": "g1",
      "text": "L",
      "description": "This is description of an event"
    }, {
      "date": new Date( 2021, 3, 5 ),
      "type": "sign",
      "graph": "g1",
      "text": "R",
      "description": "This is description of an event"
    }, {
      "date": new Date( 2021, 5, 15 ),
      "type": "arrowUp",
      "backgroundColor": "#00CC00",
      "graph": "g1",
      "description": "This is description of an event"
    }, {
      "date": new Date( 2021, 6, 25 ),
      "type": "arrowDown",
      "backgroundColor": "#CC0000",
      "graph": "g1",
      "description": "This is description of an event"
    }, {
      "date": new Date( 2021, 8, 1 ),
      "type": "text",
      "graph": "g1",
      "text": "Longer text can\nalso be displayed",
      "description": "This is description of an event"
    } ]
  } ],


  "panels": [ {
    "title": "Value",
    "stockGraphs": [ {
      "id": "g1",
      "valueField": "value"
    } ],
    "stockLegend": {
      "valueTextRegular": " ",
      "markerType": "none"
    }
  } ],

  "chartScrollbarSettings": {
    "graph": "g1"
  },

  "chartCursorSettings": {
    "valueBalloonsEnabled": true,
    "graphBulletSize": 1,
    "valueLineBalloonEnabled": true,
    "valueLineEnabled": true,
    "valueLineAlpha": 0.5
  },

  "periodSelector": {
    "periods": [ {
      "period": "DD",
      "count": 10,
      "label": "10 days"
    }, {
      "period": "MM",
      "count": 1,
      "label": "1 month"
    }, {
      "period": "YYYY",
      "count": 1,
      "label": "1 year"
    }, {
      "period": "YTD",
      "label": "YTD"
    }, {
      "period": "MAX",
      "label": "MAX"
    } ]
  },


  "panelsSettings": {
    "usePrefixes": true
  },
  "export": {
    "enabled": true
  }
} );


//-----amchart4
var chart = AmCharts.makeChart("chartdiv4", {
    "type": "serial",
    "theme": "black",
    "autoMarginOffset":20,
    "marginRight":20,
    "dataProvider": [{
        "date": "2021-10-01",
        "value": 3,
        "fromValue": 2,
        "toValue": 5
    }, {
        "date": "2021-10-02",
        "value": 5,
        "fromValue": 4,
        "toValue": 6
    }, {
        "date": "2021-10-03",
        "value": 15,
        "fromValue": 12,
        "toValue": 18
    }, {
        "date": "2021-10-04",
        "value": 13,
        "fromValue": 10.4,
        "toValue": 15.6
    }, {
        "date": "2021-10-05",
        "value": 17,
        "fromValue": 13.6,
        "toValue": 20.4
    }, {
        "date": "2021-10-06",
        "value": 15,
        "fromValue": 12,
        "toValue": 18
    }, {
        "date": "2021-10-09",
        "value": 19,
        "fromValue": 15.2,
        "toValue": 22.8
    }, {
        "date": "2021-10-10",
        "value": 21,
        "fromValue": 16.8,
        "toValue": 25.2
    }, {
        "date": "2021-10-11",
        "value": 20,
        "fromValue": 16,
        "toValue": 24
    }, {
        "date": "2021-10-12",
        "value": 20,
        "fromValue": 16,
        "toValue": 24
    }, {
        "date": "2021-10-13",
        "value": 19,
        "fromValue": 15.2,
        "toValue": 22.8
    }, {
        "date": "2021-10-16",
        "value": 25,
        "fromValue": 20,
        "toValue": 30
    }, {
        "date": "2021-10-17",
        "value": 24,
        "fromValue": 19.2,
        "toValue": 28.8
    }, {
        "date": "2021-10-18",
        "value": 26,
        "fromValue": 20.8,
        "toValue": 31.2
    }, {
        "date": "2021-10-19",
        "value": 27,
        "fromValue": 21.6,
        "toValue": 32.4
    }, {
        "date": "2021-10-20",
        "value": 25,
        "fromValue": 20,
        "toValue": 30
    }, {
        "date": "2021-10-23",
        "value": 29,
        "fromValue": 23.2,
        "toValue": 34.8
    }, {
        "date": "2021-10-24",
        "value": 28,
        "fromValue": 22.4,
        "toValue": 33.6
    }, {
        "date": "2021-10-25",
        "value": 30,
        "fromValue": 24,
        "toValue": 36
    }, {
        "date": "2021-10-26",
        "value": 72,
        "fromValue": 57.6,
        "toValue": 86.4
    }, {
        "date": "2021-10-27",
        "value": 43,
        "fromValue": 34.4,
        "toValue": 51.6
    }, {
        "date": "2021-10-30",
        "value": 31,
        "fromValue": 24.8,
        "toValue": 37.2
    }, {
        "date": "2021-11-01",
        "value": 30,
        "fromValue": 24,
        "toValue": 36
    }, {
        "date": "2021-11-02",
        "value": 29,
        "fromValue": 23.2,
        "toValue": 34.8
    }, {
        "date": "2021-11-03",
        "value": 27,
        "fromValue": 21.6,
        "toValue": 32.4
    }, {
        "date": "2021-11-04",
        "value": 26,
        "fromValue": 20.8,
        "toValue": 31.2
    }],
    "valueAxes": [{
        "axisAlpha": 0,
        "position": "left"
    }],
    "graphs": [{
        "id": "fromGraph",
        "lineAlpha": 0,
        "showBalloon": false,
        "valueField": "fromValue",
        "fillAlphas": 0
    }, {
        "fillAlphas": 0.2,
        "fillToGraph": "fromGraph",
        "lineAlpha": 0,
        "showBalloon": false,
        "valueField": "toValue"
    }, {
        "valueField": "value",
        "balloonText":"<div style='margin:10px; text-align:left'><span style='font-size:11px'>allowed: [[fromValue]] - [[toValue]]</span><br><span style='font-size:18px'>Value:[[value]]</span></div>",
        "fillAlphas": 0
    }],
    "chartCursor": {
        "fullWidth": true,
        "cursorAlpha": 0.05,
        "valueLineEnabled":true,
        "valueLineAlpha":0.5,
        "valueLineBalloonEnabled":true
    },
    "dataDateFormat": "YYYY-MM-DD",
    "categoryField": "date",
    "categoryAxis": {
     "position":"top",
        "parseDates": true,
        "axisAlpha": 0,
        "minHorizontalGap": 25,
        "gridAlpha": 0,
        "tickLength": 0,
        "dateFormats": [{
            "period": 'fff',
            "format": 'JJ:NN:SS'
        }, {
            "period": 'ss',
            "format": 'JJ:NN:SS'
        }, {
            "period": 'mm',
            "format": 'JJ:NN'
        }, {
            "period": 'hh',
            "format": 'JJ:NN'
        }, {
            "period": 'DD',
            "format": 'DD'
        }, {
            "period": 'WW',
            "format": 'DD'
        }, {
            "period": 'MM',
            "format": 'MMM'
        }, {
            "period": 'YYYY',
            "format": 'YYYY'
        }]
    },

    "chartScrollbar":{

    },

    "export": {
        "enabled": true
    }
});

chart.addListener("dataUpdated", zoomChart);

function zoomChart(){
    chart.zoomToDates(new Date(2021,9,20, 15), new Date(2021,10,3,12));
}
