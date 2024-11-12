from flask import Flask, render_template, request
import pandas as pd
import os
import json

app = Flask(__name__)


def load_music_data(name):
    data_path = f'data/{name}_Data'

    music_files = [f for f in os.listdir(data_path) if f.startswith('StreamingHistory_music') and f.endswith('.json')]

    all_data = []

    for file in music_files:
        file_path = os.path.join(data_path, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_data.extend(data)  

    music = pd.DataFrame(all_data)

    music['minutesPlayed'] = music['msPlayed'] / 60000

    return music

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/artists/<name>')
def artists(name):
    music = load_music_data(name)
    
    # Perform analysis, for example, top 10 most played songs
    top_songs_by_play_count = music['trackName'].value_counts().head(10).reset_index()
    top_songs_by_play_count.columns = ['trackName', 'play_count']
    top_songs_by_minutes_played = music.groupby('trackName')['minutesPlayed'].sum().sort_values(ascending=False).head(10).reset_index()
    return render_template('songs.html', name=name, top_songs_by_play_count=top_songs_by_play_count.to_html(index=False), top_songs_by_minutes_played=top_songs_by_minutes_played.to_html(index=False))


@app.route('/songs/<name>')
def songs(name):
    return render_template('songs.html', name=name)

@app.route('/genres/<name>')
def genres(name):
    return render_template('genres.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)