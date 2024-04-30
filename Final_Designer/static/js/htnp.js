//future plans:
//          click and drag nodes (low)
//          convert to python objects (high: next week)

let main = document.getElementById("main");
let container = d3.select(main).append("svg").attr("width", "100%").attr("height", "100%");
let svgTop = main.getBoundingClientRect().top;
let svgLeft = main.getBoundingClientRect().left;
let nodes = [];
let outputs = ["panel", "doorway"]
let outputTypes = ["None"]
let inputs = ["wall pressure plate", "ground pressure plate"]
let inputTypes = ["None"]
let rowWidth = 3
let nodeHeight = 150
let nodeWidth = 275

//line drawing vars
let isDrawing = false;
let startX, startY, endX, endY;
let tempLine;
let startType, inId, outId;

let room;
let height, width;

window.onload = function(){
    setDropdownLists();
    setupNodes();
	document.getElementById("main").addEventListener("click", (e)=>{
		createDynamicNode(e.clientX, e.clientY);
	})
	document.addEventListener("mousemove", e=>handleMouseMove(e));
}

function setupNodes(){
    nodeString = sessionStorage.getItem("puzzleProgression");
    if(nodeString == null){
        return;
    }
    nodes = JSON.parse(nodeString);

    for(let i = 0; i<nodes.length; i++){
        preGenNodes(nodes[i]);
    }

    for(let i = 0; i<nodes.length; i++){
        for(let j=0; j<nodes[i].Outputs.length; j++){
            let inputBox = document.getElementById(nodes[i].Outputs[j]+"input");
            let outputBox = document.getElementById(nodes[i].id+"output");
            outId = nodes[i].id;
            inId = nodes[i].Outputs[j]
            startDragLine(parseInt(inputBox.style.left)+20, parseInt(inputBox.style.top)+20);
            stopDragLine(parseInt(outputBox.style.left)+20, parseInt(outputBox.style.top)+20, "in");
        }
    }
}

function preGenNodes(node){
    let idInt = parseInt(node.id.replace("node", ""));

    createNodeById(idInt, node);

    let div = document.getElementById(node.id);
    div.getElementsByTagName("p")[0].innerText = node.name;
    let selects = div.getElementsByTagName("select");
    if(node.RoomInput != null){
        selects[0].value = node.RoomInput;
    }
    if(node.RoomOutput != null){
        selects[1].value = node.RoomOutput;
    }
}

function setDropdownLists(){
    let stringRoom = sessionStorage.getItem("room")
    if(stringRoom === null){
        return
    }
    room = JSON.parse(stringRoom)
    height = room.length;
    width = room[0].length;
    let wallCounts = {};
    for(let i = 0; i<height; i++){
        for(let j = 0; j<width; j++){
            if(room[i][j].floor!=null){
                //floors
                if(room[i][j].floor in wallCounts){
                    wallCounts[room[i][j].floor]++;
                }else{
                    wallCounts[room[i][j].floor] = 1;
                }
                //walls
                for(let k=0; k<4; k++){
                    if(room[i][j].walls[k] != null){
                        if(room[i][j].walls[k] in wallCounts){
                            wallCounts[room[i][j].walls[k]]++;
                        }else{
                            wallCounts[room[i][j].walls[k]] = 1;
                        }
                    }
                }
            }
        }
    }
    delete wallCounts["floor"]
    delete wallCounts["wall"]
    var keys = Object.keys(wallCounts);
    for(var i = 0; i<keys.length; i++){
        var split = keys[i].split(" ");
        var reconstitute = ""
        for(let j = 0; j<split.length; j++){
            reconstitute += split[j].charAt(0).toUpperCase() + split[j].slice(1)+" "
        }
        for(let k = 0; k<wallCounts[keys[i]]; k++){
            if(inputs.includes(keys[i])){
                inputTypes.push(reconstitute+(k+1));    
            }else{
                outputTypes.push(reconstitute+(k+1));
            }
        }

    }
}

function createDropdown(element, list){
    for(i = 0; i<list.length; i++){
        type = list[i]
        option = document.createElement("option")
        option.value = type.replaceAll(" ", "");
        option.innerText = type.charAt(0).toUpperCase()+type.slice(1)
        element.append(option)
    }
}

function createDynamicNode(x, y){
	//math find out id
	let id = Math.floor((y-35-svgTop)/nodeHeight)*rowWidth + Math.floor((x-40-svgLeft)/nodeWidth)
	//if id is used, return
	if(document.getElementById("node"+id) != null || id<0){
		return
	}
	let node = createEmptyNode(id);
	nodes.push(node);
	createNodeById(id, node);
}

function createEmptyNode(id){
	const node = {
        "id": "node"+id, "name": "Node "+id, "RoomInput": null, "RoomOutput": null, "Inputs": [], "Outputs":[]
    };
	return node;
}

function createNodeById(id, node){
    //UI:
    //dropdown menu
        //default none
    //click & drag?
    let mainBox = document.createElement("div");
    mainBox.id = "node"+id;
    mainBox.classList.toggle("mainNode", true);
    mainBox.style.left = ((id%rowWidth)*nodeWidth +100)+'px';
    mainBox.style.top = (Math.floor(id/rowWidth)*nodeHeight + 75 ) + 'px';
    mainBox.appendChild(document.createElement("p"));
    mainBox.getElementsByTagName("p")[0].innerText = "Node "+id;
    main.appendChild(mainBox);

    mainBox.addEventListener("contextmenu", (e) => {
        e.preventDefault();
        removeNode(mainBox.id);
    });

    mainBox.addEventListener("dblclick", ()=>{
        updateNode(mainBox.id);
    })

    //dropdowns
    let dropdownIn = document.createElement("select");
    createDropdown(dropdownIn, inputTypes);
    mainBox.appendChild(dropdownIn);
    dropdownIn.addEventListener("change", ()=>{
        //console.log(dropdownIn.value);
        if(dropdownIn.value !== "None"){
            node.RoomInput = dropdownIn.value;
        }else{
            node.RoomInput = null;
        }
    })
    let dropdownOut = document.createElement("select");
    createDropdown(dropdownOut, outputTypes);
    mainBox.appendChild(dropdownOut);
    dropdownOut.addEventListener("change", ()=>{
        //console.log(dropdownOut.value);
        if(dropdownOut.value !== "None"){
            node.RoomOutput = dropdownOut.value;
        }else{
            node.RoomOutput = null;
        }
    })

    //in/output boxes
        //onclick line drag (create child/parent links?)
    let inputBox = document.createElement("div");
    inputBox.id = "node"+id+"input";
    inputBox.classList.toggle("ioBox", true);
    inputBox.style.left = ((id%rowWidth)*nodeWidth +100-40)+'px';
    inputBox.style.top = (Math.floor(id/rowWidth)*nodeHeight + 75+20 ) + 'px';
    main.appendChild(inputBox);

    inputBox.addEventListener("click", (e)=>{
        lineClick(parseInt(inputBox.style.left)+20, parseInt(inputBox.style.top)+20, "in", mainBox.id);
    });

    let outputBox = document.createElement("div");
    outputBox.id = "node"+id+"output";
    outputBox.classList.toggle("ioBox", true);
    outputBox.style.left = ((id%rowWidth)*nodeWidth +100+152)+'px';
    outputBox.style.top = (Math.floor(id/rowWidth)*nodeHeight + 75+20 ) + 'px';
    main.appendChild(outputBox);

    outputBox.addEventListener("click", (e)=>{
        lineClick(parseInt(outputBox.style.left)+20, parseInt(outputBox.style.top)+20, "out", mainBox.id);
    });
}

function removeNode(id){
    for(let i = 0; i<nodes.length; i++){
        if(nodes[i].id == id){ //remove node itself
            nodes.splice(i, 1);
            document.getElementById(id).remove();
            document.getElementById(id+"input").remove();
            document.getElementById(id+"output").remove();
        }else{
            if(nodes[i].Inputs.includes(id)){
                nodes[i].Inputs.splice(nodes[i].Inputs.indexOf(id), 1);
            }
            if(nodes[i].Outputs.includes(id)){
                nodes[i].Outputs.splice(nodes[i].Outputs.indexOf(id), 1);
            }
        }
    }
    let lines = main.getElementsByTagName("line")
    for(let j = lines.length-1; j>=0; j--){
        if(lines[j].getAttribute("connections").includes(id)){
            lines[j].remove();
        }
    }
}

function updateNode(id){
    let newName = prompt("Enter a new Name:", document.getElementById(id).getElementsByTagName("p")[0].innerText);
	if(newName === null) return;
    for(let i = 0; i<nodes.length; i++){
        if(nodes[i].id == id){
            nodes[i].name = newName;
            document.getElementById(id).getElementsByTagName("p")[0].innerHTML = newName;
            break;
        }
    }
}

//Line drawing code

function lineClick(x, y, from, id){
    if(from == "in"){
        inId = id;
    }else{
        outId = id;
    }

    if(isDrawing){
		stopDragLine(x, y, from);
        //tell inID node append(outId) to inputs
        //tell outID node append(inId) to outpus
        for(let i = 0; i<nodes.length; i++){
            if(nodes[i].id === inId){
                nodes[i].Inputs.push(outId);
            }
            if(nodes[i].id === outId){
                nodes[i].Outputs.push(inId);
            }
        }
    }else{
        startType = from;
        startDragLine(x, y);
    }
}

function startDragLine(x, y) {
    isDrawing = true;
    startX = x;
    startY = y;
    tempLine = container.append("line")
        .attr("x1", startX)
        .attr("y1", startY)
        .attr("x2", startX)
        .attr("y2", startY)
        .attr("stroke", "white")
		.attr("stroke-width", "5px");
}

function stopDragLine(x, y, from) {
    isDrawing = false;
    tempLine.remove();

    if(from === startType || inId === outId){
        return;
    }

    endX = x;
    endY = y;
    // Create the final line
    container.append("line")
        .attr("x1", startX)
        .attr("y1", startY)
        .attr("x2", endX)
        .attr("y2", endY)
        .attr("connections", [outId, inId])
        .attr("stroke", "white")
        .attr("stroke-width", "5px");

    let lines = main.getElementsByTagName("line");
    const line = lines[lines.length-1];
    line.addEventListener("contextmenu", (e)=>{e.preventDefault(); removeLine(line.getAttribute("connections"))});
}

// Function to handle mouse move event
function handleMouseMove(event) {
    if (isDrawing) {
        let endX = event.clientX-svgLeft, endY = event.clientY; // Update end position while dragging
        tempLine.attr("x2", endX).attr("y2", endY);
    }
}

function removeLine(connections){
    outId = connections.substring(0, connections.indexOf(","))
    inId = connections.substring(connections.indexOf(",")+1)
    let skip1 = false, skip2 = false;
    for(let i = 0; i<nodes.length; i++){
        if(nodes[i].id === inId){
            nodes[i].Inputs.splice(nodes[i].Inputs.indexOf(outId), 1);
            skip1 = true;
        }
        if(nodes[i].id === outId){
            nodes[i].Outputs.splice(nodes[i].Outputs.indexOf(inId), 1);
            skip2 = true;
        }
        if(skip1 && skip2){
            break;
        }
    }
    let lines = main.getElementsByTagName("line")
    for(let j = lines.length-1; j>=0; j--){
        if(lines[j].getAttribute("connections") === outId+","+inId){
            lines[j].remove();
            break;
        }
    }
}

//TODO send to flask server on page leave (yknow, call before the redirect call on the nav buttons)
function saveProgression(){
    var stringProgression = JSON.stringify(nodes);
    sessionStorage.setItem("puzzleProgression", stringProgression);
}