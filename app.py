from flask import Flask, render_template
from flask_assets import Environment, Bundle
from MindCard import DataBaseManager


app = Flask(__name__, template_folder='templates')
assets = Environment()
styles = Bundle('styles.css', filters='cssmin')
assets.init_app(app)

url = 'sqlite:///mindmap.db'

db = DataBaseManager(url)
db.export('data.txt')



@app.route('/')
def index():
    # Получите все строки из таблицы.
    results = db.select(chunk=5)
    print()
    # Создайте список карточек.
    cards = []
    for row in results:
        card = {
            "front": row.eng,
            "back": row.rus
        }
        cards.append(card)

    # Отобразите набор карточек.
    return render_template('card.html', cards=cards)



if __name__ == '__main__':
    app.run()
