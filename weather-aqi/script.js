const startBtn = document.getElementById("startBtn");
const registrationPage = document.getElementById("registrationPage");
const rulesPopup = document.getElementById("rulesPopup");
const agreeCheck = document.getElementById("agreeCheck");
const weatherCard = document.getElementById("weatherCard");

function openRules() {
    rulesPopup.style.display = "block";
}

function closeRules() {
    rulesPopup.style.display = "none";
}

function enableStart() {
    if (agreeCheck.checked) {
        startBtn.classList.add("enabled");
        startBtn.disabled = false;
    } else {
        startBtn.classList.remove("enabled");
        startBtn.disabled = true;
    }
}

function goToRegister() {
    if (!agreeCheck.checked) {
        alert("⚠ Please agree to the rules before starting.");
        return;
    }
    rulesPopup.style.display = "none"; 
    registrationPage.style.display = "block";
}


// Registration + WhatsApp sending
document.getElementById("submitBtn").addEventListener("click", registerUser);

function registerUser() {
    const name = document.getElementById("name").value;
    const age = document.getElementById("age").value;
    const mobile = document.getElementById("mobile").value;
    const city = document.getElementById("city").value;

    if(!name || !age || !mobile || !city){
        alert("⚠ Please fill all details");
        return;
    }

    fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({name, age, mobile, city})
    })
    .then(res => res.json())
    .then(data => {
        if(data.error){
            document.getElementById("status").innerText = "❌ " + data.error;
            weatherCard.innerHTML = "";
        } else {
            document.getElementById("status").innerText = "✔️ WhatsApp Alert Activated!";

            const w = data.weather;

            weatherCard.style.display = "block";
            weatherCard.innerHTML = `
                <p>🌍 <strong>City:</strong> ${w.city}</p>
                <p>⏰ <strong>Time:</strong> ${w.local_time}</p>
                <p>🌡 <strong>Temperature:</strong> ${w.temperature}°C</p>
                <p>🌦 <strong>Condition:</strong> ${w.condition}</p>
                <p>💧 <strong>Humidity:</strong> ${w.humidity}%</p>
                <p>💨 <strong>Wind Speed:</strong> ${w.wind} m/s</p>
                <p>🌫 <strong>AQI Level:</strong> ${w.aqi}</p>
                <p>🔬 <strong>PM2.5:</strong> ${w.pm2_5}</p>
            `;
        }
    })
    .catch(() => {
        document.getElementById("status").innerText = "❌ Network Error";
    });
}
