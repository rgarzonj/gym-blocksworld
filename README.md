# BlocksWorld Environment for OpenAI Gym

This implementation uses the [bwstates](http://users.cecs.anu.edu.au/~jks/bwstates.html) application from John Slaney and Sylvie Thiébaux 

# How to install the OpenAI Gym Blocksworld environment

Clone this repository.

Download the bwstates sources from the [following ftp] ftp://arp.anu.edu.au/pub/bwstates.1.tar.gz (In case you cannot find it you can download my compiled version also with the [sources here](https://drive.google.com/open?id=1vtimCnD2DcxsQfElhcdAqrAwD7dS_N0q))

Untar and unzip the file with
`tar xvfz bwstates.1.tar.gz`
(this will create a folder bwstates.1)

Copy the entire folder bwstates.1 into the folder /gym-blocksworld/gym_blocksworld/envs/BWSTATES

Compile the sources in the folder bwstates.1 (follow the instructions in bwstates1/README.ms). This should generate a binary file /bwstates.1/bwstates

Go to the folder containing the cloned repository (this folder should contain the cloned folder gym-blocksworld) and run the following command:

`pip install -e gym-blocksworld`

# How to use this environment

The folder /examples includes the file RandomAgent.py 

IMPORTANT: You need to create a file numBlocks.json and specify the number of nlocks of your environment. See the file numBlocks.json in the folder /examples

# How to change the number of blocks


Edit the file numBlocks.json