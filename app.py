from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_product_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        try:
            title = soup.find("span", {"id": "productTitle"}).get_text(strip=True)
            brand = soup.find("a", {"id": "bylineInfo"}).get_text(strip=True)
            features = soup.find("div", {"id": "feature-bullets"}).get_text(strip=True)

            material = None
            material_row = soup.find("tr", {"class": "a-spacing-small po-material"})
            if material_row:
                material = material_row.find("td", {"class": "a-span9"}).get_text(strip=True)

            if not material:
                tech_details_table = soup.find("table", {"id": "productDetails_techSpec_section_1"})
                if tech_details_table:
                    rows = tech_details_table.find_all("tr")
                    for row in rows:
                        header = row.find("th", {"class": "prodDetSectionEntry"})
                        value = row.find("td", {"class": "prodDetAttrValue"})
                        if header and value and "Material" in header.get_text(strip=True):
                            material = value.get_text(strip=True)
                            break

            return {
                "title": title,
                "brand": brand,
                "features": features,
                "material": material if material else "Material information not found."
            }
        except AttributeError:
            return {"error": "Could not extract some details. The structure might have changed."}
    else:
        return {"error": f"Failed to fetch the page. Status code: {response.status_code}"}

@app.route('/scrape', methods=['GET', 'POST'])  # Allow both GET and POST
def scrape():
    url = "https://amzn.in/d/10J9AVw"
    product_details = scrape_product_details(url)
    return jsonify(product_details)

if __name__ == '__main__':
    app.run(debug=True)