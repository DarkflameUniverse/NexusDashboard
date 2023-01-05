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

# Deployment

> **NOTE: This tutorial assumes you have a working DLU server instance and**
> **some knowledge of command line interfaces on your chosen platform**


**It is highly recommended to setup a reverse proxy via Nginx or some other tool and use SSL to secure your Nexus Dashboard instance if you are going to be opening it up to any non-LANs**
 * [How to setup Nginx](https://www.digitalocean.com/community/tutorials/how-to-configure-nginx-as-a-reverse-proxy-on-ubuntu-22-04)
 * [How to use certbot for SSL](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-22-04)

## Docker

```bash
docker run -d \
    -e APP_SECRET_KEY='<secret_key>' \
    -e APP_DATABASE_URI='mysql+pymysql://<username>:<password>@<host>:<port>/<database>' \
    # you can include other optional Environment Variables from below like this
    -e REQUIRE_PLAY_KEY=True \
    -p 8000:8000/tcp \
    -v /path/to/unpacked/client:/app/luclient:ro \
    -v /path/to/cachedir:/app/cache:rw \
    ghcr.io/darkflameuniverse/nexusdashboard:latest
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

## Manual Linux Installation

Thanks to [HailStorm32](https://github.com/HailStorm32) for this manual install guide!

### Setting Up The Environment
First you will want to install the following packages by executing the following commands presuming you are on a Debian based system.

`sudo apt-get update`

`sudo apt-get install -y python3 python3-pip sqlite3 git unzip libmagickwand-dev`

> *Note: If  you are having issues with installing `sqlite3`, change it to `sqlite`*

<br>
Next you will want to clone the repository. You can clone it anywhere, but for the purpose of this tutorial, we will be cloning it to the home directory.'
<br></br>

Run `cd ~` to ensure that you are currently in the home directory then run the following command to clone the repository into our home directory
`git clone https://github.com/DarkflameUniverse/NexusDashboard.git`

You should now have a directory called `NexusDashboard` present in your home directory

### Setting up

Rename the example settings file
`cp ~/NexusDashboard/app/settings_example.py ~/NexusDashboard/app/settings.py`

Now let's open the settings file we just created and configure some of the settings with nano as it is a simple text editor that is easy to use
`nano ~/NexusDashboard/app/settings.py`
>*Obviously you can replace this with a text editor of your choice, nano is just the most simple to use out of the ones available by default on most Linux distros*

<br>
Inside this file is where you can change certain settings like user registration, email support and other things. In this tutorial we will only be focusing on the bare minimum to get up and running, but feel free to adjust what you would like to fit your needs.

>*Note: There are options in here that are related to email registration and password recovery among other features however those require extra setup not covered by this tutorial*

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
locale
└───locale.xml

res
├───BrickModels
├───brickprimitives
├───textures
├───ui
├───brickdb.zip
```
Put the two folders in `~/NexusDashboard/app/luclient`

Unzip the `brickdb.zip` in place
`unzip brickdb.zip`

Remove the `.zip` file after you have unzipped it, you can do that with
`rm brickdb.zip`

In the `luclient` directory you should now have a file structure that looks like this
```
locale
└───locale.xml

res
├───BrickModels
│   └─── ...
├───brickprimitives
│	└─── ...
├───textures
│	└─── ...
├───ui
│	└─── ...
├───Assemblies
│	└─── ...
├───Primitives
│	└─── ...
├───Materials.xml
└───info.xml
```

We will also need to copy the `CDServer.sqlite` database file from the server to the `~/NexusDashboard/app/luclient/res` folder

Once the file is moved over, you will need to rename it to `cdclient.sqlite`, this can be done with the following command
```bash
mv ~/NexusDashboard/app/luclient/res/CDServer.sqlite ~/NexusDashboard/app/luclient/res/cdclient.sqlite
```


##### Remaining Setup
To finish this, we will need to install the python dependencies and run the database migrations, simply run the following commands one at a time
```bash
cd ~/NexusDashboard
pip install -r requirements.txt
pip install gunicorn
flask db upgrade
```
##### Running the site
Once all of the above is complete, you can run the site with the command
`gunicorn -b :8000 -w 4 wsgi:app`

## Manual Windows Setup

While a lot of the setup on Windows is the same a lot of it can be completed with GUI interfaces and requires installing things from websites instead of the command line.

### Setting Up The Environment
You need to install the following prerequisites:

  * [Python 3.8](https://www.python.org/downloads/release/python-380/)
  * [Git](https://git-scm.com/downloads)
  * [ImageMagick](https://docs.wand-py.org/en/latest/guide/install.html#install-imagemagick-on-windows)
  * [7-Zip](https://www.7-zip.org/download.html)

Next you will need to clone the repository. You can clone it anywhere, but for the purpose of this tutorial, you will want to clone it to your desktop just for simplicity, it can be moved after.

Open a command prompt and run `cd Desktop` (The command line should place you in your Home directory be default) to ensure that you are currently in the desktop directory then run the following command to clone the repository into our desktop directory

Run the following command to clone the repository `git clone https://github.com/DarkflameUniverse/NexusDashboard.git`

You should now have a directory called `NexusDashboard` present on your desktop.

### Setting up
Now that we have the repository cloned you need to rename the example settings file, you can perform this manually in the GUI or you can use the command line, to do the latter run the following commands
  * `cd NexusDashboard\app`
  * `copy settings_example.py settings.py`

Now let's open the settings file we just created and configure some of the settings with the Windows default notepad.
* `notepad settings.py`

Inside this file is where you can change certain settings like user registration, email support and other things. In this tutorial we will only be focusing on the bare minimum to get up and running, but feel free to adjust what you would like to fit your needs.

> *Note: There are options in here that are related to email registration and password recovery among other features however those require extra setup not covered by this tutorial*

The two important settings to configure are `APP_SECRET_KEY` and `APP_DATABASE_URI`

For `APP_SECRET_KEY` you can just fill in any random 32 character string and for `APP_DATABASE_URI` you will need to fill in a connection string to your database. The connection string will look similar to this. You will need to fill in your own information for the username, password, host, port and database name.
```
APP_DATABASE_URI = "mysql+pymysql://<username>:<password>@<host>:<port>/<database>"
```
and the rest of the file can be left at the default values other than the `APP_SECRET_KEY` which you will need to fill in with random characters.

Once you are done making the changes, save and close the file

##### Client related files
We will need the following folders from the client
```
locale
└───locale.xml

res
├───BrickModels
├───brickprimitives
├───textures
├───ui
└───brickdb.zip
```
Put the two folders in `Desktop/NexusDashboard/app/luclient`

Unzip the `brickdb.zip` in place using 7-Zip, you can do this by right clicking the file and selecting `7-Zip > Extract Here`.

After doing this you can remove the `.zip`, simply delete the file.

In the `luclient` directory you should now have a file structure that looks like this
```
locale
└───locale.xml

res
├───BrickModels
│   └─── ...
├───brickprimitives
│	└─── ...
├───textures
│	└─── ...
├───ui
│	└─── ...
├───Assemblies
│	└─── ...
├───Primitives
│	└─── ...
├───Materials.xml
└───info.xml
```

We will also need to copy the `CDServer.sqlite` database file from the server to the `Desktop/NexusDashboard/app/luclient/res` folder

Once the file is moved over, you will need to rename it to `cdclient.sqlite`, this can be done by right clicking the file and selecting `Rename` and then changing the name to `cdclient.sqlite`

##### Remaining Setup
To finish this, we will need to install the python dependencies and run the database migrations, simply run the following commands one at a time in the root directory of the site, if you are not in the root directory you can run `cd Desktop/NexusDashboard` to get there (assuming you have opened a new terminal window)
```bat
pip install -r requirements.txt
flask db upgrade
```

##### Running the site
Once all of the above is complete, you can run the site with the command
`flask run` however bare in mind that this is a development version of the site, at the moment running a production version of the site on Windows is not supported.

# Development

Please use [Editor Config](https://editorconfig.org/) to maintain a consistent coding style between different editors and different contributors.

  * `python3 -m flask run` to run a local dev server
