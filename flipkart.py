import requests
from bs4 import BeautifulSoup

# URL of the product page
url = "https://www.flipkart.com/milton-handy-850-stainless-steel-780-ml-bottle/p/itm81ea99cf34c09?pid=BOTGQTHTSGZYWXGV&cmpid=product.share.pp&_refId=PP.32d01e52-6523-4c65-bdba-3cbf372fd4ce.BOTGQTHTSGZYWXGV&_appId=CL"

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
                        print("Material:", material)
                        break
            if material:  # Break outer loop if material is found
                break

        print("Title:", title)
        print("Material:", material if material else "Material information not found.")
    except AttributeError:
        print("Could not extract some details. The structure might have changed.")
else:
    print(f"Failed to fetch the page. Status code: {response.status_code}")