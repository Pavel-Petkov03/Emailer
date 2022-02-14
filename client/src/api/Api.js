export default class Api {
    constructor(endpoint) {
        this.endpoint = endpoint
        this.tokenManager = TokenManager()
    }


    async generateRequest(endpoint, method, body, contentType, token) {
        let init = {}
        if (body) {
            init.body = body
        }
        let headers = {
            "content/type": contentType,
            method
        }
        if (token) {
            headers.authorization = token
        }
        init.headers = headers
        const response = await fetch(endpoint, init)
        if (response.status === 400) {
            throw new Error("Something went wrong")
        }
        return await response.json()
    }

    async apiCall(method, body, contentType) {
        try {
            // will call refresh token on every hit api call
            let tokenRes = await this.generateRequest("", method, body, contentType, this.tokenManager.getCookie("refresh"))
            this.tokenManager.setCookie("access", tokenRes.refresh)
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