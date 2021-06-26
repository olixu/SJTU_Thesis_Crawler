#!/bin/bash

python downloader.py --pages '1-2' &
python downloader.py --pages '3-4' &
python downloader.py --pages '5-6' &
python downloader.py --pages '7-8' &
python downloader.py --pages '9-10' &
python downloader.py --pages '11-12' &
python downloader.py --pages '13-14' &
python downloader.py --pages '15-16' &
python downloader.py --pages '17-18' &

wait