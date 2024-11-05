# CoC_Scripts

Scripts to automate tasks in Clash of Clans using the official API. These scripts allow you to retrieve up-to-date information about your clan, members, and other related data. The following steps explain how to set up and run the scripts.

## Table of Contents

1. [Requirements](#requirements)
2. [Installing Python](#installing-python)
3. [Getting Your Clash of Clans API Token](#getting-your-clash-of-clans-api-token)
4. [Getting Your Clan Tag](#getting-your-clan-tag)
5. [Configuring Text Files](#configuring-text-files)
6. [Running the Scripts](#running-the-scripts)
7. [Contributing](#contributing)

---

### Requirements

- **Operating System**: Windows, MacOS, or Linux
- **Python**: Version 3.6 or higher (see installation instructions below)
- **Clash of Clans Account**: Needed to obtain the API token and clan tag

### Installing Python

If you don’t already have Python installed, follow these steps:

1. **Download Python** from the [official Python website](https://www.python.org/downloads/).
2. **Install Python**: During installation, select the “Add Python to PATH” checkbox to simplify usage of Python from the command line.
3. **Verify the installation**: Open a terminal or command prompt and run:

   ```bash
   python --version
   
You should see the installed Python version. If a version number appears, the installation was successful.

### Getting Your Clash of Clans API Token

To use the Clash of Clans API, you’ll need a token to authenticate your application. Follow these steps to get it:

1. Go to the **Clash of Clans API** site at [developer.clashofclans.com](https://developer.clashofclans.com).
2. Log in with your Supercell account.
3. On the main page, create a **new API Key**:
   - Add a brief description.
   - Enter the IP from which you’ll run the script (you can find your current IP by searching “my IP” on Google).
4. Copy the generated **API token** and save it, as you’ll need it to set up the script.

### Getting Your Clan Tag

1. Open the Clash of Clans app on your device.
2. Go to your clan’s page and copy the clan tag, which appears directly below the clan name and begins with the `#` symbol.
3. Write down this tag, as you’ll need it to set up the script.

### Configuring Text Files

The repository includes two text files in the `info_to_add` folder:

- **api_key.txt**: Paste your Clash of Clans API token here.
- **clan_tag.txt**: Paste your clan tag here.

To set up these files:

1. Open `info_to_add/api_key.txt` in a text editor and paste your API token into this file.
2. Open `info_to_add/clan_tag.txt` and paste your clan tag into this file.
3. Save both files.

**Note:** These files are included in `.gitignore`, so your credentials won’t be uploaded to GitHub if you make changes to them.

### Running the Scripts

To run the scripts, simply double-click on the `.py` file you want to execute. Ensure that the `api_key.txt` and `clan_tag.txt` files are correctly configured, as the scripts will use them for authentication and to retrieve clan data.

If you encounter issues with double-clicking, you can also run the scripts from the command line:

1. Open a terminal in the project folder.
2. Run the following command, replacing `script.py` with the name of the script file:

   ```bash
   python script.py

### Contributing

If you would like to contribute to this project:

1. Fork this repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Make your changes and commit them (`git commit -m "Add new feature"`).
4. Push your changes (`git push origin feature/new-feature`).
5. Open a Pull Request on GitHub.

Thank you for contributing to the CoC Scripts project!

