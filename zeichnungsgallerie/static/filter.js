const apply_filter = function () {
    const form = document.getElementById("filter_form")

    filter = {}

    for (const variable of variables) {
        const value = form.elements[variable].value
        if (value) {
            filter[variable] = value
        }

    }

    console.log("Filter:", filter)

    for (const element of document.getElementsByClassName("zeichnung")) {
        const zeichnung = element.getAttribute("zeichnung")
        const meta = records[zeichnung]

        var show = true
        for (const key in filter) {
            if (meta[key] != filter[key]) {
                var show = false
            }
        }

        element.style.display = show ? 'block' : 'none'
    }

    for (const variable in unique) {
        var i = 0
        for (const u of unique[variable]) {
            var unique_here = []
            for (const zeichnung in records) {
                const meta = records[zeichnung]
                var show = true
                for (const key in filter) {
                    if (key == variable) {
                        continue
                    }
                    if (meta[key] != filter[key]) {
                        var show = false
                    }
                }
                if (show) {
                    if (!unique_here.includes(meta[variable])) {
                        unique_here.push(meta[variable])
                    }
                }
            }


            var id = `${variable}${i}`
            console.log("ID:", id, "Unique Here:", unique_here)
            document.getElementById(id).toggleAttribute("disabled", !unique_here.includes(u))
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