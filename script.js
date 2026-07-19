window.onload = function () {

    const button = document.querySelector(".optimize-btn");
    console.log(button);
    button.onclick = async function () {

    const prompt = document.querySelector("textarea").value.trim();
    document.getElementById("originalPrompt").textContent = prompt;
    if (prompt === "") {
        alert("Please enter a prompt first!");
        return;
    }

    document.getElementById("result").style.display = "block";

    document.getElementById("aiResponse").textContent = "⏳ Gemini is thinking...";

    const response = await fetch("/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            prompt: prompt
        })
    });

    const data = await response.json();
    console.log(data);

    document.getElementById("optimizedPrompt").innerHTML =
    data.optimizedPrompt.replace(/\n/g, "<br>");

    document.getElementById("aiResponse").innerHTML =
    data.response.replace(/\n/g, "<br>");

    document.getElementById("ecoScore").textContent =
    data.ecoScore + "/100";

    document.getElementById("energy").textContent =
    data.energySaved;

    document.getElementById("co2").textContent =
    data.co2Reduced;

    document.getElementById("rating").textContent =
    data.rating;
    if (data.error) {
    document.getElementById("aiResponse").textContent = data.error;
    return;
    }
};
};