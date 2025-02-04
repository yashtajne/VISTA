import webbrowser
import voice
import gemini


current_mode = ['workspace']

def gemini_loop(current_mode):
    current_mode[0] = 'gemini'
    while True:
        print(current_mode)
        command = voice.listen().lower()
        if command == 'exit':
            print("returning to workspace mode")
            current_mode[0] = 'workspace'
            return
        gemini.prompt(command)


def gesture_recognition(current_mode):
    current_mode[0] = 'gesture control'
    pass

def main_loop():
    while True:
        try:
            command = voice.listen().lower()
            if "gemini mode" in command:
                gemini_loop(current_mode)
            if "gesture control" in command:
                gesture_recognition(current_mode)
            else:
                if command == 'open google':
                    webbrowser.open('https://www.google.com')
                elif command == 'exit':
                    print("Exiting...")
                    break
        except KeyboardInterrupt:
            print("Program interrupted. Exiting...")
            break

if __name__ == "__main__":
    main_loop()
