# BlocksWorld Environment for OpenAI Gym

This implementation uses the [bwstates](http://users.cecs.anu.edu.au/~jks/bwstates.html) application from John Slaney and Sylvie Thiébaux 

# How to install the OpenAI Gym Blocksworld environment

Clone this repository.

Download the bwstates sources from ftp://arp.anu.edu.au/pub/bwstates.1.tar.gz (In case you cannot find it you can download my compiled version also with the [sources here](https://drive.google.com/open?id=1vtimCnD2DcxsQfElhcdAqrAwD7dS_N0q))

Untar and unzip the file with
`tar xvfz bwstates.1.tar.gz`
(this will create a folder bwstates.1)

Copy the entire folder bwstates.1 into the folder /gym-blocksworld/gym_blocksworld/envs/BWSTATES

Compile the sources in the folder bwstates.1 (follow the instructions in bwstates1/README.ms). This should generate a binary file /bwstates.1/bwstates

Go to the folder containing the cloned repository (this folder should contain the cloned folder gym-blocksworld) and run the following command:

`pip install -e gym-blocksworld`

# How to use this environment

The folder /examples includes the file runEnvironment.py 

IMPORTANT: You need to create a file numBlocks.json and specify the number of blocks of your environment. See the file numBlocks.json in the folder /examples

# How to change the number of blocks
Edit the file numBlocks.json

# Syntax of the observations and actions
The observations of the environment include the current state of the environment and also the goal state. 

For example for an environment of 3 Blocks:

![Blocksworld representation sample](/BW_sample.png)

The representation for the above observation would be [3 1 0 0 0 2]
The three first digits (3 1 0) are the current state of the environment. Every array position expresses the position of the block and a value of 0 represents the table or the floor.

For example, for the (3 1 0), 3 in the first position of the array means "Block 1 is on top of Block 3", 1 in the second position of the array means "Block 2 is on top of Block 1", finally 0 in the third position of the array means "Block 3 is on top of the table or the floor")

The three last digits (0 0 2) are the goal state of the environment. For example (0 0 2) means "Block 1 is on top of the table", "Block 2 is on top of the table", "Block 3 is on top of Block ".

For the actions the representation is a 2 positions array. The first position means which block to be moved, and the second value means the destination of such Block. Value of 0 represents the table or the floor. For example if next action is [1, 0] means "Move Block 1 to the table or to the floor"
