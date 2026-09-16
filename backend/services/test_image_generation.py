import asyncio

from .openai_service import generate_thumbnail
from .imagekit_service import upload_file

async def main():
    image_bytes = await generate_thumbnail(
        prompt="Create a YouTube thumbnail",
        style_prompt="Bold, colorful, professional YouTube thumbnail",
        headshot_url="YOUR_HEADSHOT_URL"
    )

    with open("test_thumbnail.png", "wb") as f:
        f.write(image_bytes)
    
    url = upload_file(
        image_bytes,
        "test_thumbnail.png",
        "thumbnails"
    )

    print("ImageKit URL:", url)
    print("Thumbnail generated!")

asyncio.run(main())