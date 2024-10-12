def load_config(config_file_name):
    config = {
        'model': 'small.en',
        'language': 'en',
        'prompt': '',
        'enable_spinner': False,
        'speech_model_sensitivity': 0.05,
        'dump_hotkey': ';',
        'dump_time_between_lines': 0.1
    }

    if (os.path.isfile(config_file_name)):
        with open(config_file_name) as config_file:
            config = yaml.safe_load(config_file)
    else:
        with open(config_file_name, 'w') as config_file:
            yaml.safe_dump(config, config_file)
    return config

if __name__ == '__main__':

    import os
    import sys
    import keyboard
    import yaml
    from RealtimeSTT import AudioToTextRecorder 

    if os.name == 'nt' and (3, 8) <= sys.version_info < (3, 99):
        from torchaudio._extension.utils import _init_dll_path
        _init_dll_path()

    config_file_name = 'config.yml'
    config = load_config(config_file_name)

    recorder = AudioToTextRecorder(
        spinner=config['enable_spinner'],
        silero_sensitivity=config['speech_model_sensitivity'],
        model=config['model'],
        language=config['language'],
        initial_prompt=config['prompt']
        )

    lines_storage = []

    def process_text(text):
        print('Transcribed line: ' + text)
        lines_storage.append(text + '\n')

    def dump_lines():
        if len(lines_storage) > 0:
            print('writing lines...')
            for line in lines_storage:
                keyboard.write(line)
                time.sleep(config['dump_time_between_lines'])
            lines_storage.clear()


    print('start commenting...')
    keyboard.add_hotkey(config['dump_hotkey'], dump_lines)
    
    try:
        while (True):
            recorder.text(process_text)
    except KeyboardInterrupt:
        print('Exiting application due to keyboard interrupt')