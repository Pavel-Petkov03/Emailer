import {endpoints, getData} from "./api.js";

const select = document.querySelector("select")
const counter = document.querySelector("#counter")

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


class FilterLoader {

    emailReferenceReducer() {
        return Array.from(select.children).reduce((acc, cur) => {
            let value = cur.value
            acc[value] = cur
            return acc
        }, {})
    }

    extractEmail(field) {
        return Array.from(field.children).reduce((acc, cur) => {
            if (cur.selected === true) {
                acc.push(cur.value)
            }

            return acc
        }, [])
    }

    clearState() {
        Array.from(select.children).map(el => el.selected = false)
    }

    countSelected() {
        return Array.from(select.children).filter(el => el.selected).length
    }
}


const filterLoader = new FilterLoader()

async function retrieveFilterInfo() {
        const preferenceField = document.getElementById("id_preferences")
        const preferences = filterLoader.extractEmail(preferenceField)
        const min_age = document.querySelector("#from").textContent
        const max_age = document.querySelector("#to").textContent
        const body = {
            min_age,
            max_age,
            preferences
        }
        return await getData(endpoints["filter-emails"], "post", body)
    }


async function load() {
    filterLoader.clearState()
    const data = await retrieveFilterInfo()
    data.forEach(el => filterLoader.emailReferenceReducer()[el.email].selected = true)
    counter.textContent = filterLoader.countSelected()
}


async function main() {
    initialiseSlider()
    document.querySelector("#select-button").addEventListener("click", load)
    select.addEventListener("change", () => {
        counter.textContent = filterLoader.countSelected()
    })
}


main()