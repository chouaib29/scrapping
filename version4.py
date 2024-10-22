from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors=yes')  # Option supplémentaire pour ignorer les erreurs SSL
chrome_options.add_argument('--allow-insecure-localhost')  # Permet les certificats invalides sur localhost

driver = webdriver.Chrome(options=chrome_options)

driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
driver.set_window_size(12000, 5000)
driver.get('https://www.sapsailing.com/gwt/RaceBoard.html?regattaName=OSG2024TEV2023+-+Men%27s+Dinghy&raceName=ILCA+7+-+R1&leaderboardName=OSG2024TEV2023+-+Men%27s+Dinghy&leaderboardGroupId=83eb5c2a-d3ab-4e22-8422-1e4ab154ed34&eventId=b8220cee-9ec7-4640-b8d8-f40e079456d5&mode=PLAYER')

time.sleep(5)

# Étape 1 : Clique sur le bouton "Plus d'options"
more_options_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[selenium-id="moreOptionsButton"]'))
)
more_options_button.click()
print("Bouton 'Plus d'options' cliqué avec succès.")

time.sleep(5)

# Gestion du bouton "TimePanel-ShowExtended"
appeareDate_clicked = False
if not appeareDate_clicked:
    try:
        appeareDate = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.TimePanel-ShowExtended-Button'))
        )
        appeareDate.click()
        driver.execute_script("arguments[0].onclick = function() { return false; }", appeareDate)
        appeareDate_clicked = True  # Marquer le bouton comme cliqué une fois
        print("Bouton 'TimePanel-ShowExtended' cliqué.")
    except Exception as e:
        print(f"Erreur lors du clic sur le bouton : {e}")

# Récupérer la date affichée
element_date = driver.find_element(By.CSS_SELECTOR, ".timeLabel")
date_text = element_date.text
print(f"Date récupérée : {date_text}")

# Étape 3 : Récupérer tous les <canvas> dans le div spécifique
canvas_elements = driver.find_elements(By.CSS_SELECTOR, '#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(3) canvas')
print(f"Nombre de canvas trouvés : {len(canvas_elements)}")

# Filtrer les <canvas> qui n'ont pas d'attribut 'title' ou dont le titre est vide
filtered_canvas_elements = [
    canvas for canvas in canvas_elements
    if canvas.get_attribute("width") == "37" and canvas.get_attribute("height") == "38"
]
print(f"Nombre de canvas sans 'title' ou avec un 'title' vide : {len(filtered_canvas_elements)}")


def cancel_button_fct():
    try:
        cancel_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'gm-ui-hover-effect'))
            )
        cancel_button.click()
    except Exception as e :
        print(f"Erreur lors du clic sur Cancel : {e}")



# Fonction pour cliquer sur le bouton play/pause
def toggle_play_pause():
    try:
        play_pause_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'playPauseButton'))
        )
        play_pause_button.click()
    except Exception as e:
        print(f"Erreur lors du clic sur Play/Pause : {e}")

# Fonction pour récupérer les informations
def retrieve_position_data():
    processed_names = set()  # Utiliser un ensemble pour stocker les noms déjà récupérés

    if filtered_canvas_elements:
        # Récupérer la date affichée
        element_date = driver.find_element(By.CSS_SELECTOR, ".timeLabel")
        date_text = element_date.text
        print(f"Date récupérée : {date_text}")
        time.sleep(2)
        for i in range(len(filtered_canvas_elements)):
            first_canvas = filtered_canvas_elements[i]

            # Attendre que le canvas soit visible et cliquable
            WebDriverWait(driver, 20).until(EC.visibility_of(first_canvas))
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(first_canvas))

            # Simuler un clic sur ce canvas avec ActionChains
            actions = ActionChains(driver)
            actions.move_to_element(first_canvas).click().perform()
            try:
                # Récupérer les informations du nom et de la direction
                name = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(1) > td > div > div:nth-child(2)").text
                direction = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(5) > td > div > div:nth-child(2)").text

                # Si le nom n'a pas encore été traité, l'ajouter à l'ensemble et sauvegarder ses données
                if name not in processed_names:
                    print(f"Nom : {name}, Position : {direction}")

                    # Sauvegarder les informations dans un fichier
                    with open(f"{name}.txt", "a") as f:
                        f.write(f"time : {date_text}, direction: {direction}\n")

                    processed_names.add(name)  # Ajouter le nom à l'ensemble pour éviter les doublons
                
                time.sleep(2)
                cancel_button_fct()
                time.sleep(2)
            except Exception as e:
                print(f"Erreur lors de la recuperation des données : {e}")

element = driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(7) > div:nth-child(2) > div > div:nth-child(2) > div > div > div > div > div:nth-child(1) > div.timePanelSlider > div")
sub_element = element.find_element(By.CSS_SELECTOR,"body > div:nth-child(7) > div:nth-child(2) > div > div:nth-child(2) > div > div > div > div > div:nth-child(1) > div.timePanelSlider > div > div.gwt-SliderBar-line")
size = sub_element.size
w = size['width']
action = ActionChains(driver)
action.move_to_element_with_offset(sub_element, -1*w/2 + 80, 0).click().perform()

# Boucle pour récupérer les informations à chaque instant
for _ in range(10):  # touts les secondes
    toggle_play_pause()  # Mettre en pause
    time.sleep(1) 
    retrieve_position_data()  # Récupérer les infos
    time.sleep(1)  
    toggle_play_pause()  # Reprendre la lecture
    time.sleep(1) 

driver.quit()