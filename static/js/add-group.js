import {getData} from "./api.js";


async function filterEventListener() {
    let select = document.getElementsByTagName("select")[0]

    async function retrieveFilterInfo() {
        const preferenceField = document.getElementById("id_preferences")
        const preferences = extract_email(preferenceField)
        const min_age = document.querySelector("#from").textContent
        const max_age = document.querySelector("#from").textContent
        let path = ""
        const body = {
            min_age,
            max_age,
            preferences
        }
        return await getData(path, "post", body)
    }


    async function load() {

        let email_reference_reducer = Array.from(select.children).reduce((acc, cur) => {
            let value = cur.value
            acc[value] = cur
            return acc
        }, {})

        const data = await retrieveFilterInfo()
        data.forEach(el => email_reference_reducer[el].selected = true)
    }

    function extract_email(field) {
        return Array.from(field.children).reduce((acc, cur) => {
            if (cur.selected === true) {
                acc.push(cur.value)
            }

            return acc
        }, [])
    }

    await load()
}

function initialiseSlider() {
    const slider = document.getElementById('slider');
    noUiSlider.create(slider, {
        start: [20, 80],
        connect: true,
        range: {
            'min': 0,
            'max': 100
        },
    });
    const from = document.querySelector("#from")
    const to = document.querySelector("#to")
    slider.noUiSlider.on("update", (values) => {
        values = values.map(el => Number.parseInt(el))
        let [start, end] = values
        from.textContent = start
        to.textContent = end
    })
}

let select = document.querySelector("select")
let counter = document.querySelector("#counter")
select.addEventListener("click", () => {


    function extractSelectedCount() {
        return Array.from(select.children).filter(el => el.selected).length
    }

    counter.textContent = extractSelectedCount()
})

initialiseSlider()
document.querySelector("#select-button").addEventListener("click", filterEventListener)