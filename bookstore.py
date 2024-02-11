import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher
import asyncio

# Function to scrape data from the website
async def scrape_website():
    # URL of the webpage to scrape
    url = "https://ethio-bookstore.com/product-category/amharic-books-%E1%8B%A8%E1%8A%A0%E1%88%9B%E1%88%AD%E1%8A%9B-%E1%88%98%E1%8C%BD%E1%88%90%E1%8D%8D%E1%89%B5/"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all the book titles and images
        products = soup.find_all("li", class_="product")
        
        # Initialize an empty list to store scraped data
        scraped_data = []

        # Extract the titles, images, and prices
        for product in products:
            # Extract book title
            title = product.find("h2", class_="woocommerce-loop-product__title").text.strip()

            # Extract image URL
            image_url = product.find("img", class_="attachment-woocommerce_thumbnail").get("src")

            # Extract price if available
            price_elem = product.find("span", class_="woocommerce-Price-amount amount")
            price = price_elem.text.strip() if price_elem else "N/A"

            # Append scraped data to the list
            scraped_data.append({"Title": title, "Image URL": image_url, "Price": price})

        return scraped_data
    else:
        print("Failed to retrieve the webpage")
        return None

# Function to send message to Telegram channel
async def send_to_telegram_channel(item):
    # Telegram bot token
    bot_token = '6861488044:AAHMMhAq1rN8OjfJQogkHSyzOm7_NUjapBM'

    # Initialize Telegram bot
    bot = Bot(token=bot_token)

    # Telegram channel ID
    channel_id = '@Booksofethiopiaa'

    # Format scraped data as a message
    message = ""
    message += f"Title: {item['Title']}\n"
    message += f"Image URL: {item['Image URL']}\n"
    message += f"Price: {item['Price']}\n\n"

    # Send message to the channel
    await bot.send_message(chat_id=channel_id, text=message)

# Main function
async def main():
    # Scrape data from the website
    scraped_data = await scrape_website()

    if scraped_data:
        # Send each scraped data to Telegram channel
        for item in scraped_data:
            await send_to_telegram_channel(item)


if __name__ == "__main__":
    asyncio.run(main())

