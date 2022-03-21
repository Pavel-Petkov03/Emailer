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

async function getData(path, body) {
    let url = `${ROOT}` + path
    let cookieString = `csrftoken=${getCookie("csrftoken")}; sessionid=${getCookie("sessionid")}`

    let context = {
        method: "get",
        headers: {
            "content-type": "application/json",
            "Cookie": cookieString,
        }
    }
    if (body) {
        Object.assign(context, {body: JSON.stringify(body)})
    }
    let response = await fetch(url, context)
    return await response.json()
}


export {
    endpoints,
    getData
}