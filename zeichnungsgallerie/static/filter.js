const apply_filter = function () {
    const form = document.getElementById("filter_form")

    filter = {}

    for (const variable of variables) {
        const value = form.elements[variable].value
        if (value) {
            filter[variable] = value
        }

    }

    console.log(filter)

    for (const element of document.getElementsByClassName("zeichnung")) {
        const zeichnung = element.getAttribute("zeichnung")
        const meta = records[zeichnung]

        var show = true
        for (const key in filter) {
            if (meta[key] != filter[key]) {
                var show = false
            }
        }

        console.log(zeichnung, show)
        element.style.display = show ? 'block' : 'none'
    }

}