import datetime
import json
import sys
from sqlite3.dbapi2 import Date


class Config:

    def __init__(self):
        pass

    def get_config(self, file, field):
        if file == "auth":
            path = "utils/config_auth.json"
        elif file == "url":
            path = "utils/url.json"
        elif file == "status":
            path = "utils/status_id.json"
        elif file == "pack":
            path = "utils/pack.json"
        with open(path, "r") as fs:
            fields = json.load(fs)
        return fields[field]

    def save_regress_config(self, link):
        date_end = Date.today() + datetime.timedelta(days=7)
        buf_str = {'link' : link, 'end' : str(date_end)}
        with open("utils/regress.json", "w") as fs:
            fs.write(json.dumps(buf_str))

    def compare_regress_data(self):
        with open("utils/regress.json", "r") as fs:
            date_end = json.load(fs)["end"]

            end_buf = date_end.split('-')
            start_buf = str(Date.today()).split('-')

            end = datetime.date(int(end_buf[0]), int(end_buf[1]), int(end_buf[2]))
            start = datetime.date(int(start_buf[0]), int(start_buf[1]), int(start_buf[2]))
            compare = end - start

            return str(compare).split()[0]

    def translate_arv(self):
        with open(self, 'r') as fs:
            fields = json.load(fs)
        return fields