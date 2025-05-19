function identifyColor(value){
    if (value.includes("<django:green>")){
        return "color: green;";     
    } else if (value.includes("<django:yellow>")){ 
        return "color: yellow;";     
    } else if (value.includes("<django:red>")){
        return "color: red;";     
    } else if (value.includes("<django:blue>")){
        return "color: blue;";     
    } else {
        return ""
    }
}