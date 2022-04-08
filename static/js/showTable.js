import {endpoints, getData} from "./api.js";

const i = document.createElement("i")
i.className = "fa fa-solid fa-filter"


const globalDeleteButton = document.createElement("button")
globalDeleteButton.textContent = "Delete Email"
globalDeleteButton.id = "delete-button"



async function mainTableLoader(flag) {
    let filter = localStorage.getItem("filter") || ""
    const endpointString = `${endpoints.folder}?kwarg=${filter}&isbin=${flag}`
    await loadRows(endpointString)
    let headerTrs = document.querySelectorAll("thead tr th")
    Array.from(headerTrs).forEach(el => {
        if (el.textContent.toLowerCase() === localStorage.getItem("filter")) {
            el.prepend(i)
        }
        el.addEventListener("click", filterEvent.bind(this, flag))
    })
}

function deleteRowEventListener(id, event) {
    event.preventDefault()
    event.stopPropagation()

    getData(`${endpoints.email}/${id}?place=${retrieveLocation()}`, "delete", null).then(res => {
        event.target.parentNode.parentNode.remove()
    })
}


function retrieveLocation(){
    const url = window.location.href.split("/")
    return url[url.length-1]
}


function createDeleteButton(id, event){
    event.preventDefault()
    globalDeleteButton.addEventListener("click", deleteRowEventListener.bind(this, id))
    event.target.appendChild(globalDeleteButton)
}


async function loadRows(url) {
    let data = await getData(url, "get")
    let tbody = document.querySelector("tbody")
    tbody.innerText = ""
    data.forEach(el => {
        let {id, ...state} = el
        let tr = document.createElement("tr")
        tr.className = "clickable-row"
        tr.addEventListener("click", trEventListener)
        tr.setAttribute("data-href", id)
        Object.values(state).forEach(value => {
            let td = document.createElement("td")
            td.textContent = value
            td.addEventListener("contextmenu", createDeleteButton.bind(this, id))
            tr.appendChild(td)
        })
        tbody.appendChild(tr)
    })
}

function trEventListener(ev) {
    window.location.href = window.location.href + "/" + ev.target.parentNode.getAttribute("data-href")
}


async function filterEvent(flag, ev) {
    ev.target.prepend(i)
    const loweredFilter = ev.target.textContent.toLowerCase()
    localStorage.setItem("filter", loweredFilter)
    const endpointString = `${endpoints.folder}?kwarg=${loweredFilter}&isbin=${flag}`
    await loadRows(endpointString)
}

export {
    mainTableLoader
}