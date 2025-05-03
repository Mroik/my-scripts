#!/bin/sh
curl -L "https://c.xkcd.com/random/comic/" 2>/dev/null | grep -o -P "(?<=>)https://imgs\.xkcd\.com/comics/.*\.png" | xargs firefox
