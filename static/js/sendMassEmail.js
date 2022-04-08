import {endpoints, getData} from "./api.js";


function deleteReceiver(ev) {
    ev.preventDefault()
    const id = ev.target.getAttribute("data-id")
    getData(`${endpoints.receiver}/${id}`, "delete").then(data => {
        if (data.statusCode === 204) {
            ev.target.parentNode.parentNode.remove()
        }
    })
}

window.deleteReceiver = deleteReceiver