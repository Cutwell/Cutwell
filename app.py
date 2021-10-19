from flask import Flask, request, redirect, send_from_directory
import asyncio
from pyppeteer import launch
import threading

app = Flask(__name__)

print(f"Inside flask function: {threading.current_thread().name}")

KEY_MAP = ["ArrowLeft", "ArrowUp", "ArrowDown", "ArrowRight"]
REDIRECT = "http://127.0.0.1:5000/"
SERVER_BASE_URL = REDIRECT

global browser, page

@app.before_first_request
def init():
    print("Running pyppeteer init functions..")
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(initPage())

async def initPage():
    global browser, page
    # create browser session
    browser = await launch(
        headless=False,
        handleSIGINT=False,     # disable signal handling in order to run outside main thread
        handleSIGTERM=False,    # ..
        handleSIGHUP=False      # ..
    )
    page = await browser.newPage()
    url = f'{SERVER_BASE_URL}/serve/welcome_to_my_profile_.html'
    await page.goto(url)

async def getView():
    # screenshot canvas
    global page
    canvas = await page.querySelector('.game')
    await (await canvas.screenshot(path='frame.png', omitBackground=True))

async def safeShutdown():
    global browser
    await browser.close()

async def action(key):
    global page
    await page.keyboard.press(key)

@app.route('/game/action/<key>')
def event_up(key):
    if key in KEY_MAP:
        asyncio.set_event_loop(loop)
        asyncio.get_event_loop().run_until_complete(action(key))

        return redirect(REDIRECT, code=302)
    else:
        return 'invalid key', 400

@app.route('/game/view')
def view():
    print(f"Inside flask function: {threading.current_thread().name}")

    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(getView())

    return send_from_directory('', 'frame.png')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app.run(debug=1, use_reloader=False, port=5001, loop=loop)