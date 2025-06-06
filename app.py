from flask import Flask, render_template, request
import json

app = Flask(__name__)


def load_questions():
    with open("beck_questions.json", encoding="utf-8") as f:
        raw = json.load(f)
        questions = []
        for item in raw:
            if isinstance(item, list) and len(item) == 2:
                question_text = item[0]
                options = item[1]
                questions.append({
                    "text": question_text,
                    "options": options
                })
        return questions


questions = load_questions()


def results(score):
    if score <= 9:
        return "Depresión mínima o sin depresión", [
            "Mantén un estilo de vida saludable.",
            "Busca apoyo si notas cambios en tu estado de ánimo.",
            "Duerme al menos 7-8 horas por noche.",
            "Aliméntate balanceadamente y realiza actividad física.",
            "Practica técnicas de relajación como la respiración profunda o mindfulness."
        ]
    elif score <= 18:
        return "Depresión leve", [
            "Practica actividades que disfrutes.",
            "Considera hablar con un profesional de la salud mental.",
            "Establece rutinas diarias que te generen bienestar.",
            "Comparte tus emociones con alguien de confianza.",
            "Evita el aislamiento: mantente conectado con personas cercanas."
        ]
    elif score <= 29:
        return "Depresión moderada", [
            "Es recomendable buscar ayuda psicológica o psiquiátrica.",
            "No dudes en compartir tus sentimientos con personas de confianza.",
            "Establece metas pequeñas y alcanzables día a día.",
            "Monitorea tus pensamientos negativos y cuestiona su validez.",
            "Evita automedicarte y busca orientación profesional."
        ]
    else:
        return "Depresión grave", [
            "Busca atención profesional inmediata.",
            "No estás solo, hay ayuda disponible.",
            "Contacta a un psicólogo o psiquiatra de forma urgente.",
            "Habla con alguien de confianza sobre cómo te sientes.",
            "Si tienes pensamientos de autolesión o suicidio, busca ayuda de emergencia inmediatamente."
        ]


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", questions=questions)


@app.route("/result", methods=["POST"])
def result():
    try:
        answers = [int(request.form.get(
            f"question{i}")) for i in range(len(questions))]
    except (ValueError, TypeError):
        return "Por favor, responde todas las preguntas correctamente.", 400

    total = sum(answers)
    interpretation, suggestions = results(total)
    return render_template("resultado.html", total=total, interpretation=interpretation, suggestions=suggestions)


if __name__ == "__main__":
    app.run(debug=True)
