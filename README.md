<strong>Brewers Chronicle Ferment plug-in for CraftBeerPi version 3.0</strong>

This plug-in submits your ferment temperatures to the relevant ferment log in your Brewers Chronicle profile

<strong>Installation</strong>

At this stage, my request (from January 2019) to be added to the built-in "Add-On" section in CraftBeerPi has not been actioned.

Log in to your Raspberry Pi console and navigate to the plugins directory of the CBPi3 install.
Default location is /home/pi/craftbeerpi3/modules/plugins
Then copy and paste this command into your console:

git clone https://github.com/angusgrantBC/cbpi_BrewersChronicle.git BrewersChronicle

You will then need to restart CraftBerrPi by copying the below command into your Pi console. Or you can restart the entire device from within CraftBeerPi3 website
sudo service craftbeerpiboot restart

<strong>Configuration</strong>

You will need to copy your API Key from the relevant brewery selected on the <A href="https://brewerschronicle.com/BreweryDetails">brewery details</a> page on Brewers Chronicle. Once you have selected the target brewery, expand the "Integration and API" section.

Copy and paste the API Key into the "brewerschronicle_api_key setting in the Parameters section.

You will then need to configure brewery assets in the Brewery Details area to macth up the brewery asset devices to have the same "APIId" as your sensor name in CBPi3. You can view further documentation in the <a href="">Brewery Assets</a> knowledge base article

Every 15 minutes the temperature will be posted to the relevant ferment log in your Brewers Chronicle profile for any active fermentors in CBPi. If the fermentor is not currently active, no readings will be submitted.

On the first submission of readings, Brewers Chronicle will automatically create the asset and attached devices for that asset. At that stage it will not be linked to a ferment log, so you will need to log into Brewers Chronicle and allocate a ferment log to that asset. Any readings submitted are attached to the device itself.

Once you allocate a ferment log to your new Brewers Chronicle asset, submitted readings will be linked to the ferment log instead of directly to the asset device. You can elect to delete any readings attached to the device, or shift them into the ferment log.

If you set up a fermentation schedule for that ferment log, BC will calculate the current target temperature and return that value to the plug-in. That target temperature will then be applied to the relevant fermentor controller. The calculation will be based on days in ferment or gravity readings recorded to the ferment log, depending on how you setup the ferment schedule.

Please review the <a href="">CraftBeerPi</a> and <a href="">API</a> knowledge base articles for a full description of hos the system will work.

<strong>NB</strong>: one thing to note is that you will need to have a paid Brewers Chronicle subscription or switch to the personal-free-api subscription to use the API.
