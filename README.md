# twitter-bot
Building a basic Twitter bot to level up skills in working with APIs

------------------------------------------------------------

In order to run this bot a python virtual environment must be configured.


Run this command in the working directory of your bot

$python3 -m venv <name of vm>
$source ./<name of vm>/bin/activate
$pip install tweepy


We do the steps above in order to avoid installing tweepy 
dependencies on our local machine.

------------------------------------------------------------

Below is how to configure the config.py file.
Enter your twitter api tokens where <credentials>.

run this in the working directory once youve enabled the vm above.

$export CONSUMER_KEY="<credentials>"
$export CONSUMER_SECRET="<credentials>"
$export ACCESS_TOKEN="<credentials>"
$export ACCESS_TOKEN_SECRET="<credentials>"

