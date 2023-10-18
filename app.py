from flask import Flask, request, render_template
import openai

app = Flask(__name__)

openai.api_key = "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"

list_img = []

@app.route('/', methods=["GET", "POST"])
def peticion():
    if request.method == 'POST':
        descripcion = request.form.get("descripcion")
        nimg = int(request.form.get("nimg"))
        for _ in range(nimg):
            url_img = crear_img(descripcion)
            list_img.append(url_img)
        respuesta_chat = generar_res(descripcion)
        return render_template('index.html', list_img=list_img, respuesta_chat=respuesta_chat)
    return render_template('index.html', list_img=list_img)

def crear_img(descripcion):
    respuesta = openai.Image.create(
            prompt=descripcion,
            n=1,
            size="512x512"
        )
    return respuesta["data"][0]["url"]

def generar_res(descripcion):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": descripcion
            }
        ]
    )

    respuesta_chat = response["choices"][0]["message"]["content"]

    return respuesta_chat

if __name__ == "__main__":
    app.run(debug=True, port=5000)
