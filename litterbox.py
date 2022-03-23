#!/bin/python
import requests
import argparse

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", metavar="FILE",
            help="The file to upload")
    parser.add_argument("--temp", "-t", action="store_true",
            help="If used the file will be uploaded on litterbox")
    parser.add_argument("--time",
            help="If --temp is used --time specifies for how long the file will be up. Default is 1h")
    parser.add_argument("--hash", "-u",
            help="The user hash to use (ignored when using --temp)")
    args = parser.parse_args()
    if args.temp:
        if args.time:
            upload_litter(args.file, args.time)
        else:
            upload_litter(args.file)
    else:
        if args.hash:
            upload_catbox(args.file, args.hash)
        else:
            upload_catbox(args.file)
