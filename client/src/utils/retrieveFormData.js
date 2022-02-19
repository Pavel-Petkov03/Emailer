function retrieveFormData(form) {
    const customForm = new FormData(form)
    return [...customForm.entries()].reduce((acc, [k, v]) => Object.assign(acc, {[k]: v}), {})
}


export {
    retrieveFormData
}