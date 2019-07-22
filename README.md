<strong>Brewers Chronicle Ferment plug-in for CraftBeerPi version 3.0</strong>

This plug-in submits your ferment temperatures to the relevant ferment log in your Brewers Chronicle profile

<strong>Installation</strong>

At this stage, my request (from January 2019) to be added to the built-in "Add-On" section in CraftBeerPi has not been actioned.

Unfortunately this means that you will have to manually install this plug-in. Download the "__init__.py" file into a new directory in the [craftbeerpi]/modules/plugins/ directory on your device.

Read through the article on the <a href="https://github.com/Manuel83/craftbeerpi3/wiki/Extending-CraftBeerPi">CraftBeerPi website</a> on how to develop a plug-in. You could create the plug-in file and copy all content from the "__init.py" file in this repository.

<strong>Configuration</strong>

You will need to copy your API Key from the relevant brewery selected on the <A href="https://brewerschronicle.com/BreweryDetails">brewery details</a> page on Brewers Chronicle. Once you have selected the target brewery, expand the "Integration and API" section.

Copy and paste the API Key into the "brewerschronicle_api_key setting in the Parameters section.

When entering a name for each of your active ferments enter in the "|" pipe symbol followed by the ferment id copied out of Brewers Chronicle.
e.g "Summer pale ale|2017010114032846b96ce3c78b364f9"

Every 15 minutes the temperature will be posted to the relevant ferment log in your Brewers Chronicle profile.

If you set up a fermentation schedule for that ferment log, BC will calculate the current target temperature and return that value to the plug-in. That target temperature will then be applied to the relevant fermentor controller. The calculation will be based on days in ferment or gravity readings recorded to the ferment log, depending on how you setup the ferment schedule.

<strong>NB</strong>: one thing to note is that you will need to have a paid Brewers Chronicle brewery subscription to use the API. The free account does not allow API usage
