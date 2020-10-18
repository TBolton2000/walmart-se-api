import io
import simplejson as json

dir = "C:\\Users\\TBolt\\projects\\hackathon\\walmart-web-crawler\\"
files = ["data_478_entertainment.json", "data_1429_professional.json", "data_4376_fashion.json",
         "everyday.json", "home.json", "other.json"]

output_file = io.open("all_data.json", "w", encoding="utf-8")
output_file.write("[")
for file in files:
    with io.open(dir+file, "r", encoding="utf-8") as read_file:
        output_file.write(read_file.read()[1:-1])
        if file != file[-1]:
            output_file.write(",")

output_file.write("]")

output_file.close()
