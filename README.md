# Nexus Dashboard

<p align="center">
  <img src="app/static/logo/logo.png" alt="DLU logo"/>
</p>

## Features

  * Account Management:
    * Ban, Lock, and Mute accounts (This Mute affects all Characters)
    * Email (all optional):
      * Require email verification
      * Reset Password via Email
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
  * Install `imagemagick` or `libmagickwand-dev` for dds-to-png conversion
  * Copy `app/settings_exmaple.py` to `app/settings.py` and adjust the settings you would like.
    * Provide `APP_SECRET_KEY` and `APP_DATABASE_URI` in `app/settings.py`
  * app/luclient must contian a copy of an unpacked client
    * you only need `res/` and `locale/` from the client, but dropping the whole client in there won't hurt
  * Use `fdb_to_sqlite.py` in lcdr's utilities on `res/cdclient.fdb` in the unpacked client to convert the client database to `cdclient.sqlite`
    * Put the resulting `cdclient.sqlite` in the res folder: `res/cdclient.sqlite`
  * unzip `res/brickdb.zip` in-place
    * you should have new folders and files in the following places:
      * `res/Assemblies/../..` with a bunch of sub folders
      * `res/Primitives/../..` with a bunch of sub folders
      * `res/info.xml`
      * `res/Materials.xml`
  * Run:
    * `pip install -r requirements.txt`
    * `pip install gunicorn`
    * `flask db upgrade`
    * `gunicorn -b :8000 -w 4 wsgi:app`
      * Preferably, you want to setup a systemd service or something to keey this running

# Development

Please use [Editor Config](https://editorconfig.org/)

  * `flask run` to run local dev server
