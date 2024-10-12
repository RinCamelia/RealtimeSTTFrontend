import os
import sys
import keyboard
import time
import ruamel.yaml
from ruamel.yaml import yaml_object
from enum import Enum, auto


yaml = ruamel.yaml.YAML(typ='rt', pure=True)
yaml.explicit_start = True
yaml.explicit_end = True
yaml.line_break = True

config_file_name = 'config.yml'
lines_storage = []

class DumpMethod(Enum):
    yaml_tag = "DumpMethod"

    KEYBOARD = auto()
    TEXT_FILE = auto()

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_str(node.name)
    
    @classmethod
    def from_yaml(cls, constructor, node):
        return cls[node]

yaml.register_class(DumpMethod)

def load_config(config_file_name):
    config = dict(
        version=3,
        model='small.en',
        language='en',
        prompt='',
        enable_spinner=False,
        speech_model_sensitivity=0.05,
        dump_hotkey=';',
        dump_time_between_lines= 0.1,
        dump_method=DumpMethod.KEYBOARD,
        dump_file_name='transcribed_text.txt'
    )

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

def dump_lines(method):
    if len(lines_storage) > 0:
        print('writing lines via chosen dump method')
        match config['dump_method']:
            case DumpMethod.KEYBOARD:
                for line in lines_storage:
                    keyboard.write(line)
                    time.sleep(config['dump_time_between_lines'])
            case DumpMethod.TEXT_FILE:
                with open(config['dump_file_name'], 'a') as transcription_file:
                    transcription_file.writelines(lines_storage)
        lines_storage.clear()

config = load_config(config_file_name)

if __name__ == '__main__':
    from RealtimeSTT import AudioToTextRecorder 

    if os.name == 'nt' and (3, 8) <= sys.version_info < (3, 99):
        from torchaudio._extension.utils import _init_dll_path
        _init_dll_path()

    recorder = AudioToTextRecorder(
        spinner=config['enable_spinner'],
        silero_sensitivity=config['speech_model_sensitivity'],
        model=config['model'],
        language=config['language'],
        initial_prompt=config['prompt']
        )

    print('start commenting...')
    keyboard.add_hotkey(config['dump_hotkey'], dump_lines)
    
    try:
        while (True):
            recorder.text(process_text)
    except KeyboardInterrupt:
        print('Exiting application due to keyboard interrupt')