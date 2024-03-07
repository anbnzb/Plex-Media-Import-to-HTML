# Plex-Media-Import-to-HTML
Export your Plex Library as an interactive HTML page to save as a backup or for others to browse.<br>

# Summary
Plex Export allows you to produce an HTML page with information on the media contained within your Plex library.<br>
HTML page generated by the script does not expose any direct access to your Plex server.<br>

# Features
-Provides an overview of all media in each of your library sections.<br>
-Images are lazy loaded as you scroll down.<br>

# Instructions

1. You must have Python installed on your system for this to work (PLEX Media Import to HTML does not have to be run on the system containing Plex Media Server)<br>
2. In your preferred shell/terminal enter the following command: python import.py<br>
3. Enter Plex Ip address, Plex token, location to save the html and then install packages.<br>
4. If Plex Media Server is running on a different machine, specify it's URL with the -plex-url parameter e.g. plex-ip-address:32400<br>
5. Upon completion your html page will contain thumbnails of all movies and tv shows on your server unless hidden. Enjoy :)<br>

# Notes

-The script was built on windows 11 using edge browser and command prompt.<br>
-Delete import.py if you upload PLEX Media Import to HTML to any public location<br>
-If your Plex Server is running in Home mode, we need to authenticate via a token<br>
-To get a valid token for your system, look here: https://support.plex.tv/hc/en-us/articles/204059436-Finding-your-account-token-X-Plex-Token<br>
 
