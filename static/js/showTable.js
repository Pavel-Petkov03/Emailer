import {endpoints, getData} from "./api.js";

const i = document.createElement("i")
i.className = "fa fa-solid fa-filter"
window.onload = async () => {
    let filter = localStorage.getItem("filter") || ""
    await loadRows(endpoints.folder + "?kwarg=" + filter)
    let headerTrs = document.querySelectorAll("thead tr th")
    Array.from(headerTrs).forEach(el => {
        if (el.textContent.toLowerCase() === localStorage.getItem("filter")) {
            el.prepend(i)
        }
        el.addEventListener("click", filterEvent)
    })
}


async function loadRows(url) {
    let data = await getData(url, "get'")
    let tbody = document.querySelector("tbody")
    tbody.innerText = ""
    data.forEach(el => {
        let {id , ...state} = el
        let tr = document.createElement("tr")
        tr.className = "clickable-row"
        tr.addEventListener("click", trEventListener)
        tr.setAttribute("data-href", id)
        Object.values(state).forEach(value => {
            let td = document.createElement("td")
            td.textContent = value
            tr.appendChild(td)
        })
        tbody.appendChild(tr)
    })
}

function trEventListener(ev){
    window.location.href = window.location.href + "/" +  ev.target.parentNode.getAttribute("data-href")
}



async function filterEvent(ev) {
    ev.target.prepend(i)
    const loweredFilter = ev.target.textContent.toLowerCase()
    localStorage.setItem("filter", loweredFilter)
    await loadRows(endpoints.folder + "?kwarg=" + loweredFilter)
}