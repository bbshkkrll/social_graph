let box = document.getElementsByClassName('box')[0];
let svg = d3.select("svg.graph"), width = box.clientWidth, height = box.clientHeight;

let visible = false;

const color_male = '#0062AA';
const color_female = '#B40081';

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
d3.json("https://vk-social-graph.herokuapp.com/data", function (error, graph) {
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
        .attr("r", 11)
        .attr("fill", function (d) {
            if (d.group > 1)
                return color_male;
            return color_female;
        })
        .on("click", function (d) {
            click(d);
        })
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

    if (!visible) {
        visible = !visible;
        d3.selectAll("line").transition().duration(500)
            .style("opacity", function (o) {
                return o.source === d || o.target === d ? 1 : 0;
            });
        d3.selectAll("circle").transition().duration(500)
            .style("opacity", function (o) {
                return neighboring(d, o) ? 1 : 0;
            });
    } else {
        visible = !visible;
        d3.selectAll("line").transition().duration(500)
            .style("opacity", 1);
        d3.selectAll("circle").transition().duration(500)
            .style("opacity", 1);
    }
}


function neighboring(a, b) {
    return a.index === b.index || linkedByIndex[a.index + "," + b.index];
}

function resize() {
    let box = document.getElementsByClassName('box')[0];
    simulation.force('center', d3.forceCenter(box.clientWidth / 2, box.clientHeight / 2));
}

window.addEventListener('resize', resize);
