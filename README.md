# BlocksWorld Environment for OpenAI Gym!

This implementation uses the [bwstates](http://users.cecs.anu.edu.au/~jks/bwstates.html) application from John Slaney and Sylvie Thiébaux 

# How to install the environment

Clone this repository

Download the bwstates sources from the following ftp [ftp://arp.anu.edu.au/pub/bwstates.1.tar.gz](ftp://arp.anu.edu.au/pub/bwstates.1.tar.gz)

Untar and unzip the file with
`tar xvfz bwstates.1.tar.gz`

Copy the folder bwstates.1 folder into the folder /gym-blocksworld/gym-blocksworld/envs/BWSTATES

Compile the sources. This should generate a binary file /bwstates.1/bwstates

Go to the folder containing the file setup.py and run: 

`pip install .`

# How to use this environment

The folder /examples includes the file RandomAgent.py 

IMPORTANT: You need to create a file numBlocks.json and specify the number of nlocks of your environment. See the file numBlocks.json in the folder /examples
