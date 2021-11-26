from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import urllib.request
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get('http://127.0.0.1:5500/index.html')
driver.set_window_position(3500, 0)
driver.maximize_window()

driver.implicitly_wait(1)

imageCaptcha = driver.find_element(By.ID, 'image')
srcImage = imageCaptcha.get_attribute('src')

urllib.request.urlretrieve(srcImage, "captcha.png")
image = Image.open('captcha.png')

image = image.filter(ImageFilter.MedianFilter)
enhancer = ImageEnhance.Contrast(image)

image = enhancer.enhance(4)

image = image.convert('1')

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

reponse = pytesseract.image_to_string(image)
print(reponse)

inputReponse = driver.find_element(By.NAME, 'reponse')
inputReponse.clear()
inputReponse.send_keys(reponse)

valider = driver.find_element(By.XPATH, '//input[@type="button"]')
valider.send_keys(Keys.ENTER)

user_choice = input('Cliquer sur ENTER pour stopper')
if not user_choice:
    print('Processus stoppé')
quit()
