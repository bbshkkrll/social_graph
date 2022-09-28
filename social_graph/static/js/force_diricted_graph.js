let divOuter = document.getElementById('outer');
let svg = d3.select("svg.graph"), width = divOuter.clientWidth, height = divOuter.clientHeight;

let color = d3.scaleOrdinal(d3.schemeCategory20);

let simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function (d) {
        return d.id;
    }))
    .force("charge", d3.forceManyBody().strength(-100))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide().radius(function (d) {
        d.value;
    }))
    .force('y', d3.forceY().y(function () {
        return -1;
    }))
    .force('x', d3.forceX().x(function () {
        return -1;
    }));

let filename = getCookie('filename_json');

d3.json(filename, function (error, graph) {
    if (error) throw error;

    let link = svg.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(graph.links)
        .enter().append("line");

    let node = svg.append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(graph.nodes)
        .enter().append("circle")
        .attr("r", 8)
        .attr("fill", function (d) {
            if (d.group > 1)
                return '#8ecae6';
            return '#cf91b5';
        })
        .on("click", click)
        .on('dblclick', r_click)
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));


    node.append("title")
        .text(function (d) {
            return d.name;
        });

    simulation
        .nodes(graph.nodes)
        .on("tick", ticked);

    simulation.force("link")
        .links(graph.links);

    function ticked() {
        link
            .attr("x1", function (d) {
                return d.source.x;
            })
            .attr("y1", function (d) {
                return d.source.y;
            })
            .attr("x2", function (d) {
                return d.target.x;
            })
            .attr("y2", function (d) {
                return d.target.y;
            });

        node
            .attr("cx", function (d) {
                return d.x;
            })
            .attr("cy", function (d) {
                return d.y;
            });
    }


});

function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}


function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;

}

function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;

}

function click(d) {

    d3.selectAll("line").transition().duration(500)
        .style("opacity", function (o) {
            return o.source === d || o.target === d ? 1 : 0;
        });
    d3.selectAll("circle").transition().duration(500)
        .style("opacity", function (o) {
            return neighboring(d, o) ? 1 : 0;
        });
}


function r_click() {
    d3.selectAll("line").transition().duration(500)
        .style("opacity", 1);
    d3.selectAll("circle").transition().duration(500)
        .style("opacity", 1);
}


function neighboring(a, b) {
    return a.index === b.index || linkedByIndex[a.index + "," + b.index];
}

function getCookie(name) {
    let nameEQ = name + "=";
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}