class Api {
    constructor(endpoint) {
        this.endpoint = endpoint
        this.tokenManager = TokenManager()
    }


    async generateRequest(endpoint, method, body, contentType, token) {
        let init = {}
        if (body) {
            init.body = body
        }

        init.headers = {
            "content/type": contentType,
            "authorization": `Bearer ${token}`
        }
        const response = await fetch(endpoint, init)
        if (response.status === 400) {
            throw new Error("Something went wrong")
        }
        return await response.json()
    }

    async apiCall(method, body, contentType) {
        try {
            let tokenRes = await this.generateRequest("", method, body, contentType, this.tokenManager.getCookie("refresh"))
            this.tokenManager.setCookie("access_token", tokenRes.access)
            return await this.generateRequest(this.endpoint, method, body, contentType, this.tokenManager.getCookie("access"))
        } catch (er) {
            // here will apply logic for redirect or modal toggle [not sure yet]
            console.log(er.message)
        }
    }

}


class TokenManager {

    updateCurrentToken(){

    }

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