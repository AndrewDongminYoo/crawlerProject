import json
import os

from pymongo import MongoClient

client = MongoClient()
db = client.get_database("cat")
col = db.get_collection("CatFood_test007")
data_path = os.path.join(os.curdir, "data")
files = [x for x in os.listdir(data_path) if x != "__pycache__"]


def upload(name=None):
    for fp in files:
        if name and name != fp:
            pass
        else:
            file_path = os.path.join(data_path, fp)
            with open(file=file_path, mode="r", encoding="utf8") as old:
                obj = json.load(old)
                for data in obj:
                    col.update_one({"url": data["url"]}, {"$set": data}, upsert=True)


def download():
    result = dict()
    for data in col.find({}, {"_id": False, "updated_at": False}):
        del data["analysis"]
        if data["brand"] + ".json" in result.keys():
            result[data["brand"] + ".json"].append(data)
        else:
            result[data["brand"] + ".json"] = [data]

    for key, value in result.items():
        file_path = os.path.join(data_path, key)
        with open(file=file_path, mode="w", encoding="utf8", newline="") as input_file:
            json.dump(value, input_file, allow_nan=False, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    upload()
    # download()
