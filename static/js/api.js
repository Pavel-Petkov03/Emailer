const ROOT = "http://localhost:8000/api"


const endpoints = {
    folder: "/folder",
    bin: "/bin",
}

async function getData(path, body) {
    let url = `${ROOT}` + path
    let init = {
        method: "get",
        headers: {
            "content-type": "application/json",
        },
    }
    if (body) {
        Object.assign(init, body)
    }
    console.log(init)
    let response = await fetch(url, init)
    return await response.json()
}


function mainLoad() {
    let select = document.getElementsByName("select")[0]

    async function sendFilterInfo() {
        const preferenceField = select.getElementById("id_preferences")
        const all_emails = extract_email(preferenceField)

        let path = ""
        let data = await getData(path)
    }


    function load() {

        let email_reference_reducer = Array.from(select.children).reduce((acc, cur) => {
            let value = cur.value
            acc[value] = cur
            return acc
        }, {})
    }

    function extract_email(field) {
        return Array.from(field.children.map(child => child.value))
    }
}


export {
    endpoints,
    getData
}