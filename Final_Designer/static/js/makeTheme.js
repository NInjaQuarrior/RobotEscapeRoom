function setTheme(){
    //disable custom
    document.getElementById("customCreator").classList.toggle("disabled", true);
    let theme = document.querySelector('input[name="theme"]:checked').value;
    if(theme==="light"){
        document.documentElement.style.setProperty('--bgColor', "white")
        document.documentElement.style.setProperty('--fontColor', "black")
        document.documentElement.style.setProperty('--lowContrast', "grey")
    }else if(theme === "dark"){
        document.documentElement.style.setProperty('--bgColor', "#131231")
        document.documentElement.style.setProperty('--fontColor', "white")
        document.documentElement.style.setProperty('--lowContrast', "black")
    }else{
        //enable custom
        document.getElementById("customCreator").classList.toggle("disabled", false);
        updateCustom();
    }
}

function updateCustom(){
    document.documentElement.style.setProperty('--bgColor', document.getElementById("bgColor").value)
    document.documentElement.style.setProperty('--fontColor', document.getElementById("fontColor").value)
    document.documentElement.style.setProperty('--lowContrast', document.getElementById("lowContrast").value)
}

window.onload = () => {
    loadTheme();
    setTheme();
    document.getElementsByName("theme").forEach(element => {
        element.addEventListener("change", setTheme);
    });
    document.querySelectorAll('input[type=color]').forEach(element => {
        element.addEventListener("input", updateCustom)
    });
};

function loadTheme(){
    let themeString = sessionStorage.getItem("theme")
    if(themeString!== null){
        let theme = JSON.parse(themeString)
        document.getElementById(theme["name"]).checked = true;
        // if custom set the input values
        if(theme["name"] == "custom"){
            document.getElementById("bgColor").value = theme["--bgColor"]
            document.getElementById("fontColor").value = theme["--fontColor"]
            document.getElementById("lowContrast").value = theme["--lowContrast"]
            updateCustom();
        }
    }else{
        theme = {"name": "dark"}
        document.getElementById("dark").checked = true;
    }
}

function saveTheme(){
    let theme = {}
    theme["name"] = document.querySelector('input[name="theme"]:checked').value;
    theme["--bgColor"] = document.documentElement.style.getPropertyValue("--bgColor");
    theme["--fontColor"] = document.documentElement.style.getPropertyValue("--fontColor");
    theme["--lowContrast"] = document.documentElement.style.getPropertyValue("--lowContrast");
    let themeString = JSON.stringify(theme);
    console.log(themeString)
    sessionStorage.setItem("theme", themeString)
}