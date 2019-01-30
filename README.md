<strong>Brewers Chronicle Ferment plug-in for CraftBeerPi version 3.0</strong>

This plug-in submits your ferment temperatures to the relevant ferment log in your Brewers Chronicle profile

<strong>Installation</strong>

Use the "Add-On" section in the "System" menu to download and install this plug-in.

Alternatively, you can pull the source files from GitHub into the [craftbeerpi]/modules/plugins/ directory

<strong>Configuration</strong>

You will need to copy your API Key from the relevant brewery selected from https://brewerschronicle.com/BreweryDetails. Once you have selected the target brewery, expand the "Integration and API" section.

Copy and paste the API Key into the "brewerschronicle_api_key setting in the Parameters section.

When entering a name for each of your active ferments enter in the "|" pipe symbol followed by the ferment id copied out of Brewers Chronicle.
e.g "Summer pale ale|2017010114032846b96ce3c78b364f9"

Every 15 minutes the temperature will be posted to the relevant ferment log in your Brewers Chronicle profile.

If you set up a fermentation schedule for that ferment log, BC will calculate the current target temperature. The calculation will be based on days in ferment or gravity readings recorded to the ferment log, depending on how you setup the ferment schedule.

<strong>NB</strong>: one thing to note is that you will need to have a paid Brewers Chronicle brewery subscription to use the API. The free account does not allow API usage
