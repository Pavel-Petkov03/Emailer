const ROOT = "http://localhost:8000/api"


const endpoints = {
    folder: "/folder",
    bin: "/bin",
    "filter-emails" : "/filter"
}


// These functions will be used to interact with django api folder
function getCookie(name) {
    const value = `; ${document.cookie}`;
    let parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function getData(path, method ,body) {
    let url = `${ROOT}` + path
    const csrfToken = getCookie("csrftoken")
    const sessionId = getCookie("sessionid")
    let cookieString = `csrftoken=${csrfToken}; sessionid=${sessionId}`

    let context = {
        method,
        headers: {
            "content-type": "application/json",
            "Cookie": cookieString,
            "X-CSRFToken" : csrfToken
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