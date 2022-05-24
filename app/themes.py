APP_THEME = "Blue"
FONT_THEME = "Nunito"


def openFile(theme):
    with open("static/scss/site.scss", 'r') as f:
        lines = f.readlines()
        newline = "        \"primary\": " + theme + "," + "\n"
    with open("static/scss/site.scss", 'w') as f:
        lines[2] = newline
        f.writelines(lines)
        f.close()

def newFont(font_url, font):
    with open("static/scss/site.scss", 'r') as f:
        lines = f.readlines()
        importline = "@import url(" + font_url + ");" + "\n"
        bodyline = "body { font-family:'" + font + "', Helvetica, Arial, sans-serif; }" + "\n"
    with open("static/scss/site.scss", 'w') as f:
        lines[10] = importline
        lines[12] = bodyline
        f.writelines(lines)
        f.close()


if APP_THEME == "Blue":
    HEX_CODE = "#005ac2"
    openFile(HEX_CODE)
if APP_THEME == "Red":
    HEX_CODE = "#FF0000"
    openFile(HEX_CODE)
if APP_THEME == "Green":
    HEX_CODE = "#006400"
    openFile(HEX_CODE)
if APP_THEME == "Yellow":
    HEX_CODE = "#FFCC00"
    openFile(HEX_CODE)
if APP_THEME == "Black":
    HEX_CODE = "#000000"
    openFile(HEX_CODE)
if APP_THEME == "Purple":
    HEX_CODE = "#A020F0"
    openFile(HEX_CODE)

if FONT_THEME == "Nunito":
    URL = "https://fonts.googleapis.com/css?family=Nunito:700"
    FONT_NAME = "Nunito"
    newFont(URL, FONT_NAME)
if FONT_THEME == "Grape Nuts":
    URL = "https://fonts.googleapis.com/css2?family=Grape+Nuts&display=swap"
    FONT_NAME = "Grape Nuts"
    newFont(URL, FONT_NAME)
if FONT_THEME == "Odibee Sans":
    URL = "https://fonts.googleapis.com/css2?family=Odibee+Sans&display=swap"
    FONT_NAME = "Odibee Sans"
    newFont(URL, FONT_NAME)
if FONT_THEME == "Righteous":
    URL = "https://fonts.googleapis.com/css2?family=Righteous&display=swap"
    FONT_NAME = "Righteous"
    newFont(URL, FONT_NAME)

print("Updated Dashboard Theme")



