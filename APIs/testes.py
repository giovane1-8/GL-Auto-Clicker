from pynput.mouse import Listener


def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicado em ({x}, {y})")


def main():
    with Listener(on_click=on_click) as listener:
        listener.join()


if __name__ == "__main__":
    main()