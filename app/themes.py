APP_THEME = "Blue"


def openFile(theme):
    with open("static/scss/site.scss", 'r') as f:
        lines = f.readlines()
        primary = lines[2]
        print(primary)
        print("        \"primary\": " + theme + ",")


if APP_THEME == "Blue":
    HEX_CODE = "#005ac2"
    openFile(HEX_CODE)
if APP_THEME == "Red":
    HEX_CODE = "#FF0000"
    openFile(HEX_CODE)
if APP_THEME == "Green":
    HEX_CODE = "#808000"
    openFile(HEX_CODE)
if APP_THEME == "Yellow":
    HEX_CODE = "#FFFF00"
    openFile(HEX_CODE)


