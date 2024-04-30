class Space{
    constructor(){
        this.floor = null;
        this.walls = [null, null, null, null]
    }
}

let selected = [-1, -1, -1] // x, y, side; -1 for none
let room;
let width = 5;
let height = 5;
let size = 100;
let wallSelect = document.getElementById("wallSelect");
let wallTypes = ["wall pressure plate", "panel", "doorway"]
let floorSelect = document.getElementById("floorSelect")
let floorTypes = ["ground pressure plate"]
const canvas = document.getElementById("roomCanvas");
const context = canvas.getContext("2d");
// image natural dimensions = name: [width, height]
const natImages = {"wall pressure plate": [1821, 2048], "doorway": [1821, 2048], "panel": [1821, 2048], "ground pressure plate": [756, 514]}

let descriptions = {
    "wall pressure plate": ": A wall with a recessed section, which will send out a signal when a cube is placed in it", 
    "panel": ": A wall with a small panel that can open up when it recieves a signal, revealing a vertical strip of information",
    "doorway": ": A space through which the robot can move to exit the room",
	"ground pressure plate": ": A floor with a raised area that will send out a signal when an object is placed upon it, or when the robot drives over it"
}

window.addEventListener('DOMContentLoaded', ()=>{
    loadRoom();
    wallSelect.addEventListener("change", ()=>{changeSelected("wall")});
    floorSelect.addEventListener("change", ()=>{changeSelected("floor")});
    setLegend();
    setDropdowns();
    drawRoom();
    document.getElementById("submit").addEventListener("click", ()=>{nextPage()})
    document.getElementById("previous").addEventListener("click", ()=>{prevPage()})
});

function loadRoom(){
    let stringRoom = sessionStorage.getItem("room")
    if(stringRoom !== null){
        room = JSON.parse(stringRoom)
    }else{
        newRoom();
    }
}

function setLegend(){
    legend = document.getElementById("pieces");
	if(wallTypes.length>0)
	    legend.innerHTML += "Wall types:<br/>"
    for(i in wallTypes){
        p = document.createElement("p")
        type = wallTypes[i]
        if(!(type in natImages)){
            type = "default"
        }
        image = document.createElement("img")
        image.height = 50
        image.src = "/static/img/"+type+".png"
        p.append(image)
        p.innerHTML += type.charAt(0).toUpperCase()+type.slice(1)+descriptions[type]+"<br/>"
        legend.append(p)
    }
    if(floorTypes.length>0)
		legend.innerHTML += "Floor types: <br/>"
    for(i in floorTypes){
        p = document.createElement("p")
        type = floorTypes[i]
        if(!(type in natImages)){
            type = "default"
        }
        image = document.createElement("img")
		if(image.height > image.width){
        	image.height = 50
		}else{
			image.width = 50
		}
        image.src = "/static/img/"+type+".png"
        p.append(image)
        p.innerHTML += type.charAt(0).toUpperCase()+type.slice(1)+descriptions[type]+"<br/>"
        legend.append(p)
    }
}

function setDropdowns(){
    floorDrop = floorSelect
    for(i = 0; i<floorTypes.length; i++){
        type = floorTypes[i]
        option = document.createElement("option")
        option.value = type
        option.innerText = type.charAt(0).toUpperCase()+type.slice(1)
        floorDrop.append(option)
    }
    wallDrop = wallSelect
    for(i = 0; i<wallTypes.length; i++){
        type = wallTypes[i]
        option = document.createElement("option")
        option.value = type
        option.innerText = type.charAt(0).toUpperCase()+type.slice(1)
        wallDrop.append(option)
    }
}

function newRoom(){
    room = []
    for(let i = 0; i<height; i++){
        room[i] = []
        for(let j = 0; j<width; j++){
            room[i][j] = new Space();
        }
    }
}

function validateWalls(){
    for(let i = 0; i<height; i++){
        for(let j = 0; j<width; j++){
            if(room[i][j].floor===null){
                room[i][j].walls = [null, null, null, null];
            }else{
                if(i>0){//there is a row north
                    if(room[i-1][j].floor!==null){//if floor to north, no wall
                        room[i][j].walls[0] = null;
                    }else if(room[i][j].walls[0] === null){//if no floor to north, establish as wall
                        room[i][j].walls[0] = "wall"
                    }
                }else if(room[i][j].walls[0] === null){//establish as wall if not already
                    room[i][j].walls[0] = "wall"
                }
                if(i<height-1){//there is a row south
                    if(room[i+1][j].floor!=null){//if floor to south, no wall
                        room[i][j].walls[2] = null;
                    }else if(room[i][j].walls[2]===null){//if no floor to east, establish as wall
                        room[i][j].walls[2] = "wall"
                    }
                }else if(room[i][j].walls[2]===null){//establish as wall if not already
                    room[i][j].walls[2] = "wall"
                }

                if(j>0){//there is a column west
                    if(room[i][j-1].floor!==null){//if floor to west, no wall
                        room[i][j].walls[3] = null;
                    }else if(room[i][j].walls[3] === null){//if no floor to west, establish as wall
                        room[i][j].walls[3] = "wall"
                    }
                }else if(room[i][j].walls[3] === null){//establish as wall if not already
                    room[i][j].walls[3] = "wall"
                }

                if(j<width-1){//there is a column east
                    if(room[i][j+1].floor!==null){//if floor to east, no wall
                        room[i][j].walls[1] = null;
                    }else if(room[i][j].walls[1] === null){//if no floor to east, establish as wall
                        room[i][j].walls[1] = "wall"
                    }
                }else if(room[i][j].walls[1] === null){//establish as wall if not already
                    room[i][j].walls[1] = "wall"
                }
            }   
        }
    }
}

function drawRoom(){
    validateWalls()
    context.clearRect(0,0, canvas.width, canvas.height)
    map = document.getElementById("floorMap")
    wallList = map.children
    while(wallList.length>0){
        wallList[0].remove()
    }
    editList = document.getElementById("floorEdit").children
    while(editList.length > 2){
        editList[2].remove();
    }
    for(let i = 0; i<height; i++){
        for(let j = 0; j<width; j++){
            x = size*(j+1);
            y = size*(i+1);
            interactableFloor(map, j, i)
            if(room[i][j].floor!==null){
                setImage(room[i][j].floor, y, x, y+size, x+size)
                context.beginPath()
                context.rect(x, y, size, size)
                context.stroke();
                if(room[i][j].walls[0]!==null){//top wall
                    let corner1x = x, corner2x = x+size;
                    if(room[i][j].walls[3]!==null){//left wall
                        corner1x = x-(size*0.3);
                    }else if(i>0 && j>0){
                        if(room[i-1][j-1].walls[1]!==null){//top left space has right wall
                            corner1x = x+(size*0.3);
                        }
                    }
                    if(room[i][j].walls[1]!==null){//right wall
                        corner2x = x+(size*1.3);
                    }else if(i>0 && j<width-1){
                        if(room[i-1][j+1].walls[3]!==null){//top right space has left wall
                            corner2x = x+(size*0.7);
                        }
                    }
                    drawQuad(corner1x, y-(size*0.3), x, y, x+size, y, corner2x, y-(size*0.3))
                    setImage(room[i][j].walls[0], y-(size*0.3), Math.max(corner1x, x), y, Math.min(corner2x, x+size))
                    interactableQuad(map, j, i, 0, corner1x, y-(size*0.3), x, y, x+size, y, corner2x, y-(size*0.3))
                }
                if(room[i][j].walls[1]!==null){//right wall
                    let corner1y = y, corner2y = y+size;
                    if(room[i][j].walls[0]!==null){//top wall
                        corner1y = y-(size*0.3);
                    }else if(i>0 && j<width-1){
                        if(room[i-1][j+1].walls[2]!==null){//top right space has bottom wall
                            corner1y = y+(size*0.3);
                        }
                    }
                    if(room[i][j].walls[2]!==null){//bottom wall
                        corner2y = y+(size*1.3);
                    }else if(i<height-1 && j<width-1){
                        if(room[i+1][j+1].walls[0]!==null){//bottom right space has top wall
                            corner2y = y+(size*0.7);
                        }
                    }
                    drawQuad(x+size, y+size, x+size, y, x+(size*1.3), corner1y, x+(size*1.3), corner2y)
                    setImage(room[i][j].walls[1], Math.max(corner1y, y), x+size, Math.min(corner2y, y+size), x+(size*1.3))
                    interactableQuad(map, j, i, 1, x+size, y+size, x+size, y, x+(size*1.3), corner1y, x+(size*1.3), corner2y)
                }
                if(room[i][j].walls[2]!==null){//bottom wall
                    let corner1x = x, corner2x = x+size;
                    if(room[i][j].walls[3]!==null){//left wall
                        corner1x = x-(size*0.3);
                    }else if(i<height-1 && j>0){
                        if(room[i+1][j-1].walls[1]!==null){//bottom left space has right wall
                            corner1x = x+(size*0.3);
                        }
                    }
                    if(room[i][j].walls[1]!==null){//right wall
                        corner2x = x+(size*1.3);
                    }else if(i<height-1 && j<width-1){
                        if(room[i+1][j+1].walls[3]!==null){//bottom right space has left wall
                            corner2x = x+(size*0.7);
                        }
                    }
                    drawQuad(corner1x, y+(size*1.3), x, y+size, x+size, y+size, corner2x, y+(size*1.3))
                    setImage(room[i][j].walls[2], y+size, Math.max(corner1x, x), y+(size*1.3), Math.min(corner2x, x+size))
                    interactableQuad(map, j, i, 2, corner1x, y+(size*1.3), x, y+size, x+size, y+size, corner2x, y+(size*1.3))
                }
                if(room[i][j].walls[3]!==null){//left wall
                    let corner1y = y, corner2y = y+size;
                    if(room[i][j].walls[0]!==null){//top wall
                        corner1y = y-(size*0.3);
                    }else if(i>0 && j>0){
                        if(room[i-1][j-1].walls[2]!==null){//top left space has bottom wall
                            corner1y = y+(size*0.3);
                        }
                    }
                    if(room[i][j].walls[2]!==null){//bottom wall
                        corner2y = y+(size*1.3);
                    }else if(i<height-1 && j>0){
                        if(room[i+1][j-1].walls[0]!==null){//bottom left space has top wall
                            corner2y = y+(size*0.7);
                        }
                    }
                    drawQuad(x, y+size, x, y, x-(size*0.3), corner1y, x-(size*0.3), corner2y)
                    setImage(room[i][j].walls[3], Math.max(corner1y, y), x-(size*0.3), Math.min(corner2y, y+size), x)
                    interactableQuad(map, j, i, 3, x, y+size, x, y, x-(size*0.3), corner1y, x-(size*0.3), corner2y)
                }
            }
        }
    }
}

function drawQuad(x1, y1, x2, y2, x3, y3, x4, y4){
    context.beginPath();
    context.moveTo(x1, y1);
    context.lineTo(x2, y2);
    context.lineTo(x3, y3);
    context.lineTo(x4, y4);
    context.lineTo(x1, y1);
    context.stroke();
}

function setImage(name, top, left, bottom, right){
    if(name !== "wall" && name !== "floor"){
        if(!(name in natImages)){
            name = "default"
        }
        let container = document.getElementById("floorEdit")
        let image = document.createElement("img")
        image.src = "/static/img/"+name+".png"
		let imgWidth = natImages[name][0], imgHeight = natImages[name][1];
        if(bottom-top<right-left){
            image.style.height = bottom-top
            image.style.left = ((right+left)/2)-((bottom-top)/imgHeight*imgWidth/2)
            image.style.top = top
        }else if(bottom-top>right-left){
            image.style.width = right-left
            image.style.left = left
            image.style.top = ((bottom+top)/2)-((right-left)/imgWidth*imgHeight/2)
        }else{
			if(imgWidth<=imgHeight){
				image.style.height = bottom-top;
				image.style.top = top;
				image.style.left = ((right+left)/2)-((bottom-top)/imgHeight*imgWidth/2);
			}else{
				image.style.width = right-left;
				image.style.top = ((bottom+top)/2)-((right-left)/imgWidth*imgHeight/2);
				image.style.left = left;
			}
		}
        container.append(image)
    }
}

function interactableFloor(map, coordX, coordY){
    let top = (coordY+1)*size, bottom = (coordY+2)*size, left = (coordX+1)*size, right = (coordX+2)*size
    floor = document.createElement("area")
    floor.shape = "rect"
    if(coordY>0){
        if(room[coordY-1][coordX].walls[2]!==null){ top+= size*0.3 }
    }
    if(coordY<height-1){
        if(room[coordY+1][coordX].walls[0]!==null){ bottom += size*-0.3 }
    }
    if(coordX>0){
        if(room[coordY][coordX-1].walls[1]!==null){ left += size*0.3 }
    }
    if(coordX<width-1){
        if(room[coordY][coordX+1].walls[3]!==null){ right += size*-0.3 }
    }
    floor.coords = left+","+top+","+right+","+bottom
    floor.addEventListener("click", ()=>{floorClick(coordX, coordY)})
    floor.addEventListener("contextmenu", (e)=>{
        e.preventDefault()
        selected = [coordX, coordY, -1]
        setSelection(floorSelect, room[coordY][coordX].floor)
        menu = document.getElementById("floorDropdown")
        openMenu(menu, e.clientX, e.clientY)
    })
    map.append(floor)
}

function openMenu(menu, x, y){
    if(menu.id == "wallDropdown"){ // hide the other when it opens
        document.getElementById("floorDropdown").style.visibility = "hidden"
    }else{
        document.getElementById("wallDropdown").style.visibility = "hidden"
    }
    if(room[selected[1]][selected[0]].floor !== null){
        containerStyle = window.getComputedStyle(document.getElementById("floorEdit"))
        menu.style.left = (x - trimPX(containerStyle.left))+"px";
        menu.style.top = (y - trimPX(containerStyle.top))+"px";
        if(menu.style.visibility =="hidden" || menu.style.visibility ==""){
            document.body.addEventListener("click", (e) => {clickOff(menu, e)}, {once: true})
            menu.style.visibility = "visible"
        }
    }
}

function clickOff(element, mouse){
    computed = window.getComputedStyle(element)
    containerStyle = window.getComputedStyle(document.getElementById("floorEdit"))
    let top = trimPX(computed.top)+trimPX(containerStyle.top)
    let left = trimPX(computed.left)+trimPX(containerStyle.left)
    if(mouse.clientX<left || mouse.clientX>left+trimPX(computed.width)
        || mouse.clientY<top || mouse.clientY>top+trimPX(computed.height)){
        element.style.visibility = "hidden"
    }else{
        document.body.addEventListener("click", (e) => {clickOff(menu, e)}, {once: true})
    }
}

function trimPX(string){
    return parseInt(string.substring(0, string.length-2))
}

function floorClick(x, y){
    if(room[y][x].floor===null){
        room[y][x].floor = "floor"
    }else{
        selected = [x, y, -1]
        removeSelectedFloor()
    }
    drawRoom()
}

function removeSelectedFloor(){
    room[selected[1]][selected[0]].floor = null
    document.getElementById("floorDropdown").style.visibility = "hidden"
    drawRoom()
}

function changeSelected(type){
    if(type=="wall"){
        room[selected[1]][selected[0]].walls[selected[2]] = wallSelect.value;
    }else{
        room[selected[1]][selected[0]].floor = floorSelect.value;
    }
    drawRoom()
}

sides =  ["top", "right", "bottom", "left"]
function interactableQuad(map, parentX, parentY, side, x1, y1, x2, y2, x3, y3, x4, y4){
    wall = document.createElement("area")
    wall.shape = "poly"
    wall.coords = x1+","+y1+","+x2+","+y2+","+x3+","+y3+","+x4+","+y4
    wall.addEventListener("contextmenu", (e)=>{
        e.preventDefault();
        wallClick(parentX, parentY, side, e)
    })
    map.append(wall)
}

function wallClick(x, y, side, event){
    selected = [x, y, side]
    setSelection(wallSelect, room[y][x].walls[side])
    menu = document.getElementById("wallDropdown")
    openMenu(menu, event.clientX, event.clientY)
}

function setSelection(dropdown, value){
    if(value==null){ return; }
    for(var i, j= 0; i = dropdown.options[j]; j++){
        if(i.value == value){
            dropdown.selectedIndex = j;
            return;
        }
    }
}

function prevPage(){
    saveRoom();
    // window.location.replace('')
}

function saveRoom(){
    let stringRoom = JSON.stringify(room)
    sessionStorage.setItem("room", stringRoom)
}