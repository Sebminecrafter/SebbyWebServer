# SebbyWebServer
A simple python webserver
# Config
Set config via the config.txt file (it will be interpreted as python) be careful tho bro dont put random stuff you find online

port - the port of your server that data will be served on (the default for http is 80, https is 443)

host - The ip of your server (you can leave this blank if you are just testing and want it to auto-bind to all)

keyfilelocation - the file location of your private key (only needed for ssl/https)

certfilelocation - the file location of your certificate (only needed for ssl/https)

sebby_using_ssl - Whether or not to use ssl

handler_class = SebbyServer - Not recommended to change this (but you can if you know what you're doing)

append - what to add at the end of the page (by default it will add the sebby webserver name and version)

notfoundpage - the page that will show when a 404 error occurs (file not found)

# Features
 - Does not require any other modules (Only python 3.13+ guaruanteed working)
 - Very sigma
 - Coded very well (prob. not)
# Planned
 - Loadable custom functions
