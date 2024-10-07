if __name__ == '__main__':

    import os
    import sys
    import keyboard

    if os.name == "nt" and (3, 8) <= sys.version_info < (3, 99):
        from torchaudio._extension.utils import _init_dll_path
        _init_dll_path()

    from RealtimeSTT import AudioToTextRecorder

    recorder = AudioToTextRecorder(
        spinner=False,
        silero_sensitivity=0.05,
        model="small.en",
        language="en"
        )
    
    lines_storage = []

    def process_text(text):
        print("Transcribed line: " + text)
        lines_storage.append(text + "\n")

    def dump_lines():
        if len(lines_storage) > 0:
            print("writing lines...")
            for line in lines_storage:
                keyboard.write(line)
            lines_storage.clear()


    print("start commenting...")
    keyboard.add_hotkey(";", dump_lines)
    
    try:
        while (True):
            recorder.text(process_text)
    except KeyboardInterrupt:
        print("Exiting application due to keyboard interrupt")