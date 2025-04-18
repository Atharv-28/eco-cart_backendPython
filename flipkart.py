import requests
from bs4 import BeautifulSoup

def scrape_flipkart(url):
    # Set up headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    # Send a GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        try:
            # Extract product details
            title = soup.find("span", {"class": "VU-ZEz"}).get_text(strip=True)  # Product title
            

             # Extract image URL
            img_tag = soup.find("img", {"class": "DByuf4 IZexXJ jLEJ7H"})
            img_url = img_tag["src"] if img_tag else "Image not found."

            # Extract material information
            material = None
            spec_tables = soup.find_all("table", {"class": "_0ZhAN9"})  # Find all tables with the same class
            for spec_table in spec_tables:
                rows = spec_table.find_all("tr")
                for row in rows:
                    header = row.find("td", {"class": "+fFi1w col col-3-12"})
                    value = row.find("td", {"class": "Izz52n col col-9-12"})
                    if header and value:
                        text = header.get_text(strip=True).lower()
                        if "material" in text or "fabric" in text:
                            # Use .find() to go directly into <li> tag if it exists
                            li_tag = value.find("li")
                            if li_tag:
                                material = li_tag.get_text(strip=True)
                            else:
                                material = value.get_text(strip=True)
                            break
                if material:  # Break outer loop if material is found
                    break

            return {
                "title": title,
                "image_url": img_url,
                "material": material if material else "Material information not found."
            }
        except AttributeError:
            return {"error": "Could not extract details."}
    else:
        return {"error": f"Failed to fetch the page. Status code: {response.status_code}"}

# URL of the product page
url = "https://www.flipkart.com/jayshri-handicrafts-trophy-school-student-appreciating-best/p/itm524bf960f4aee?pid=TMEGUXCREWJMXZ4Q&lid=LSTTMEGUXCREWJMXZ4Q023YWN&marketplace=FLIPKART&fm=factBasedRecommendation%2FrecentlyViewed&iid=R%3Arv%3Bpt%3App%3Buid%3Acdb3ad99-1c88-11f0-b1c1-6f084f2e2284%3B.TMEGUXCREWJMXZ4Q&ppt=pp&ppn=pp&ssid=uzhru83uao0000001745003419804&otracker=pp_reco_Recently%2BViewed_6_39.productCard.RECENTLY_VIEWED_Jayshri%2Bhandicrafts%2BTrophy%2Bfor%2BSchool%2BStudent%2BAppreciating%2BBest%2Bstudent%2BTrophy_TMEGUXCREWJMXZ4Q_factBasedRecommendation%2FrecentlyViewed_5&otracker1=pp_reco_PINNED_factBasedRecommendation%2FrecentlyViewed_Recently%2BViewed_DESKTOP_HORIZONTAL_productCard_cc_6_NA_view-all&cid=TMEGUXCREWJMXZ4Q"

# Call the function and print the result
result = scrape_flipkart(url)
print(result)