////////// On définit un event listener sur les inputfields qui servent à la recherche de produits //////////
function process()
{
    // Si l'event se fait au niveau de l'inputfield du header, on définit la valeur de la variable url
    if ( document.getElementById("productRequestHeader").value ) {
    var url = "/result/?query=" + document.getElementById("productRequestHeader").value;
    }

    // Même démarche s'il se déclare au niveau de l'inputfield d'index.html
    else {
    var url = "/result/?query=" + document.getElementById("productRequestIndex").value;
    }

// Et on définit la valeur de l'url d'après celle de la variable url avec la méthode location.href
location.href = url;
return false;
}