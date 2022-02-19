import {retrieveFormData} from "./retrieveFormData";
import Api from "../api/Api";

async function onClick(url, router, ev) {
    console.log(router)
    ev.preventDefault()
    const body = retrieveFormData(document.querySelector("form"))
    let api = new Api()
    api.generateRequest(url, "post", body, "application/json").catch(er => {
        console.log(er)
    }).then(data => {
        router("/")
    })
}



export {
    onClick
}