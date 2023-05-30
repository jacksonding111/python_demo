import requests

m_url = 'https://webfs.ali.kugou.com/202305301209/a0c1dfee1e00e6936d72a3c3ab68dd00/part/0/960111/KGTX/CLTX001' \
        '/clip_bfbdd3df47727b701d4480ea36a8f73b.mp3'

headers = {
    ' User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 '
        'Safari/537.36'
}

m_response = requests.get(m_url, headers=headers)
print(m_response)
with open('zzz.mp3', 'wb') as f:
    f.write(m_response.content)
