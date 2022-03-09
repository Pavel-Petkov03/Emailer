import {endpoints, getData} from "./api.js";


window.onload = async () => {
    let data = await getData(endpoints.folder)
    let tbody = document.querySelector("tbody")
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

