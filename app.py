from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_amazon(url):
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

def scrape_flipkart(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        try:
            # Extract product title
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

            return {
                "title": title,
                "material": material if material else "Material information not found."
            }
        except AttributeError:
            return {"error": "Could not extract some details. The structure might have changed."}
    else:
        return {"error": f"Failed to fetch the page. Status code: {response.status_code}"}

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get("url")

    if "amazon" or "amzn" in url:
        product_details = scrape_amazon(url)
    elif "flipkart" in url:
        product_details = scrape_flipkart(url)
    else:
        return jsonify({"error": "Unsupported URL. Only Amazon and Flipkart are supported."})

    return jsonify(product_details)

if __name__ == '__main__':
    app.run(debug=True)