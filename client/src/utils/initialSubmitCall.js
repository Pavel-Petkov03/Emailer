import {retrieveFormData} from "./retrieveFormData";
import {TokenManager, Api} from "../api/Api";

async function onClick(url, router, ev) {
    ev.preventDefault()
    const body = retrieveFormData(document.querySelector("form"))
    let api = new Api()
    api.generateRequest(url, "post", body, "application/json").catch(er => {
    }).then(data => {
        let tokenManager = new TokenManager()
        tokenManager.setCookie("access" , data.access)
        tokenManager.setCookie("refresh" , data.refresh)
        router("/")
    })
}



export {
    onClick
}