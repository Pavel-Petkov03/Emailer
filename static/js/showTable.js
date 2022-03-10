import {endpoints, getData} from "./api.js";

const i = document.createElement("i")
i.className = "fa fa-solid fa-filter"
window.onload = async () => {
    let filter = localStorage.getItem("filter") || ""
    await loadRows(endpoints.folder + "?" + filter)
    let headerTrs = document.querySelectorAll("thead tr th")
    Array.from(headerTrs).forEach(el => {
        if (el.textContent.toLowerCase() === localStorage.getItem("filter")) {
            el.prepend(i)
        }
        el.addEventListener("click", filterEvent)
    })
}


async function loadRows(url) {
    let data = await getData(url)
    let tbody = document.querySelector("tbody")
    tbody.innerText = ""
    data.forEach(el => {
        let tr = document.createElement("tr")
        Object.values(el).forEach(value => {
            let td = document.createElement("td")
            td.textContent = value
            tr.appendChild(td)
        })
        tbody.appendChild(tr)
    })
}


async function filterEvent(ev) {
    ev.target.prepend(i)
    const loweredFilter = ev.target.textContent.toLowerCase()
    localStorage.setItem("filter", loweredFilter)
    await loadRows(endpoints.folder + "?" + loweredFilter)
}