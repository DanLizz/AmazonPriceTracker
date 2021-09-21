from bs4 import BeautifulSoup
import requests
import smtplib

# Email details
my_email = "youremail@domain.com"
my_password = "yourp4SSW0RD"
# Receipient email
your_mail = "receipientemail@domain.com"

# Link for Amazon product page
URL = "https://www.amazon.com/Oculus-Quest-Advanced-All-One-Virtual/dp/B099VMT8VZ/ref=lp_16225009011_1_1?dchild=1"
response = requests.get(URL, headers={"Accept-Language": "en-US,en;q=0.9,ml;q=0.8", "Accept-Encoding": "gzip, deflate",
                                      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"})
webpage = response.content
encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None

soup = BeautifulSoup(webpage, "html.parser", from_encoding="encoding")
product_name = soup.find(name="span", id="productTitle").getText().encode('ascii', 'ignore').strip()
price = float(soup.find(name="span", id="priceblock_ourprice").getText().split('$')[1])

print(product_name)
print(price)



# Function to send email when price is lower
def send_notification_mail():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email, to_addrs=your_mail,
                            msg=f"Subject:Amazon Price Alert\n\n{product_name} is now ${price}.\nBuy now at {URL}!")


# Decision to send mail when price is lower
if price < 300:
    send_notification_mail()
