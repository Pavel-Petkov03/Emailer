const ROOT = "http://localhost:8000/api"

const endpoints = {
    folder: "/folder",
    bin: "/bin",
    "filter-emails": "/filter"
}


async function getData(url, method, data) {
     const response = await axios({
        url : `${ROOT}${url}`,
        method,
        data,
        withCredentials : true
    })
    return response.data
}


export {
    endpoints,
    getData
}