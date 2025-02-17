document.addEventListener("DOMContentLoaded", async function () {
    const selectFryzjer = document.getElementById("fryzjer");
    const selectGodzina = document.getElementById("godzina");
    const selectUsluga = document.getElementById("usluga");
    const selectDzien = document.getElementById("dzien");
    const status = document.getElementById("status");

    try {
        const response = await fetch("https://fryzjer-rezerwacje.onrender.com/terminy");
        const data = await response.json();

        // Dodaj fryzjerów do wyboru
        for (const fryzjer in data.fryzjerzy) {
            let option = document.createElement("option");
            option.value = fryzjer;
            option.textContent = fryzjer;
            selectFryzjer.appendChild(option);
        }

        // Załaduj domyślne usługi dla pierwszego fryzjera
        updateUslugi(selectFryzjer.value, data.fryzjerzy);

        // Zmiana usług w zależności od wybranego fryzjera
        selectFryzjer.addEventListener("change", function () {
            updateUslugi(selectFryzjer.value, data.fryzjerzy);
        });

        // Dodaj godziny do wyboru (reset przed dodaniem)
        selectGodzina.innerHTML = "";
        data.godziny.forEach(godzina => {
            let option = document.createElement("option");
            option.value = godzina;
            option.textContent = godzina;
            selectGodzina.appendChild(option);
        });

    } catch (error) {
        console.error("Błąd pobierania terminów:", error);
        status.textContent = "Nie można załadować terminów!";
        status.style.color = "red";
    }

    function updateUslugi(fryzjer, fryzjerzy) {
        selectUsluga.innerHTML = "";
        if (fryzjerzy[fryzjer]) {
            fryzjerzy[fryzjer].forEach(usluga => {
                let option = document.createElement("option");
                option.value = usluga;
                option.textContent = usluga;
                selectUsluga.appendChild(option);
            });
        }
    }
});

function zarezerwuj() {
    let fryzjer = document.getElementById("fryzjer").value;
    let usluga = document.getElementById("usluga").value;
    let godzina = document.getElementById("godzina").value;
    let dzien = document.getElementById("dzien").value;
    let status = document.getElementById("status");

    if (!dzien) {
        alert("Wybierz datę!");
        return;
    }

    fetch("https://fryzjer-rezerwacje.onrender.com/rezerwuj", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ fryzjer, usluga, godzina, dzien })
    })
    .then(response => response.json())
    .then(data => {
        status.textContent = data.message;
        status.style.color = "green";
    })
    .catch(error => {
        console.error("Błąd rezerwacji:", error);
        status.textContent = "Błąd rezerwacji!";
        status.style.color = "red";
    });
}
