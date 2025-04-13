import urllib.parse
import threading
import requests
import time
import os


def get_page(url):
    """获取网页内容."""
    response = requests.get(url)
    response.raise_for_status()  # 检查请求是否成功
    return response.content.decode('utf-8')


def pages_from_duitang(label):
    """从对特定标签进行搜索获取博客页面."""
    url_template = 'https://www.duitang.com/napi/blog/list/by_search/?kw={}&start={}'
    pages = []

    # 对标签进行URL编码
    label = urllib.parse.quote(label)

    # 遍历获取多页数据
    for start in range(0, 3600, 100):
        url = url_template.format(label, start)
        print("Fetching:", url)
        page = get_page(url)
        pages.append(page)
    return pages


href = "https://c-ssl.duitang.com/uploads/blog/202208/14/20220814191826_ca2e0.jpg"


def findall_pages(page, startpart, endpart):
    """在页面内容中提取特定内容."""
    urls = []
    end = 0

    while True:
        start = page.find(startpart, end)
        if start == -1:
            break
        start += len(startpart)
        end = page.find(endpart, start)
        urls.append(page[start:end])  # 提取并保存URL
    return urls


def pic_url_from_pages(pages):
    """从多个页面获取图片URL."""
    all_urls = []

    for page in pages:
        urls = findall_pages(page, 'path":"', '"')
        all_urls.extend(urls)  # 合并图片URL列表
    return all_urls


def pic_download(url, n, dir_path):
    """下载图片并保存到本地."""
    response = requests.get(url)
    response.raise_for_status()  # 检查请求是否成功

    # 保存图片
    path = dir_path + f"\\{n}.jpg"
    with open(path, 'wb') as file:
        file.write(response.content)


# 使用线程锁来限制同时进行的线程数量
thread_lock = threading.BoundedSemaphore(value=5)


def download_worker(url, n, dir_path):
    """工作线程：下载图片."""
    with thread_lock:  # 确保只有5个线程在同时运行
        try:
            print(f'正在下载第 {n} 张图片: {url}')
            pic_download(url, n, dir_path)
            time.sleep(2)  # 每下载一张图片，等待2秒
        except requests.RequestException as e:
            print(f"下载失败: {e}")


def main(label):
    """主函数，负责协调工作流."""
    try:
        # 判断文件夹是否存在
        dir_path = "D:\\program\\" + label
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        pages = pages_from_duitang(label)
        pic_urls = pic_url_from_pages(pages)

        threads = []
        # 使用多线程下载每张图片
        for n, url in enumerate(pic_urls, start=1):
            t = threading.Thread(target=download_worker, args=(url, n, dir_path))
            threads.append(t)
            t.start()

        # 等待所有线程完成
        for t in threads:
            t.join()

        print("所有图片下载完成。")

    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    main('杨幂')
