import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup


def get_last_update(url):
    try:
        print("getting last update")
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        tag = soup.find("i")
        date_str = tag.text.replace("Last updated:", "").strip()

        return datetime.strptime(date_str, "%d/%m/%y").date()

    except requests.exceptions.RequestException:
        return None


def get_file_last_modified(filepath):
    if not os.path.exists(filepath):
        return None

    time = os.path.getmtime(filepath)
    return datetime.fromtimestamp(time).date()


def is_updated(url, filepath):
    siteDate = get_last_update(url)
    fileDate = get_file_last_modified(filepath)

    if fileDate is None or siteDate > fileDate:
        return False
    return True


def download_csv(url):
    r = requests.get(url)
    r.raise_for_status()

    if "BRA" in url:
        name = "brasileirao"
    else:
        name = "premierleague"
    with open(name + ".csv", "wb") as f:
        f.write(r.content)

    print("CSV downloaded!")
    return


def update_csv(url, filepath):
    if is_updated(url, filepath):
        print("CSV is updated.")
        return

    download_csv(url)

    return
