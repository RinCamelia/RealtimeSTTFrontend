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
    review_lines = []
    print("start commenting...")
    
    try:
        while (True):
            speech_line = recorder.text()
            print("Transcribed line: " + speech_line)
            review_lines.append(speech_line + "\n")
    except KeyboardInterrupt:
        print("writing lines...")
        for line in review_lines:
            keyboard.write(line)
        print("Exiting application due to keyboard interrupt")