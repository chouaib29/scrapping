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


def cancel_button_fct():
    try:
        cancel_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'gm-ui-hover-effect'))
            )
        cancel_button.click()
    except Exception as e :
        print(f"Erreur lors du clic sur Cancel : {e}")

def uncheck_button_fct():
    try:

        first_cell = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'td:first-child'))
            )
        first_cell.click()
    except Exception as e :
        print(f"Erreur lors du clic sur uncheck : {e}")

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
    competitors = competitors_table.find_elements(By.TAG_NAME, "tr")

    # Récupérer les lignes du tableau
    for i in range(len(competitors)) :
        try:
            # Accéder à la première cellule de la ligne
            first_cell = competitors[i].find_element(By.CSS_SELECTOR, 'td:first-child')
            
            # Afficher la longueur du texte dans la cellule pour vérifier
            first_cell_text = first_cell.text
            print(f"Texte de la première cellule : {first_cell_text}")
            
            # Cliquer sur la première cellule
            first_cell.click()
            print(f"Cellule de la ligne {i+1} cliquée avec succès.")

        except Exception as e:
            print(f"Erreur lors de l'accès ou du clic sur la cellule de la ligne {i+1} : {e}")

        
        # Étape 3 : Récupérer tous les <canvas> dans le div spécifique
        canvas_elements = driver.find_elements(By.CSS_SELECTOR, '#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(3) canvas')
        print(f"Nombre de canvas trouvés : {len(canvas_elements)}")

        # Filtrer les <canvas> qui n'ont pas d'attribut 'title' ou dont le titre est vide
        filtered_canvas_elements = [
            canvas for canvas in canvas_elements
            if canvas.get_attribute("width") == "37" and canvas.get_attribute("height") == "38"
        ]
        print(f"Nombre de canvas sans 'title' ou avec un 'title' vide : {len(filtered_canvas_elements)}")
        if filtered_canvas_elements:
            # Récupérer la date affichée
            element_date = driver.find_element(By.CSS_SELECTOR, ".timeLabel")
            date_text = element_date.text
            print(f"Date récupérée : {date_text}")
            time.sleep(2)

            # Attendre que le canvas soit visible et cliquable
            WebDriverWait(driver, 20).until(EC.visibility_of(filtered_canvas_elements[0]))
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(filtered_canvas_elements[0]))
            print("cannva visible ")

            # Simuler un clic sur ce canvas avec ActionChains
            actions = ActionChains(driver)
            actions.move_to_element(filtered_canvas_elements[0]).click().perform()
            print("clic sur canva")

            try:
                # Récupérer les informations du nom et de la direction
                name = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(1) > td > div > div:nth-child(2)").text
                voile = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(2) > td > div > div:nth-child(2)").text
                place = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(3) > td > div > div:nth-child(2)").text
                vitesse = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(4) > td > div > div:nth-child(2)").text
                direction = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(5) > td > div > div:nth-child(2)").text
                angle = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(6) > td > div > div:nth-child(2)").text
                position_DMS = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(7) > td > div > div:nth-child(2)").text
                position_Decimal = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(8) > td > div > div:nth-child(2)").text

                # Si le nom n'a pas encore été traité, l'ajouter à l'ensemble et sauvegarder ses données
                if name not in processed_names:
                    print(f"Nom : {name}, Position : {direction}")

                    # Sauvegarder les informations dans un fichier
                    with open(f"{name}.txt", "a") as f:
                        f.write(f"time : {date_text}, direction: {direction}, voile: {voile}, place, {vitesse} ,angle: {angle} ,position_DMS: {position_DMS}, position_Decimal: {position_Decimal} \n")

                    processed_names.add(name)  # Ajouter le nom à l'ensemble pour éviter les doublons
                
                time.sleep(2)
                cancel_button_fct()
                time.sleep(2)
                uncheck_button_fct()
                time.sleep(2)


            except Exception as e:
                print(f"Erreur lors de la recuperation des données : {e}")


# Étape 1 : Clique sur le bouton "Plus d'options"
more_options_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[selenium-id="moreOptionsButton"]'))
)
more_options_button.click()
print("Bouton 'Plus d'options' cliqué avec succès.")

time.sleep(2)

# Étape 2 : Clique sur le bouton "settings"
settings_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[selenium-id="raceMapSettingsButton"]'))
)
settings_button.click()
print("Bouton 'settings' cliqué avec succès.")

time.sleep(2)

# Étape 3 : Clique sur le bouton "checkBox"
checkBox_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[selenium-id="showOnlySelectedCompetitorsCheckBox-input"]'))
)
checkBox_button.click()
print("Bouton 'checkBox' cliqué avec succès.")

time.sleep(2)

# Étape 3 : Clique sur le bouton "done"
done_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[selenium-id="OkButton"]'))
)
done_button.click()
print("Bouton 'done_button' cliqué avec succès.")

time.sleep(2)

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



element = driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(7) > div:nth-child(2) > div > div:nth-child(2) > div > div > div > div > div:nth-child(1) > div.timePanelSlider > div")
sub_element = element.find_element(By.CSS_SELECTOR,"body > div:nth-child(7) > div:nth-child(2) > div > div:nth-child(2) > div > div > div > div > div:nth-child(1) > div.timePanelSlider > div > div.gwt-SliderBar-line")
size = sub_element.size
w = size['width']
action = ActionChains(driver)
action.move_to_element_with_offset(sub_element, -1*w/2 + 80, 0).click().perform()

# Attendre que le tableau des concurrents soit présent
competitors_table = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div:nth-child(7) > div:nth-child(2) > div > div:nth-child(3) > div > div > div:nth-child(2) > div > div:nth-child(12) > div > div > div > div > table > tbody:nth-child(3)'))
)

# Boucle pour récupérer les informations à chaque instant
for _ in range(10):  # touts les secondes
    toggle_play_pause()  # Mettre en pause
    time.sleep(1) 
    retrieve_position_data()  # Récupérer les infos
    time.sleep(1)  
    toggle_play_pause()  # Reprendre la lecture
    time.sleep(1) 

driver.quit()