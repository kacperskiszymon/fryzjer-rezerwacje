document.addEventListener("DOMContentLoaded", function () {
    const fryzjerSelect = document.getElementById("fryzjer");
    const uslugaSelect = document.getElementById("usluga");
    const godzinaSelect = document.getElementById("godzina");
    const statusMessage = document.getElementById("status");

    // Pobierz terminy z API
    fetch("/terminy")
        .then(response => response.json())
        .then(data => {
            if (!data.fryzjerzy || !data.godziny) {
                throw new Error("Błąd w danych z API");
            }

            // Załaduj fryzjerów do listy
            Object.entries(data.fryzjerzy).forEach(([name, info]) => {
                let option = document.createElement("option");
                option.value = name;
                option.textContent = name;
                fryzjerSelect.appendChild(option);
            });

            // Po zmianie fryzjera wypełnij select usług oraz godzin
            fryzjerSelect.addEventListener("change", function () {
                const selectedFryzjer = fryzjerSelect.value;
                uslugaSelect.innerHTML = '<option value="">Wybierz usługę</option>';
                godzinaSelect.innerHTML = '<option value="">Wybierz godzinę</option>';

                if (selectedFryzjer && data.fryzjerzy[selectedFryzjer]) {
                    // Załaduj usługi dla wybranego fryzjera
                    data.fryzjerzy[selectedFryzjer].uslugi.forEach(usluga => {
                        let option = document.createElement("option");
                        option.value = usluga;
                        option.textContent = usluga;
                        uslugaSelect.appendChild(option);
                    });
                    // Załaduj dostępne godziny
                    data.godziny.forEach(godzina => {
                        let option = document.createElement("option");
                        option.value = godzina;
                        option.textContent = godzina;
                        godzinaSelect.appendChild(option);
                    });
                }
            });
        })
        .catch(error => {
            console.error("Błąd:", error);
            statusMessage.style.color = "red";
            statusMessage.textContent = "Nie można załadować terminów!";
        });
});

// Funkcja rezerwacji
function zarezerwuj() {
    const fryzjer = document.getElementById("fryzjer").value;
    const usluga = document.getElementById("usluga").value;
    const godzina = document.getElementById("godzina").value;
    const dzien = document.getElementById("dzien").value;
    const email = document.getElementById("email").value;
    const statusMessage = document.getElementById("status");

    if (!fryzjer || !usluga || !godzina || !dzien || !email) {
        statusMessage.style.color = "red";
        statusMessage.textContent = "Wypełnij wszystkie pola!";
        return;
    }

    fetch("/rezerwuj", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ fryzjer, usluga, godzina, dzien, email })
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
