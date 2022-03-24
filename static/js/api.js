const ROOT = "http://localhost:8000/api"


const endpoints = {
    folder: "/folder",
    bin: "/bin",
    "filter-emails" : "/filter"
}


// These functions will be used to interact with django api folder
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function getData(path, method ,body) {
    let url = `${ROOT}` + path

    let context = {
        method,
        headers: {
            "content-type": "application/json",
            "X-CSRFToken" : getCookie("csrftoken"),
            mode : "same-origin"
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