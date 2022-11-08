// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.
// If you get an error about "Streamlit" not being defined, that
// means you're missing that file.

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onDataFromPython(event) {
  var myPlot = document.getElementById("plot");

  const data = event.detail;

  spec = JSON.parse(data.args.spec);
  console.log(spec);

  Plotly.newPlot(myPlot, spec);

  // on event, return data to Python
  myPlot.on("plotly_click", (eventData) => {
    const clickedPoints = eventData.points.map((p) => {
      return { x: p.x, y: p.y };
    });
    Streamlit.setComponentValue(clickedPoints);
  });

  // Render iframe with the plot height
  Streamlit.setFrameHeight(document.documentElement.clientHeight);
}

var xVal = spec.length + 1;
var yVal = 20;	
var updateInterval = 1000;
 
var updateChart = function () {
    spec = JSON.parse(data.args.spec);
    console.log(spec);
    Plotly.newPlot(myPlot, spec);
    yVal = yVal +  Math.round(5 + Math.random() *(-5-5));
    spec.push({x: xVal,y: yVal});
    xVal++;
    Plotly.newPlot(myPlot, spec);	
    Streamlit.setFrameHeight(document.documentElement.clientHeight);

    };


    var timeoutId,
    startButton = document.getElementById('submitStartButton'),
    stopButton = document.getElementById('submitStopButton');
  
  function startLiveChart() {
      timeoutId = setInterval(function(){updateChart()}, updateInterval);
    startButton.removeEventListener('click', startLiveChart);
    stopButton.addEventListener('click', stopLiveChart);
  }
  
  function stopLiveChart() {
      clearTimeout(timeoutId);
    stopButton.removeEventListener('click', stopLiveChart);
    startButton.addEventListener('click', startLiveChart);
  }  
  
  startButton.addEventListener('click', startLiveChart);
  
  


// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onDataFromPython);
// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady();