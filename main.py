import string
import re
import requests
import os
from bs4 import BeautifulSoup
import urllib.parse
from slugify import slugify

from configuration import HOUSE_OF_REPRESENTATIVES_IMAGES_FOLDER, HOUSE_OF_COUNCILLORS_IMAGES_FOLDER

ALPHABET = string.ascii_lowercase


def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path


def get_house_of_representatives():
    root_url = "https://www.shugiin.go.jp"

    for character in ALPHABET:
        list_of_members_page = f"{root_url}/internet/itdb_english.nsf/html/statics/member/mem_{character}.htm"

        page = requests.get(list_of_members_page)

        if page.status_code == 404:
            print("No member under %s" % character)
            continue

        soup = BeautifulSoup(page.content, "html.parser")
        member_urls = soup.findAll('a', {'href': re.compile(".*member/e.*")})

        for member_url in member_urls:
            member_page = requests.get(f"{root_url}{member_url['href']}")
            soup = BeautifulSoup(member_page.content, "html.parser")

            profile_image = soup.find('img', {'src': re.compile(".*/profile/.*")})

            print(profile_image)

            with open(f"{HOUSE_OF_REPRESENTATIVES_IMAGES_FOLDER}\\{profile_image['alt']}.jpg", "wb") as image:
                image.write(requests.get(f"{root_url}{profile_image['src']}").content)
            image.close()


def get_house_of_councillors():
    root_url = "https://www.sangiin.go.jp/japanese/joho1/kousei/eng/members/index.htm"

    page = requests.get(root_url)

    soup = BeautifulSoup(page.content, "html.parser")
    member_urls = soup.findAll('a', {'href': re.compile(".*profile/.*")})

    for member_url in member_urls:
        member_page_url = urllib.parse.urljoin(root_url, member_url['href'])
        member_page = requests.get(member_page_url)
        if member_page.status_code == 404:
            print(f"No member under {member_page}")
            continue

        soup = BeautifulSoup(member_page.content, "html.parser")

        profile_image = soup.find('img', {'src': re.compile(".*/photo/.*")})

        sanitised_filename = uniquify(os.path.join(HOUSE_OF_COUNCILLORS_IMAGES_FOLDER, f"{slugify(profile_image['alt'])}.jpg"))
        with open(sanitised_filename, "wb") as image:
            requested_image = requests.get(urllib.parse.urljoin(member_page_url, profile_image['src']))
            if requested_image.status_code == 404:
                print(f"No image under {requested_image}")

            image.write(requested_image.content)
        image.close()

        print(f"Got {sanitised_filename}")


if not os.path.exists(HOUSE_OF_REPRESENTATIVES_IMAGES_FOLDER):
    os.mkdir(HOUSE_OF_REPRESENTATIVES_IMAGES_FOLDER)

    get_house_of_representatives()

if not os.path.exists(HOUSE_OF_COUNCILLORS_IMAGES_FOLDER):
    os.mkdir(HOUSE_OF_COUNCILLORS_IMAGES_FOLDER)

    get_house_of_councillors()
