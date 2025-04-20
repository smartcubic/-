import requests
from bs4 import BeautifulSoup
import json
import re

def extract_url_from_share_text(share_text):
    """
    Extract the actual URL from a mobile share text.
    
    Args:
        share_text (str): The mobile share text containing the URL
        
    Returns:
        str: The extracted URL or None if not found
    """
    # Pattern to match URLs in the share text
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    
    # Find all URLs in the text
    urls = re.findall(url_pattern, share_text)
    
    # Return the first URL found (usually there's only one)
    return urls[0] if urls else None

def scrape_xiaohongshu(url):
    """
    Scrape content from a Xiaohongshu post URL.
    
    Args:
        url (str): The URL of the Xiaohongshu post
        
    Returns:
        dict: A dictionary containing the title, content, and media URLs (images or videos)
    """
    # Set headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.xiaohongshu.com/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1'
    }
    
    try:
        # Send GET request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title - using name="og:title" instead of property
        title_tag = soup.find('meta', {'name': 'og:title'})
        title = title_tag['content'] if title_tag else "Title not found"
        
        # Extract description/content - using name="description"
        desc_tag = soup.find('meta', {'name': 'description'})
        content = desc_tag['content'] if desc_tag else "Content not found"
        
        # Initialize result dictionary
        result = {
            'title': title,
            'content': content,
            'media_type': 'unknown',
            'media_urls': []
        }
        
        # Check for video content - specifically look for meta name="og:video"
        video_tag = soup.find('meta', {'name': 'og:video'})
        
        if video_tag and video_tag.get('content'):
            # This is a video post
            video_url = video_tag.get('content')
            result['media_urls'].append(video_url)
            result['media_type'] = 'video'
            
            # Also check for additional video URLs in the same format
            additional_video_tags = soup.find_all('meta', {'name': 'og:video'})
            for tag in additional_video_tags[1:]:  # Skip the first one as we already added it
                if tag.get('content') and tag.get('content') not in result['media_urls']:
                    result['media_urls'].append(tag.get('content'))
        else:
            # This is an image post
            image_tags = soup.find_all('meta', {'name': 'og:image'})
            image_urls = [tag['content'] for tag in image_tags] if image_tags else []
            result['media_urls'] = image_urls
            result['media_type'] = 'image'
        
        # Debug information
        print("\nDebug Information:")
        print(f"HTML Length: {len(response.text)}")
        print(f"Detected media type: {result['media_type']}")
        print(f"Number of media URLs found: {len(result['media_urls'])}")
        
        return result
        
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    # Get input from user
    user_input = input("Please enter the Xiaohongshu URL or mobile share text: ")
    
    # Check if the input is a mobile share text
    if "小红书" in user_input and "http" in user_input:
        url = extract_url_from_share_text(user_input)
        if url:
            print(f"\nExtracted URL: {url}")
        else:
            print("Could not extract URL from the share text.")
            return
    else:
        url = user_input
    
    # Scrape the content
    result = scrape_xiaohongshu(url)
    
    if result:
        print("\nResults:")
        print(f"Title: {result['title']}")
        print(f"Content: {result['content']}")
        print(f"Media Type: {result['media_type']}")
        
        if result['media_type'] == 'video':
            print("\nVideo URLs:")
            for i, video_url in enumerate(result['media_urls'], 1):
                print(f"{i}. {video_url}")
        else:
            print("\nImage URLs:")
            for i, img_url in enumerate(result['media_urls'], 1):
                print(f"{i}. {img_url}")

if __name__ == "__main__":
    main() 