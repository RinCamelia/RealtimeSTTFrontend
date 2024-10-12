import os
import sys
import keyboard
import time
import ruamel.yaml
from enum import Enum, auto


yaml = ruamel.yaml.YAML(typ='rt', pure=True)
yaml.explicit_start = True
yaml.explicit_end = True
yaml.line_break = True

config_file_name = 'config.yml'
lines_storage = []

class DumpMethod(Enum):

    KEYBOARD = auto()
    TEXT_FILE = auto()

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_scalar(u'!DumpMethod',  node.name)
    
    @classmethod
    def from_yaml(cls, constructor, node):
        return cls[node.value]

yaml.register_class(DumpMethod)

def load_config(config_file_name):
    config = {
        'version': 4,
        'stt_settings': {
            'model': 'small.en',
            'language': 'en',
            'prompt': None,
            'enable_spinner': False,
            'speech_model_sensitivity': 0.05,
        },
        'hotkeys': {
            'text_output': ';'
        },
        'text_output': {
            'time_between_lines': 0.1,
            'method': DumpMethod.KEYBOARD,
            'file_name': 'transcribed_text.txt'
        }
    }

    if (os.path.isfile(config_file_name)):
        with open(config_file_name) as config_file:
            loaded_config = yaml.load(config_file)
            if loaded_config != None and 'version' in loaded_config and loaded_config['version'] == config['version']:
                config = loaded_config
            else:
                dump_config(config)
    else:
        dump_config(config)
    return config

def dump_config(config):
     with open(config_file_name, 'w') as config_file:
         yaml.dump(config, config_file)

def process_text(text):
    print('Transcribed line: ' + text)
    lines_storage.append(text + '\n')

def dump_lines():
    if len(lines_storage) > 0:
        print('writing lines via chosen dump method')
        match config['text_output']['method']:
            case DumpMethod.KEYBOARD:
                for line in lines_storage:
                    keyboard.write(line)
                    time.sleep(config['text_output']['time_between_lines'])
            case DumpMethod.TEXT_FILE:
                with open(config['text_output']['file_name'], 'a') as transcription_file:
                    transcription_file.writelines(lines_storage)
        lines_storage.clear()

config = load_config(config_file_name)

if __name__ == '__main__':
    from RealtimeSTT import AudioToTextRecorder 

    if os.name == 'nt' and (3, 8) <= sys.version_info < (3, 99):
        from torchaudio._extension.utils import _init_dll_path
        _init_dll_path()

    recorder = AudioToTextRecorder(
        spinner=config['stt_settings']['enable_spinner'],
        silero_sensitivity=config['stt_settings']['speech_model_sensitivity'],
        model=config['stt_settings']['model'],
        language=config['stt_settings']['language'],
        initial_prompt=config['stt_settings']['prompt']
        )

    print('start commenting...')
    keyboard.add_hotkey(config['hotkeys']['text_output'], dump_lines)
    
    try:
        while (True):
            recorder.text(process_text)
    except KeyboardInterrupt:
        print('Exiting application due to keyboard interrupt')