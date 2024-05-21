document.querySelector("#finish-work").addEventListener("click", (event) => {
    document.querySelectorAll("input").forEach((target) => {
        target.removeAttribute("disabled");
    })
})