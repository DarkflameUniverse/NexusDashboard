# Nexus Dashboard

**This is a WIP: For Advanced Users**

<p align="center">
  <img src="app/static/logo/logo.png" alt="Sublime's custom image"/>
</p>

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
   -v /path/to/cachedir:/app/cache:rw \ # optional for persistent cache for conversions
   aronwk/nexus-dashboard:latest

```

 * /app/luclient must be mapped to the location of an unpacked client
   * you only need `res/` and `locale/` from the client, but dropping the whole cleint in there won't hurt
 * Use `fdb_to_sqlite.py` in lcdr's utilities on `res/cdclient.fdb` in the unpacked client to convert the client database to `cdclient.sqlite`
   * Put teh resulting `cdclient.sqlite` in the res folder: `res/cdclient.sqlite`
 * unzip `res/brickdb.zip` in-place
   * **Docker will do this for you**
   * you should have new folders and files in the following places:
      * `res/Assemblies/../..` with a bunch of sub folders
      * `res/Primitives/../..` with a bunch of sub folders
      * `res/info.xml`
      * `res/Materials.xml`

### Environmental Variables
 * Required:
    * APP_SECRET_KEY (Must be provided)
    * APP_DATABASE_URI (Must be provided)
 * Optional
    * USER_ENABLE_REGISTER (Default: True)
    * USER_ENABLE_EMAIL (Default: True, Needs Mail to be configured)
    * USER_ENABLE_CONFIRM_EMAIL (Default: True)
    * USER_ENABLE_INVITE_USER (Default: False)
    * USER_REQUIRE_INVITATION (Default: False)
    * REQUIRE_PLAY_KEY (Default: True)
    * MAIL_SERVER (Default: smtp.gmail.com)
    * MAIL_PORT (Default: 587)
    * MAIL_USE_SSL (Default: False)
    * MAIL_USE_TLS (Default: True)
    * MAIL_USERNAME (Default: None)
    * MAIL_PASSWORD (Default: None)
    * USER_EMAIL_SENDER_NAME (Default: None)
    * USER_EMAIL_SENDER_EMAIL (Default: None)

## Manual

Don't, use Docker /s

TODO: Make manual deployment easier to configure

# Development

Please use [Editor Config](https://editorconfig.org/)

 * `flask run` to run local dev server
