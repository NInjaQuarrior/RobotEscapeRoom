//[id name, page name, image name]
buttons = [["home", "main", "Home"], ["lock", "hint", "Hint"], ["settings", "settings", "Settings"], ["info", "manual", "Info"]]
// omitted: ["progress", "progress", "Progress"]

document.addEventListener("DOMContentLoaded", () => {
    buttons.forEach((element)=>{
        document.body.innerHTML += "<button class='sidebarButton' type='button' id='"+element[0]+"Button' onclick='window.location=&quot;/"+element[1]+"&quot;'></button>"
        //document.body.innerHTML += "<button class='sidebarButton' type='button' id='"+element[0]+"Button'> <img src='static/Images/"+imageFolder+"/"+element[2]+".png'></button>"
        //document.getElementById(element[0]+"Button").onclick = function(){window.location = "{{ url_for("+element[1]+")}}"};
    });
    updateButtons();
});

function updateButtons(){
    console.log("Image theme: "+imageFolder)
    buttons.forEach((element)=>{
        let image = "<img src='static/Images/"+imageFolder+"/"+element[2]+".png'></img>"
        let button = document.getElementById(element[0]+"Button");
        button.innerHTML = `${image}`;
    })
}
