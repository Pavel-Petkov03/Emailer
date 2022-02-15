import {root} from "./endpoints";


export default class Api {
    constructor(endpoint) {
        this.endpoint = endpoint
        this.tokenManager = new TokenManager()
    }


    async generateRequest(endpoint, method, body, contentType, token) {
        let options = {
            method,
        }

        let headers = {
            "Content-Type": contentType,
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods" : "GET,HEAD,OPTIONS,POST,PUT",
            "Access-Control-Allow-Headers" : "Origin, X-Requested-With, Content-Type, Accept, Authorization"
        }
        if (body) {
            Object.assign(options, {body: JSON.stringify(body)})
        }
        if (token) {
            Object.assign(headers, {"Authorization": "Bearer " + token})
        }

        Object.assign(options, {headers})
        const res = await fetch(endpoint, options)
        return  await res.json()
    }

    async apiCall(method, body, contentType) {
        try {
            // will call refresh token on every hit api call
            let tokenRes = await this.generateRequest("", method, body, contentType, this.tokenManager.getCookie("refresh"))
            this.tokenManager.setCookie("refresh", tokenRes.refresh)
            this.tokenManager.setCookie("access", tokenRes.access)
            return await this.generateRequest(this.endpoint, method, body, contentType, tokenRes.access)
        } catch (er) {
            // here will apply logic for redirect or modal toggle [not sure yet]
            console.log(er.message)
        }
    }
}


class TokenManager {
    setCookie(name, value) {
        const date = new Date();
        date.setTime(date.getTime() + (60 * 1000 * 2000));
        document.cookie = `${name}=${value};path=/;secure=true`
    }

    getCookie(name) {
        let value = `; ${document.cookie}`;
        let parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
}