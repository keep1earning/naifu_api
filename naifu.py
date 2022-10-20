import uuid
import getopt
import requests
import json
import base64
import sys
def base64_2_img(base64_str):
    name = str(uuid.uuid4())
    with open(name + ".png", "wb") as fh:
        fh.write(base64.decodebytes(base64_str))
    return name
def query_dl(domain, protocol, word, width, height, url):
    payload = json.dumps({
      "prompt": "masterpiece, best quality, " + word,
      "width": width,
      "height": height,
      "scale": 12,
      "sampler": "k_euler_ancestral",
      "steps": 28,
      "n_samples": 1,
      "ucPreset": 0,
      "uc": "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry"
    })
    headers = {
      'authority': domain,
      'accept': '*/*',
      'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
      'authorization': 'Bearer',
      'content-type': 'application/json',
      'dnt': '1',
      'origin': protocol + domain,
      'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    img_data = str.encode(response.text[27:])
    name = base64_2_img(img_data)
    print("Image saved as " + name + ".png")
def printUsage():
    print("Usage: Default server is 127.0.0.1:6969, with http protocol, -w to add words, heigh with -h , width with -wh, changing protocol with -p (http:// or https://), changing server with -d (127.0.0.1:6969 or ****.com)")
def main():
    domain = "127.0.0.1:6969"
    protocol = "http://"
    word = ""
    width = "512"
    height = "512"
    try:
        opts, args = getopt.getopt(sys.argv[1:],"p:d:w:h:wh:",["protocol=","domain=","word=","height=","width=", "help="])
    except getopt.GetoptError:
        printUsage()
        sys.exit(-1)
    for opt, arg in opts:
        if opt in ("--help"):
            printUsage()
            sys.exit(0)
        elif opt in ("-p"):
            protocol = arg
        elif opt in ("-d"):
            domain = arg
        elif opt in ("-w"):
            word = arg
        elif opt in ("-h"):
            height = arg
        elif opt in ("-wh"):
            width = arg
    url = protocol + domain + "/generate-stream"
    return domain, protocol, word, width, height, url
if __name__ == "__main__":
    domain, protocol, word, width, height, url = main()
    try:
        query_dl(domain, protocol, word, width, height, url)
    except requests.exceptions.ConnectionError:
        printUsage()
        sys.exit(-1)
