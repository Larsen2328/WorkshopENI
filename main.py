from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import urllib.request
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

# *** CHARGEMENT DU DRIVER ET CONNEXION AU SITE WEB CIBLE ***

# Chargement du driver chrome pour Selenium
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Obtention de l'url
driver.get('http://127.0.0.1:5500/index.html')

# Affichage écran de droite (Si nécessaire)
# driver.set_window_position(3500, 0)
# Plein écran
driver.maximize_window()
# Temps de pause (lié au JS du site web pour l'affichage du code)
driver.implicitly_wait(1)

# *** RECUPERATION DE L'IMAGE DU CAPTCHA ***

# On trouve l'élément HTML de l'image grâce à son id
imageCaptcha = driver.find_element(By.ID, 'image')
# On récupère l'uri de la source de l'image
srcImage = imageCaptcha.get_attribute('src')
# On stocke l'image récupérée à la racine du projet
urllib.request.urlretrieve(srcImage, "captcha.png")
# On "ouvre" cette image afin de la traiter
image = Image.open('captcha.png')

# *** AMELIORATION DE L'IMAGE ***

# On applique un filtre dessus
image = image.filter(ImageFilter.MedianFilter)
# On essaie d'améliorer le contraste
enhancer = ImageEnhance.Contrast(image)
# On applique un coefficient pour améliorer l'image/ 1=image identique / + = plus de contraste, brillance, ...
image = enhancer.enhance(4)
# On convertit l'image en noir et blanc
image = image.convert('1')

# *** LECTURE DU CONTENU DE L'IMAGE ***

# On charge Tesseract. A télécharger au préalable. Tout est indiqué dans le Github du projet
# https://github.com/tesseract-ocr/tesseract#installing-tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# On stocke la "lecture" faite par Tesseract
reponse = pytesseract.image_to_string(image)
# On l'affiche en console
print(reponse)

# *** TENTATIVE DE VALIDATION DU CAPTCHA DANS LE SITE WEB ***

# On capte le champ de saisie de la réponse avec son name
inputReponse = driver.find_element(By.NAME, 'reponse')
# On vide le champ (par précaution)
inputReponse.clear()
# On copie le code obtenu dans le champ
inputReponse.send_keys(reponse)

# On cherche le bouton de validation. Recherche plus complexe à partir de la balise HTML et de son type
valider = driver.find_element(By.XPATH, '//input[@type="button"]')
# On simule un clic
valider.send_keys(Keys.ENTER)

# On bloque le processus en console pour éviter que la fenêtre ne se referme automatiquement
user_choice = input('Cliquer sur ENTER pour stopper')
if not user_choice:
    print('Processus stoppé')
quit()
