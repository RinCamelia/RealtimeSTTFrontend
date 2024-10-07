# Intro

Simple frontend that uses `RealtimeSTT` and `keyboard` to do local speech to text. Currently very minimal for my personal use.

# Requirements

 * [RealtimeSTT](https://github.com/KoljaB/RealtimeSTT) 
 * [Keyboard](https://github.com/boppreh/keyboard)
 * Python 3.12

# Usage

> python main.py

On a command line. Speak into your mic as you need it. it will be transcribed to the command line so you can see the lines as they come in, and pressing ; will dump everything in its buffer via keyboard events into whatever is open and clear its current buffer. 

# Notes

Does not use CUDA - I don't have an NVidia GPU to install or test this, and I haven't yet figured out any of the AMD compatible translation layers.
Uses the `small` model - this is reasonably performant on my machine, but you may want to edit to `base` or `tiny` if your CPU isn't very powerful. 
Credit to the simple test script provided by `RealtimeSTT` - the script is currently a modified version of that while I figure out how the final form should behave