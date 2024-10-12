# Intro

Simple frontend that uses `RealtimeSTT` and `keyboard` to do local speech to text. Currently very minimal for my personal use.

# Requirements

 * [RealtimeSTT](https://github.com/KoljaB/RealtimeSTT) 
 * [Keyboard](https://github.com/boppreh/keyboard)
 * [PyYAML](https://pyyaml.org/)
 * Python 3.12

# Usage

> python main.py

On a command line. Speak into your mic. it will be transcribed to the command line so you can see the lines as they come in, and pressing the configured hotkey (default is ';') will dump everything in its buffer via keyboard events and clear its current buffer. Careful! If you hold a modifier or have a non-text-field focused, you could dump a ton of inputs into something that you don't intend.

The script dumps a config YAML file if it doesn't exist on first run - then you can modify it to change many aspects of behaviour. 

# Notes

Does not use CUDA - I don't have an NVidia GPU to install or test this, and I haven't yet figured out any of the AMD compatible translation layers.
Uses the `small` model - this is reasonably performant on my machine, but you may want to edit to `base` or `tiny` if your CPU isn't very powerful. 
Many thanks to the testing scripts provided by RealtimeSTT!