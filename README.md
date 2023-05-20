This was made using ChatGPT so I have no idea what stuff does, I am not a coder. so if there is any errors or crashes I have no idea how to fix them.
ask ChatGPT if you have questions I guess.. feel free to modify the code as you see fit and make any desired changes.

1. On Windows, simultaneously hold Shift and right-click.

2. Select "Open PowerShell Window here".

3. Populate the episodes.js file by running "python fetch_transcripts.py"
NOTE!! When dealing with many links, the process may take a while and generate larger file sizes due to varying transcript lengths. 
Please be aware that there may be episodes without transcripts or with unspecified languages, in which case an error will be reported before moving on to the next URL.
The "youtube_urls.txt" contains links to all the videos, livestreams, and podcasts from the H3 Podcast YouTube Channel until May 19, 2023.

4. Once the fetch_transcripts.py script is finished, start a Python server from this folder by typing "python -m http.server".

5. Open a browser and go to the following URL: http://localhost:8000/

6. Wait for a few seconds until the buttons vanish, indicating that the episodes file has finished loading and the site is now ready for use.

