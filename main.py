import string
import re
import requests
import os
from bs4 import BeautifulSoup

from configuration import IMAGES_FOLDER

alphabet = string.ascii_lowercase
rootUrl = "https://www.shugiin.go.jp"


def get_house_of_representatives():
    for character in alphabet:
        list_of_members_page = f"{rootUrl}/internet/itdb_english.nsf/html/statics/member/mem_{character}.htm"

        page = requests.get(list_of_members_page)

        if page.status_code == 404:
            print("No member under %s" % character)
            continue

        soup = BeautifulSoup(page.content, "html.parser")
        member_urls = soup.findAll('a', {'href': re.compile(".*member/e.*")})

        for member_url in member_urls:
            member_page = requests.get(f"{rootUrl}{member_url['href']}")
            soup = BeautifulSoup(member_page.content, "html.parser")

            profile_image = soup.find('img', {'src': re.compile(".*/profile/.*")})

            print(profile_image)

            with open(f"{IMAGES_FOLDER}\\{profile_image['alt']}.jpg", "wb") as image:
                image.write(requests.get(f"{rootUrl}{profile_image['src']}").content)
            image.close()


if not os.path.exists(IMAGES_FOLDER):
    os.mkdir(IMAGES_FOLDER)

    get_house_of_representatives()
