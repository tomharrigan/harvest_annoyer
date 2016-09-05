# harvest_annoyer
Script to check whether a Harvest timer is running, and trigger a notification if not

The script will ping Harvest (every 5 minutes by default) to see if you have a timer running. If you don't, it will trigger an event which you can set up in IFTTT. A variable number of events can be set up to increase the annoyance level of the notification you receive depending on how long it's been since a timer has been running.

For example, in my current setup, at 5 minutes without a timer, I receive a push notification. 10 minutes: a text. 15 minutes: a phone call

To get up and running, plug your credentials into the init, replacing the placeholders.

The required credentials are:
* Your organizations' Harvest URL
* Your login email
* Your login password

This script is set up to trigger an IFTTT event using the Maker channel. You can replace this with your own notification mechanism, but the required items for triggering IFTTT are:
* ifttt_key: [Your IFTTT Maker Channel Key](https://ifttt.com/maker)
* ifttt_event: An event prefix for the events that fire. For example, if my events are 'harvest_tracking_1', 'harvest_tracking_2', 'harvest_tracking_3', the ifttt_event should be 'harvest_tracking'
* num_events: The number of events you've set up in IFTTT with this naming scheme

* frequency: How often the script will check to see if a timer is running. Currently set to 300 (5 minutes)

Once set up, just run by calling the file from the terminal, `python harvest_annoyer.py`

Currently this uses a scheduler. It can be changed to use a cron, but this method required the least set up time for getting this set up for others.

This script is based off of Lionhearts [Python wrapper for the Harvest API](https://github.com/lionheart/python-harvest) and [this article from Matt Henderson](http://dafacto.com/2012/how-to-never-forget-to-enable-your-time-tracking-timer/)