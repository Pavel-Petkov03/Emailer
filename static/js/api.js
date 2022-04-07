const ROOT = "http://localhost:8000/api"

const urls = {
    folder: "/folder",
    bin: "/bin",
    "filter-emails": "/filter",
    email: "/email"
}


const endpoints = Object.entries(urls).reduce((acc, [key, value]) =>
    Object.assign(acc, {[key]: `${ROOT}${value}`}), {})

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}


async function getData(url, method, data) {
    const response = await axios({
        url,
        method,
        data,
        withCredentials: true,
        headers : {
            "X-CSRFToken" : getCookie("csrftoken")
        }
    })
    return response.data
}


export {
    endpoints,
    getData
}