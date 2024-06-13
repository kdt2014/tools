# pip install scholarly pandas PySocks

import pandas as pd
import socks
import socket
from scholarly import scholarly

# 设置socks5代理
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 8080)
socket.socket = socks.socksocket

# 搜索关键词
search_query = scholarly.search_pubs('(intitle:"Plane Detection" OR intitle:"Plane Localization" OR intitle:"Standard Plane Localization" OR intitle:"Standard Plane Detection" OR intitle:"Standard Plane") intext:medical AND ultrasound')

# 存储结果
results = []

# 迭代搜索结果并存储
for i in range(100):  # 假设需要保存前100个结果
    try:
        pub = next(search_query)
        results.append({
            'title': pub['bib'].get('title', ''),
            'author': pub['bib'].get('author', ''),
            'pub_year': pub['bib'].get('pub_year', ''),
            'venue': pub['bib'].get('venue', ''),
            'abstract': pub['bib'].get('abstract', ''),
            'url': pub['pub_url'] if 'pub_url' in pub else ''
        })
    except StopIteration:
        break

# 创建DataFrame并保存为CSV文件
df = pd.DataFrame(results)
df.to_csv('scholar_results.csv', index=False)

print("结果已保存到 scholar_results.csv")
