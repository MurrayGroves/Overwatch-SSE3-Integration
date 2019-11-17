from pynput import mouse

def on_click(x, y, button, pressed):
    if pressed:
        print(button)

    if not pressed:
        return False

with mouse.Listener(on_click=on_click) as listener:
    listener.join()
