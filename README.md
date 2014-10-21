## Python 3 Text Based Game Engine (with demo mode!)
<br>
**Description:**<br>
The engine to a Zork-like text game-- written entirely in Python 3
This particular version contains a simple demonstration of how to implement rooms, items, and simple commands into the game. There is also a "demo mode" in this code which you will be prompted to activate upon running the code. Try it, it's fun.
<br>
<br>
**To Run:**<br>
run main.py
<br>
<br>
**Just Beware:**<br>
This thing is an experiment. It's not complete, and I'm not going to complete it anytime soon. Besides, I can't write narrative, just code. You'll note that actor.py is barely used if at all, events.py was an experiment, help.py is a stand alone module and not yet implemented into the game, and there's at least one super hacky line in item.py. The meat and potatoes is here though. The magic happens in tokenizer.py, and room.py and item.py are so alike you should immediately see how they're used. My goal here was to make something that is as close to self-explanatory as code can get, so hopefully I've done that.
<br>
<br>
**Stuff For Coders:**<br>
I created this as an excercise in practicing Object Oriented Programming with Python. The most fragile code in this entire repo is anything with the work "import" before it. I learned a lot about import interactions between modules, and I would highly recommend that you pay close attention to the order in which imports happen while editing this code or adding enhancments.
<br>
Implementing decorators for the attributes of rooms seems like a great idea. I tinkered with this in previous versions (of which there are 9) but never got something solid enough to seem like it was worth the hassle. Some coders will tell you avoid them altogether, others swear by them, I'm undecided.
<br>
<br>
**One Other Thing:**<br>
If you want to play a larger demo of this type of thing, just Google "Zork" and look for the free online version of that amazing game. This game is based entirely off of that interface, though it is still lacking some of Zork's robustness.
<br>
