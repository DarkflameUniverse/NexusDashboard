# Nexus Dashboard

<p align="center">
  <img src="app/static/logo/logo.png" alt="DLU logo"/>
</p>

## Features

  * Account Management:
    * Ban, Lock, and Mute accounts (This Mute affects all Characters)
    * Account Deletion
    * Email ( all optional ):
      * Require email verification
      * Reset Password via Email
      * Edit Email ( by Admin only )
      * User Registration
      * Invitations ( TODO: Implement this )
      * Invitation Only Registration ( TODO: Implement this )
  * Play Key Management:
    * Create, Edit, and Add notes to play keys
    * View accounts Tied to a play key
  * Character Management:
    * Rescue: Pull character to a previously visited world
    * Restrict Trade: Toggle the character's ability to trade
    * Restrict Mail: Toggle the character's ability to send mail
    * Restrict Chat: Toggle the character's ability to send chat messages
    * Inventory viewer
      * View backpack contents, vault, models, and more!
    * Stats Viewer
  * Moderation:
    * Character Names:
      * Approve and mark as needs rename
    * Pet Names:
      * Auto-moderation of Pet names based on already moderated names
        * This is a scheduled tack that runs in the background every hour
      * Character Association, to see who has requested what name
      * Name cleanup: remove names of deleted pets/characters
    * Properties:
      * Approve and Un-approve Properties
      * Property/Model viewer
        * Pre-built and UGC model rendering
        * View Properties in full 360 in the browser!
        * View in LOD0 (High), LOD1(Medium), or LOD2(Low) quality
        * Download models
  * Bug Reports:
    * View and Resolve bug reports
  * Logs:
    * Command: View commands that have been run
    * Activity: View character activity of entering and exiting worlds
    * Audit:
      * View moderation activity (characters, pets, properties)
      * View GM Level changes
      * View Send Mail usage
    * System: View Extra logging of background activities of Nexus Dashboard
  * Send Mail:
    * Send Mail to characters
    * Attach items to Mail
  * Economy Reports:
    * Reports are generated as a scheduled background task run every day at 2300 UTC
    * Accounts with GM Level 3 and above are ignored
    * Item reports:
      * Reports numbers of items in existence
      * Includes backpack and Vault items
    * Currency:
      * Reports how much currency that characters posses
    * U-Score:
      * Reports how much U-Score that characters posses
  * Analytics:
    * Provide reporting to Developers to help better solve issues
    * Disabled by default. Set `ALLOW_ANALYTICS` to true to enable.

# Deployment

> **NOTE: This tutorial assumes you have a working DLU server instance and**
> **some knowledge of Linux**
## Docker

```bash

docker run -d \
    -e APP_SECRET_KEY='<secret_key>' \
    -e APP_DATABASE_URI='mysql+pymysql://<username>:<password>@<host>:<port>/<database>' \
    # you can include other optional Environment Variables from below like this
    -e REQUIRE_PLAY_KEY=True
    -p 8000:8000/tcp
    -v /path/to/unpacked/client:/app/luclient:rw \
    -v /path/to/cachedir:/app/cache:rw \
    aronwk/nexus-dashboard:latest

```

 * `/app/luclient` must be mapped to the location of an unpacked client
    * you only need `res/` and `locale/` from the client, but dropping the whole client in there won't hurt
 * Use `fdb_to_sqlite.py` in lcdr's utilities on `res/cdclient.fdb` in the unpacked client to convert the client database to `cdclient.sqlite`
    * Put the resulting `cdclient.sqlite` in the res folder: `res/cdclient.sqlite`

### Environmental Variables

Please Reference `app/settings_exmaple.py` to see all the variables

  * Required:
    * APP_SECRET_KEY (Must be provided)
    * APP_DATABASE_URI (Must be provided)
  * Everything else is optional and has defaults

## Manual

Thanks to [HailStorm32](https://github.com/HailStorm32) for this manual install guide!
### Setting Up The Environment
First you will want to install the following packages by executing the following commands
`sudo apt-get update`
`sudo apt-get install -y python3 python3-pip sqlite3 git unzip libmagickwand-dev`

> *Note: If  you are having issues with installing `sqlite3`, change it to `sqlite`*

<br>
Next we will clone the repository. You can clone it anywhere, but for the purpose of this tutorial, we will be cloning it to the home directory.

`cd` *make sure you are in the home directory*
`git clone https://github.com/DarkflameUniverse/NexusDashboard.git`

You should now have a directory called `NexusDashboard`

### Setting up

Rename the example settings file
`cp ~/NexusDashboard/app/settings_example.py ~/NexusDashboard/app/settings.py`

Now let's open the settings file we just created and configure some of the settings
`vim ~/NexusDashboard/app/settings.py`
>*Feel free to use any text editor you are more comfortable with instead of vim*

<br>
Inside this file is where you can change certain settings like user registration, email support and other things. In this tutorial I will only be focusing on the bare minimum to get up and running, but feel free to adjust what you would like

>*Note: Enabling the email option will require further setup that is outside the scope of this tutorial*

The two important settings to configure are `APP_SECRET_KEY` and `APP_DATABASE_URI`

For `APP_SECRET_KEY`, fill in any random 32 character string
For `APP_DATABASE_URI`, fill in the respective fields
```
<username>  --> database username
<password>  --> database password
<host>		--> database address
	(this will most likely be localhost if you are running the database on the same machine
<port>		--> port number of the database
	(this can most likely be left out if you are running the database on the same machine)
<database>	--> database name
```
>*If you are omitting `<port>`, make sure to also omit the `:`*

For a configuration where the database is running on the same machine, it would similar to this
```
APP_SECRET_KEY = "abcdefghijklmnopqrstuvwxyz123456"
APP_DATABASE_URI = "mysql+pymysql://DBusername:DBpassword@localhost/DBname"
```
The rest of the file is left at the default values

Once you are done making the changes, save and close the file

##### Client related files

We will need the following folders from the client
```
locale  (all of the files inside)

res
|_BrickModels
|_brickprimitives
|_textures
|_ui
|_brickdb.zip
```
Put the two folders in `~/NexusDashboard/app/luclient`

Unzip the `brickdb.zip` in place
`unzip brickdb.zip`

Remove the `.zip` after you have unzipped it
`rm brickdb.zip`

In the `luclient` directory you should now have a file structure that looks like this
```
local
|_locale.xml

res
|_BrickModels
	|_...
|_brickprimitives
	|_...
|_textures
	|_...
|_ui
	|_...
|_Assemblies
	|_...
|_Primitives
	|_...
|_Materials.xml
|_info.xml
```

We will also need to copy the `CDServer.sqlite` database file from the server to the `~/NexusDashboard/app/luclient/res` folder

Once the file is moved over, you will need to rename it to `cdclient.sqlite`
`mv ~/NexusDashboard/app/luclient/res/CDServer.sqlite ~/NexusDashboard/app/luclient/res/cdclient.sqlite`


##### Remaining Setup
Run the following commands one at a time

`cd ~/NexusDashboard`
`pip install -r requirements.txt`
`pip install gunicorn`
`flask db upgrade`

##### Running the site
You can run the site with
`gunicorn -b :8000 -w 4 wsgi:app`

# Development

Please use [Editor Config](https://editorconfig.org/)

  * `flask run` to run local dev server
