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

function add_to_favorites()
{
    // On récupère l'url de la page courante
    var urlcourante = window.location.href;
    
    // On va mettre en place un process qui va parser l'URL courante et ne conserver que le paramètre ( url du produit )
    var part_to_remove = 0
    for (var i = 0; i < urlcourante.length; i++ ) {
        if (urlcourante.charAt(i) != '=') {
            part_to_remove += 1
        }
        else {
            break
        }
    }

    var url = "/add_product/?url=" + urlcourante.substr(part_to_remove + 1);

    // Et on définit une nouvelle valeur de l'url d'après celle de la variable url avec la méthode location.href
    location.href = url;
    return false;
}

function create_account()
{
    // Si les inputFields ayant pour id mail et userName ne sont pas Null, on construit une URL
    if ( document.getElementById("mail").value && document.getElementById("userName").value) {
    var url = "/create/?username=" + document.getElementById("userName").value + "&email=" + document.getElementById("mail").value;

    // Et on définit la valeur de l'url d'après celle de la variable url avec la méthode location.href
    location.href = url;
    return false;
    }

    // Sinon, on envoie simplement une alerte à l'utilisateur
    else {
    alert("Vous n'avez pas correctement rempli les champs User Name et eMail");
    }

}

function connect_account()
{
    // On va suivre essentiellement la même démarche que pour la fonction create_acount, avec un schéma d'url différent
    if ( document.getElementById("mail").value && document.getElementById("userName").value) {
    var url = "/connect/?username=" + document.getElementById("userName").value + "&email=" + document.getElementById("mail").value;

    location.href = url;
    return false;
    }

    else {
    alert("Vous n'avez pas correctement rempli les champs User Name et eMail");
    }

}