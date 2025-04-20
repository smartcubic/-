# Xiaohongshu Scraper API

A FastAPI-based API for scraping content from Xiaohongshu (小红书) posts.

## Features

- Extract title, content, and media URLs (images or videos) from Xiaohongshu posts
- Support for both direct URLs and mobile share text
- Automatically detect whether a post contains images or videos

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the API

Start the API server:

```bash
python xiaohongshu_api.py
```

The API will be available at `http://localhost:8000`.

### API Endpoints

#### GET /

Returns information about the API.

#### POST /scrape

Scrapes content from a Xiaohongshu URL.

**Request Body:**

```json
{
  "url": "https://www.xiaohongshu.com/explore/..."
}
```

Or with mobile share text:

```json
{
  "url": "15 青哥儿的🍠发布了一篇小红书笔记，快来看吧！ 😆 Hv4AGTICbgxfrIV 😆 http://xhslink.com/a/PHXDnnbscVEab，复制本条信息，打开【小红书】App查看精彩内容！"
}
```

**Response:**

```json
{
  "title": "安溥 湖州芒禾音乐节 2025.4.19 - 小红书",
  "content": "我在你眼里看尽了相恋的年代 曾经的黑白 此刻灿烂 #安溥",
  "media_type": "image",
  "media_urls": [
    "http://sns-webpic-qc.xhscdn.com/202504201146/dfa3bc1b221eb7363605929d2bf25aaf/1040g00831gf66j1a3s004a4ksf36rbc87sitl30!nd_dft_wlteh_webp_3",
    "..."
  ]
}
```

For video posts:

```json
{
  "title": "《秦皇岛》："站在能分割世界的桥"",
  "content": "听了无数次收藏夹里的高雄潮水箴言《秦皇岛》cover，今天终于听到现场版了[哭惹R][哭惹R][哭惹R]没有想到第一次听现场版就是安溥的版本[皱眉R][皱眉R]20250412·南京#安溥 #焦安溥 #潮水箴言 #潮水箴言南京 #万能青年旅店 #秦皇岛 #张悬",
  "media_type": "video",
  "media_urls": [
    "https://sns-video-qc.xhscdn.com/stream/1/110/259/01e7fb16351ab8d201037003962cd5566a_259.mp4?sign=85abcbf42ba06f86f5a83b44aaaca5d6&t=680920f5"
  ]
}
```

### API Documentation

FastAPI automatically generates interactive API documentation. Visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Example Usage with curl

```bash
curl -X POST "http://localhost:8000/scrape" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.xiaohongshu.com/explore/67fa74b7000000001c03dc63"}'
```

## Example Usage with Python

```python
import requests

url = "http://localhost:8000/scrape"
data = {
    "url": "https://www.xiaohongshu.com/explore/67fa74b7000000001c03dc63"
}

response = requests.post(url, json=data)
print(response.json())
``` 