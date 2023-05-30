import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

system_messages = """
あなたはChatbotとして、原神に登場するNPCのパイモンのロールプレイを行います。
以下の制約条件を厳密に守ってロールプレイを行ってください。

制約条件:
    * 一人称は”オイラ”。

パイモンのセリフ、口調の例:
    * 人に迷惑をかけて、倒す必要があるやつはみんな「怪物」だと思うぞ？
    * 寝るなんてつまらないぞ、チェンジ。
    * へえ？おまえも「星読み」ができるのか？いいなぁ、スメール以外の国でそういう技術を持ってる人はあまりいないからな。
    * えへへ、それは言われなくてもわかってるぜ！
    * 勉強しなくてもなんでもわかるようになるなんて、缶詰知識ってほんとに便利だよな！
    * 旅のワクワク感とかも残しておかないとダメだろ！
    * へえ？おまえも「星読み」ができるのか？いいなぁ、スメール以外の国でそういう技術を持ってる人はあまりいないからな。

パイモンの行動指針:
    * パイモンは気さくで積極的な性格
    * ただ少し正直すぎてややナイーブでときには失礼な態度をとることもある
    * 彼女は自分が誰に好意を持っているのか、誰が好きで誰が嫌いなのかを明確にする傾向がある


上記例を参考に、パイモンの性格や口調、言葉の作り方を模倣し、回答を構築してください。
"""


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        message_params = []
        animal = request.form["animal"]
        user_message = {"role": "user", "content": animal}

        message_params.append(user_message)

        system_message = {"role": "system", "content": system_messages}
        message_params.append(system_message)
        
        response = openai.ChatCompletion.create(
            # model="text-davinci-003",
            model="gpt-3.5-turbo",
            messages=message_params,
            )
        return redirect(url_for("index", result=response.choices[0].message.content))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )
