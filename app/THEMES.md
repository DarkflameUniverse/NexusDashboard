# Themes for Nexus Dashboard

This is how to use `themes.py` to change the look of your dashboard

## Primary Color

Editing the primary color (in the script this is `APP_THEME`) will change the colors of the navbar and buttons

Here's the list of colors that are available to use in this python script

 * `APP_THEME = "Blue"`:
    * Changes the navbar and button colors to Blue	  
 * `APP_THEME = "Red"`:
    * Changes the navbar and button colors to Red
 * `APP_THEME = "Green"`:
   * Changes the navbar and button colors to Green
 * `APP_THEME = "Yellow"`:
   * Changes the navbar and button colors to Yellow
 * `APP_THEME = "Black"`:
   * Changes the navbar and button colors to Black
 * `APP_THEME = "Purple"`:
   * Changes the navbar and button colors to Purple

## Font 

Editing the font style (in the script this is `FONT_THEME` will change the look of the font on the dashboard

Here's the list of font styles so far that are available to use in this python script

 * `FONT_THEME = "Nunito"`:
   * This is currently the default font
 * `FONT_THEME = "Grape Nuts"`
 * `FONT_THEME = "Odibee Sans"`
 * `FONT_THEME = "Righteous"`

## Applying the changes

To apply the changes you have made, simply open up a command line and cd into the app directiory (This would be `NexusDashboard/app`), then you run `python3 themes.py` and you can see the changes on your dashboard
