function checkFileExist(urlToFile) {
    var xhr = new XMLHttpRequest();
    xhr.open('HEAD', urlToFile, false);
    xhr.send();

    if (xhr.status == "404") {
        return false;
    } else {
        return true;
    }
}

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    //return xmlHttp.responseText;
    document.write(xmlHttp.responseText);
}

async function renderSimPics() {

    // Calling function
    // set the path to check
    var result = false;

    // Define a template
    while (result == false) {
        var result = checkFileExist("/static/images/calls.png");
        if (result == true){
            httpGet("/run_simulation");
        }
    }
}
renderSimPics();