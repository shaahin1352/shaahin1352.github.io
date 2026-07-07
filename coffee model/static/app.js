async function runModel() {

    const roomTemp = document.getElementById("roomTemp").value;
    const adjust = document.getElementById("adjust").value;

    const url = `/run?room_temp=${roomTemp}&adjust=${adjust}`;

    console.log(url);

    const response = await fetch(url);

    const data = await response.json();

    let x = [];
    let y = [];

    data.forEach(item => {
        x.push(item.time);
        y.push(item["coffee temp"]);
    });

    Plotly.newPlot("graph", [{
        x: x,
        y: y,
        mode: "lines",
        type: "scatter"
    }]);

}