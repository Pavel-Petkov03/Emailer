const ROOT = "http://localhost:8000/api"


const endpoints = {
    folder: "/folder",
    bin: "/bin",

}


// These functions will be used to interact with django api folder
function getCookie(name) {
    const value = `; ${document.cookie}`;
    let parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function getData(path) {
    let url = `${ROOT}` + path
    let cookieString = `csrftoken=${getCookie("csrftoken")}; sessionid=${getCookie("sessionid")}`
    let response = await fetch(url, {
        method: "get",
        headers: {
            "Access-Control-Allow-Origin" : "http://localhost:8000/",
            "content-type": "application/json",
            "Cookie": cookieString,
        }
    })
    return await response.json()
}

export {
    endpoints,
    getData
}