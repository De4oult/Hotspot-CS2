from sanic import Sanic, Request
from sanic.response import html
from sanic_cors import CORS

# REMOVE ON PROD
from dotenv import load_dotenv
load_dotenv()

import requests

from fetch import supabase

import os

app = Sanic(__name__)

CORS(app)

steam_key: str = os.getenv('STEAM_API_KEY')
bot_token: str = os.getenv('BOT_TOKEN')

@app.route('/confirm_steam', methods = ['GET'])
async def confirm_steam(request: Request):
    steam_id = request.args.get('openid.claimed_id').split('/')[-1]

    player_data = requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steam_key}&steamids={steam_id}').json().get('response').get('players')[0]

    playername = player_data.get('personaname')

    await supabase.push('players', {
        'id' : request.args.get('tg_id'),
        'steam_id' : steam_id,
        'playername' : playername,
        'username' : request.args.get('username')
    })

    requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', data = { 
        'chat_id' : request.args.get('tg_id'),
        'text' : f'event:registration_complete,playername:{playername}'
    })

    return html('<h1 style="text-align: center; font-size: 2rem;">Это окно можно закрыть</h1>', status = 200)

if __name__ == "__main__":
    app.run(
        host = '0.0.0.0', 
        port = 8080, 
        access_log = False
    )