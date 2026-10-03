import requests
from bs4 import BeautifulSoup
import csv
import time

# Website URL
URL = "https://books.toscrape.com/"

# Send request to website
response = requests.get(URL)

# Check whether website is accessible
if response.status_code != 200:
    print("Failed to access website")
    exit()

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Store scraped data
books = []

# Find all book containers
book_items = soup.find_all("article", class_="product_pod")

print("Starting Web Scraping...\n")

for book in book_items:

    # Book title
    title = book.h3.a["title"]

    # Price
    price = book.find("p", class_="price_color").text.strip()

    # Availability
    availability = book.find(
        "p", class_="instock availability"
    ).text.strip()

    # Rating
    rating = book.find("p", class_="star-rating")

    rating_class = rating.get("class")

    if len(rating_class) > 1:
        rating_value = rating_class[1]
    else:
        rating_value = "Not Available"

    # Book URL
    book_url = book.h3.a["href"]

    # Store data
    books.append([
        title,
        price,
        availability,
        rating_value,
        book_url
    ])

    print("Title:", title)
    print("Price:", price)
    print("Availability:", availability)
    print("Rating:", rating_value)
    print("-" * 50)

    time.sleep(0.2)


# Create CSV file
with open(
    "products.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    # CSV Header
    writer.writerow([
        "Book Title",
        "Price",
        "Availability",
        "Rating",
        "Book URL"
    ])

    # Write scraped data
    writer.writerows(books)


print("\nWeb Scraping Completed Successfully!")
print("Total Books Scraped:", len(books))
print("Dataset saved as: products.csv")