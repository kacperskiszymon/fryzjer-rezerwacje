document.addEventListener("DOMContentLoaded", function () {
    const fryzjerSelect = document.getElementById("fryzjer");
    const godzinaSelect = document.getElementById("godzina");
    const dzienInput = document.getElementById("dzien");
    const emailInput = document.getElementById("email");
    const statusMessage = document.getElementById("status");

    // Pobierz terminy z API
    fetch("/terminy")
        .then(response => response.json())
        .then(data => {
            if (!data.fryzjerzy || !data.godziny) {
                throw new Error("Błąd w danych z API");
            }

            // Załaduj fryzjerów do listy
            Object.entries(data.fryzjerzy).forEach(([name, services]) => {
                let option = document.createElement("option");
                option.value = name;
                option.textContent = `${name} - ${services.join(", ")}`;
                fryzjerSelect.appendChild(option);
            });

            // Obsługa wyboru fryzjera
            fryzjerSelect.addEventListener("change", function () {
                godzinaSelect.innerHTML = '<option value="">Wybierz godzinę</option>';
                data.godziny.forEach(godzina => {
                    let option = document.createElement("option");
                    option.value = godzina;
                    option.textContent = godzina;
                    godzinaSelect.appendChild(option);
                });
            });
        })
        .catch(error => {
            console.error("Błąd:", error);
            statusMessage.textContent = "Nie można załadować terminów!";
        });
});

// Funkcja rezerwacji
function zarezerwuj() {
    const fryzjer = document.getElementById("fryzjer").value;
    const godzina = document.getElementById("godzina").value;
    const dzien = document.getElementById("dzien").value;
    const email = document.getElementById("email").value;
    const statusMessage = document.getElementById("status");

    if (!fryzjer || !godzina || !dzien || !email) {
        statusMessage.textContent = "Wypełnij wszystkie pola!";
        return;
    }

    fetch("/rezerwuj", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ fryzjer, godzina, dzien, email })
    })
        .then(response => response.json())
        .then(data => {
            statusMessage.style.color = "green";
            statusMessage.textContent = data.message;
        })
        .catch(error => {
            console.error("Błąd:", error);
            statusMessage.style.color = "red";
            statusMessage.textContent = "Wystąpił błąd podczas rezerwacji.";
        });
}
