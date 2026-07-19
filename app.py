import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-flash-latest")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    try:

        user_prompt = request.json.get("prompt")

        if not user_prompt:
            return jsonify({"error": "Prompt missing"}), 400

        print("Request received")

        prompt = f"""
You are EcoPrompt AI.

Perform BOTH tasks in ONE response.

Task 1:
Rewrite the user's prompt to make it shorter, clearer and energy-efficient.
Reduce unnecessary words.
If many examples are requested, limit to 3-5 examples.

Task 2:
Answer ONLY the optimized prompt.

Return EXACTLY in this format:

OPTIMIZED PROMPT:
<optimized prompt>

AI RESPONSE:
<answer>

User Prompt:
{user_prompt}
"""

        result = model.generate_content(prompt)

        text = result.text

        if "AI RESPONSE:" in text:

            optimized_prompt = text.split("AI RESPONSE:")[0]
            optimized_prompt = optimized_prompt.replace(
                "OPTIMIZED PROMPT:",
                ""
            ).strip()

            ai_response = text.split("AI RESPONSE:")[1].strip()

        else:

            optimized_prompt = user_prompt
            ai_response = text

        original_words = len(user_prompt.split())
        optimized_words = len(optimized_prompt.split())

        words_saved = max(0, original_words - optimized_words)

        improvement = int(
            (words_saved / max(original_words, 1)) * 100
        )

        eco_score = min(100, 70 + improvement)

        energy_saved = round(improvement * 0.4, 1)

        co2_saved = round(improvement * 0.02, 3)

        if eco_score >= 90:
            rating = "🌍 Eco Champion"
        elif eco_score >= 80:
            rating = "🌱 Green Thinker"
        elif eco_score >= 70:
            rating = "👍 Good Prompt"
        else:
            rating = "⚠️ Needs Improvement"

        print("Gemini replied successfully")

        return jsonify({

            "optimizedPrompt": optimized_prompt,

            "response": ai_response,

            "ecoScore": eco_score,

            "energySaved": f"{energy_saved}%",

            "co2Reduced": f"{co2_saved} g",

            "rating": rating

        })

    except Exception as e:

        print("Error:", e)

        return jsonify({

            "error": str(e)

        }), 500


if __name__ == "__main__":
    app.run(debug=True)