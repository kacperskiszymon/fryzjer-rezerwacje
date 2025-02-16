document.addEventListener("DOMContentLoaded", function () {
    fetch("/terminy")
        .then(response => response.json())
        .then(data => {
            let godzinaSelect = document.getElementById("godzina");
            data.godziny.forEach(godz => {
                let option = document.createElement("option");
                option.value = godz;
                option.textContent = godz;
                godzinaSelect.appendChild(option);
            });
        })
        .catch(error => console.error("Błąd ładowania godzin:", error));
});

function zarezerwuj() {
    let fryzjer = document.getElementById("fryzjer").value;
    let godzina = document.getElementById("godzina").value;
    let dzien = document.getElementById("dzien").value;

    if (!dzien) {
        alert("Wybierz datę!");
        return;
    }

    fetch("/rezerwuj", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ fryzjer, usluga: "Strzyżenie", godzina, dzien })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("status").textContent = data.message;
    })
    .catch(error => console.error("Błąd rezerwacji:", error));
}
