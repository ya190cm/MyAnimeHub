from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

# Завантаження даних про аніме
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'data/anime_data.json')
with open(file_path, 'r') as f:
    anime_list = json.load(f)

@app.route('/')
def index():
    return render_template('index.html', anime_list=anime_list)

@app.route('/anime/<title>')
def anime_detail(title):
    # Заміна дефісів назад на пробіли та перетворення в правильний регістр
    title = title.replace('-', ' ').title()
    anime = next((a for a in anime_list if a["title"].lower() == title.lower()), None)
    if anime:
        return render_template('anime.html', anime=anime)
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    
    # Перевірка на None або порожній рядок
    if not query:
        return redirect(url_for('index'))

    results = [a for a in anime_list if query.lower() in a['title'].lower()]

    if results:
        if len(results) == 1:
            # Якщо знайдено тільки один збіг, перенаправляємо безпосередньо на сторінку аніме
            return redirect(url_for('anime_detail', title=results[0]['title'].replace(' ', '-').lower()))
        else:
            # Якщо знайдено декілька збігів, відображаємо їх
            return render_template('search_results.html', results=results, query=query)
    
    # Якщо нічого не знайдено, повертаємось на головну сторінку
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
