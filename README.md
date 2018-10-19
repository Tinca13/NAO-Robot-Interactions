# NAO-Robot-Interactions
Scripts that allow for full manipulation of the NAO robot's joints and sensors. Built using Python 2.7 32-bit (requirement for the naoqi module which works with the NAO robot). These scripts are for general purpose use for interacting with the robot. For more advanced experimental methods, the [old-gui branch](https://github.com/EThomas16/NAO-Robot-Interactions/tree/old-gui) contains more advanced functionality.

## Functionality:
- Speech recognition: for use with an external microphone, to allow control of the robot through speech commands with Python's [speech recognition module](https://pypi.org/project/SpeechRecognition/).
- GUI: Contains sliders to manipulate each joint of the robot's body as well as an option to perform preset movements.
- Live video: Streaming of video from the robot's camera.

## Voice commands:
There are five types of voice commands, with the full list being given in extra_info/commands.txt. The types of command are:
- Speech: Conversation based Human-Robot Interactions.
- Movement: For controlling the robots movements, such as walking.
- Behaviours: Used to trigger pre-installed complex movements.
- Dances: A subset of behaviours, these are pre-installed dances for the robot such as Michael Jackson's Thriller.
- Audio: Plays various songs using the robot's speakers.
There is also a final command which will stop the robot. Provided you say 'stop' in a sentence the robot will stop its current action and reset to wait for a new command to be given.

## Contributors:
- [Zach Wharton](https://github.com/zwharton15)
- [Erik Thomas](https://github.com/EThomas16)
- Neil Worthington
- Ryan Turner
