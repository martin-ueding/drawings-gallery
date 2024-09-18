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

    currently_unique = {}
    for (const variable of variables) {
        currently_unique[variable] = []
    }

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


        if (show) {
            for (const variable of variables) {
                if (!currently_unique[variable].includes(meta[variable])) {
                    currently_unique[variable].push(meta[variable])
                }
            }
        }
    }


    console.log(currently_unique)

    for (const variable in unique) {
        var i = 0
        for (const u of unique[variable]) {
            var id = `${variable}${i}`
            console.log(id)
            document.getElementById(id).toggleAttribute("disabled", !currently_unique[variable].includes(u))
            ++i
        }
    }

}

const reset_filter = function () {
    for (const variable of variables) {
        document.getElementById(variable).checked = true
    }
    apply_filter()
}

reset_filter()