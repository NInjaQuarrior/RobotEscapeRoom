//js file that every page uses
//currently just loading in themes
let linkLocation = -1;
let imageFolder = "light";

function loadCSS(){
    const theme = localStorage.getItem("theme");
    let themeString;
    if(theme !== null){
        themeString = "/static/css/themes/"+theme+"Theme.css";
    }else{
        themeString = "/static/css/themes/darkTheme.css"
    }
    if(linkLocation===-1){
        linkLocation = document.head.childElementCount;
        let link = document.createElement("link");
        link.type = "text/css";
        link.rel = "stylesheet";
        link.href = themeString;
        document.head.append(link);
    }else{
        let link = document.head.children[linkLocation];
        link.href = themeString;
    }
    getImageType();
}

function getImageType(){
    if(linkLocation !== -1){
        imageFolder = getComputedStyle(document.documentElement).getPropertyValue("--imageBrightness");
    }
}

function changeTheme(name){
    localStorage.setItem("theme", name);
    loadCSS();
    updateButtons();
}

loadCSS();