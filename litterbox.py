#!/bin/python
import json
import random
import requests
import argparse
import re


NEXTCLOUD = "nextcloud.cactusgroup.space"
ALLOWED_CHARS = [chr(x) for x in range(65, 65 + 26)] + [chr(x) for x in range(97, 97 + 26)] + [chr(x) for x in range(48, 48 + 10)]


def upload_litter(location, time="1h"):
    if not time in ("1h", "12h", "24h", "72h"):
        raise ValueError("Allowed times: 1h, 12h, 24h, 72h")
    resp = requests.post(
            "https://litterbox.catbox.moe/resources/internals/api.php",
            data={
                "reqtype": "fileupload",
                "time": time
            },
            files={"fileToUpload": open(location, "rb")}
    )
    print(resp.text)


def upload_catbox(location, u_hash=None):
    if u_hash is None:
        data = {"reqtype": "fileupload"}
    else:
        data = {"reqtype": "fileupload", "userhash": u_hash}
    resp = requests.post(
            "https://catbox.moe/user/api.php",
            data=data,
            files={"fileToUpload": open(location, "rb")}
    )
    print(resp.text)


class Nextcloud:
    def __init__(self, domain, username, password):
        self.session = requests.Session()
        self.domain = domain
        self.username = username
        self.password = password

    def get_login_token(self):
        resp = self.session.get(f"https://{self.domain}/login")
        if resp.status_code != 200:
            raise Exception
        token = re.search("requesttoken\=\".*\"", resp.text).group(0)[14:-1]
        if token is None:
            raise Exception
        return token

    def login(self):
        resp = self.session.post(
            f"https://{self.domain}/login",
            data={
                "user": self.username,
                "password": self.password,
                "timezone": "Europe/Rome",
                "timezone_offset": 2,
                "requesttoken": self.get_login_token()
            }
        )
        if resp.status_code != 200:
            raise Exception

    def get_upload_token(self):
        resp = self.session.get(f"https://{self.domain}/apps/files/?dir=/")
        if resp.status_code != 200:
            raise Exception
        token = re.search("requesttoken\=\".*\"", resp.text).group(0)[14:-1]
        if token is None:
            raise Exception
        return token

    def upload_nextcloud(self, fd, name):
        resp = self.session.put(
            f"https://{self.domain}/remote.php/webdav/{name}",
            fd,
            headers={
                "requesttoken": self.get_upload_token()
            }
        )
        if resp.status_code != 201:
            raise Exception

    def get_share_link(self, name):
        resp = self.session.post(
            f"https://{self.domain}/ocs/v2.php/apps/files_sharing/api/v1/shares",
            json={
                "attributes": "[]",
                "path": f"/{name}",
                "shareType": 3
            },
            headers={
                "requesttoken": self.get_upload_token(),
                "accept": "application/json"
            }
        )
        data = json.loads(resp.text)
        print(data["ocs"]["data"]["url"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", metavar="FILE",
            help="The file to upload")
    parser.add_argument("--temp", "-t", action="store_true",
            help="If used the file will be uploaded on litterbox")
    parser.add_argument("--time",
            help="If --temp is used --time specifies for how long the file will be up. Default is 1h")
    parser.add_argument("--nextcloud", "-n", action="store_true",
            help="If used the file will be uploaded on nextcloud")
    parser.add_argument("--username", "-u",
            help="Used to specify nextcloud username")
    parser.add_argument("--password", "-p",
            help="Used to specify nextcloud password")
    args = parser.parse_args()
    if args.temp:
        if args.time:
            upload_litter(args.file, args.time)
        else:
            upload_litter(args.file)
    elif args.nextcloud:
        n = Nextcloud(NEXTCLOUD, args.username, args.password)
        n.login()
        name = "".join([random.choice(ALLOWED_CHARS) for x in range(16)]) + "." + args.file.split(".")[-1]
        n.upload_nextcloud(open(args.file, "rb"), name)
        n.get_share_link(name)
    else:
        if args.hash:
            upload_catbox(args.file, args.hash)
        else:
            upload_catbox(args.file)
