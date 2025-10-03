import os
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def get_last_update(url):
    try:
        print("Getting last update date...")
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        tag = soup.find("i")
        date_str = tag.text.replace("Last updated:", "").strip()

        return datetime.strptime(date_str, "%d/%m/%y")

    except requests.exceptions.RequestException:
        return None


def get_file_last_modified(filepath):
    if os.path.exists(filepath):
        time = os.path.getmtime(filepath)
        return datetime.fromtimestamp(time)

    return None


def is_updated(url, filepath):
    site_date = get_last_update(url)
    file_date = get_file_last_modified(filepath)

    if site_date is None:
        print("Could not get update date from the website.")
        return True

    if file_date is None or site_date > file_date:
        return False
    
    return True


def download_csv(league_config: dict):
    DATA_FOLDER = Path("data")
    DATA_FOLDER.mkdir(exist_ok=True)

    url = league_config["csv_url"]

    try:
        r = requests.get(url)
        r.raise_for_status()

        name = league_config["file_name"]

        download_path = DATA_FOLDER / name
        with open(download_path, "wb") as f:
            f.write(r.content)

        print("CSV downloaded!")
        return

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")


def update_csv(league_config: dict):
    if is_updated(league_config["check_url"], league_config["filepath"]):
        print("CSV is updated.")
        return

    print("Update avaliable!")
    download_csv(league_config)

    return
