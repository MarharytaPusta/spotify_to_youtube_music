# Spotify to YouTube Music Converter

An automated Python script that reads a list of songs from a Spotify playlist and adds them to a YouTube Music playlist using browser UI automation.

## Features

* **Data Extraction:** Parses the provided Spotify playlist link to extract song titles.
* **UI Automation:** Uses Selenium to interact with the YouTube Music web interface, search for tracks, and add them to the user's library.

## Tech Stack

* **Python 3**
* **Selenium** for browser automation

## Setup and Usage

1. **Install dependencies:**
   ```bash
   pip install selenium
   ```
2. **Prepare configuration:**
Create a file named `data.txt` in the root directory. The first line of this file must contain the link to the target Spotify playlist.

3. **Prepare YouTube Music:**
For the addition to be successful, you must have a single playlist in YouTube Music that is named exactly the same as the target playlist in Spotify.

4. **Run the script:**
Launch the application from your terminal:
   ```bash
   python add_music.py
   ```

5. **The script will** launch a browser window and prompt for Google credentials to access YouTube Music.

## Known Issues

**Missing Tracks:** The program relies on YouTube Music's search engine, so it may occasionally not find certain specific songs.

**Google Security Blocks:** Because this script uses UI automation to log into a Google account, Google's security algorithms may occasionally flag and block the login attempt as an unverified browser.

If the program encounters an error or stops unexpectedly, simply restarting the script often resolves the issue.
