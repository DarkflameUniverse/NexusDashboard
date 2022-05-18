APP_THEME = "Blue"


def openFile(theme):
    with open("static/scss/site.scss", 'r') as f:
        lines = f.readlines()
        newline = "        \"primary\": " + theme + "," + "\n"
    with open("static/scss/site.scss", 'w') as f:
        lines[2] = newline
        f.writelines(lines)
        f.close()


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


