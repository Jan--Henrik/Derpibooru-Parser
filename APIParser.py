#!/bin/python3.5
import urllib.request
import json
import sys

tags = sys.argv[1]
filename = sys.argv[2]
config = sys.argv[3]

class APIParser:
    def __init__(self, taglist="", filename="", config=""):

        self.tagList = taglist
        self.config = config

        self.imgCounter = 0
        self.fileCounter = 0
        self.filePrefix = filename
        self.fileSuffix = ".txt"

        self.imgList = []
        self.imgPage = 0
        self.dataTrue = True

        with open(self.config) as target:
            config = target.read().replace("\t", "")
        config_dict = {}

        for element in config.split("\n"):
            tmp_dict = {element[:element.find(':')]: element[element.find(':') + 1:]}
            config_dict.update(tmp_dict)

        self.urlStr = str(config_dict['urlStr'])
        self.hereticStr = str(config_dict['hereticStr'])
        self.urlSearchStr = str(config_dict['urlSearchStr'])
        self.pageStr = str(config_dict['pageStr'])
        self.keyStr = str(config_dict['keyStr'])

        self.key = str(config_dict['key'])

        self.fileSize = int(config_dict['fileSize'])
        self.imgSize = str(config_dict['imgSize'])

    def run(self):
        while self.dataTrue:
            self.download()
            self.save()
        self.exit()

    def download(self):
        self.imgList = []
        while True:
            url = self.urlStr + self.pageStr + str(self.imgPage) + self.hereticStr + self.urlSearchStr + self.tagList + self.hereticStr + self.keyStr + self.key
            self.page = urllib.request.urlopen(url).read()
            self.page = self.page.decode("utf-8")

            if len(self.page) <= 100:
                self.dataTrue = False
                break
            data = json.loads(self.page)
            cnt = 0

            while True:
                try:
                    __tmp = data['search'][cnt]['representations'][self.imgSize]
                    cnt += 1
                    self.imgList.append(__tmp)
                except:
                    break
            sys.stderr.write('%s Images\r' % (len(self.imgList))),
            sys.stderr.flush()
            self.imgPage += 1

    def save(self):
        target = open("data/%s%d%s" % (self.filePrefix, self.fileCounter, self.fileSuffix),'a+')
        for img in self.imgList:
            if self.imgCounter == self.fileSize:
                self.imgCounter = 0
                self.fileCounter += 1
                target.close()
                target = open("data/%s%d%s" % (self.filePrefix, self.fileCounter, self.fileSuffix),'a+')
            target.write(img + "\n")
            target.flush()
            self.imgCounter += 1
        print(self.imgCounter + (self.fileCounter * self.fileSize))
        target.close()

    def exit(self):
        exit()


if __name__ == "__main__":

    API = APIParser(tags, filename, config)
    API.run()

    while 42:
        try:
            pass
        except KeyboardInterrupt:
            API.exit()
            break
