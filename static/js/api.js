const ROOT = "http://localhost:8000/api"


const endpoints = {
    folder: "/folder",
    bin: "/bin",
}

async function getData(path, method , body) {
    let url = `${ROOT}` + path
    let init = {
        method,
        headers: {
            "content-type": "application/json",
        },
    }
    if (body) {
        Object.assign(init, {body})
    }
    console.log(init)
    let response = await fetch(url, init)
    return await response.json()
}

export {
    endpoints,
    getData
}