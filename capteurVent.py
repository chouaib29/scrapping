from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors=yes') 
chrome_options.add_argument('--allow-insecure-localhost')  

driver = webdriver.Chrome(options=chrome_options)

driver = webdriver.Chrome() 
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
    processed_names = set()  
    
    element_date = driver.find_element(By.CSS_SELECTOR, ".timeLabel")
    date_text = element_date.text
    print(f"Date récupérée : {date_text}")
    time.sleep(2)
    canvas_elements = driver.find_elements(By.CSS_SELECTOR, '#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(3) canvas')
    print(f"Nombre de canvas trouvés : {len(canvas_elements)}")

    filtered_canvas_elements = [
        canvas for canvas in canvas_elements
        if canvas.get_attribute("width") == "28" and canvas.get_attribute("height") == "28"
    ]
    print(f"Nombre de canvas sans 'title' ou avec un 'title' vide : {len(filtered_canvas_elements)}")

    for i in range(len(filtered_canvas_elements)):
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of(filtered_canvas_elements[i]))
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(filtered_canvas_elements[i]))

            actions = ActionChains(driver)
            actions.move_to_element(filtered_canvas_elements[i]).click().perform()
            print("Clic sur le canvas")

            Source  = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(1) > td > div > a").text
            Vent = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(2) > td > div > div:nth-child(2)").text
            vitesse = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(3) > td > div > div:nth-child(2)").text
            temps = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(4) > td > div > div:nth-child(2)").text
            position_DMS = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(5) > td > div > div:nth-child(2)").text
            position_Decimal = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(6) > td > div").text

            if Source not in processed_names:
                print(f"Nom : {Source}, Vent : {Vent}")

                with open(f"{Source}.txt", "a") as f:
                    f.write(f"time : {date_text}, Source: {Source}, Vent: {Vent}, vitesse: {vitesse}, temps_cateur: {temps}, position_DMS: {position_DMS}, position_Decimal: {position_Decimal}\n")

                processed_names.add(Source)  # Ajouter le nom à l'ensemble pour éviter les doublons

            time.sleep(2)
            cancel_button_fct()
            time.sleep(2)

        except Exception as e:
            print(f"Erreur lors de la récupération des données : {e}")

# Gestion du bouton "TimePanel-ShowExtended"
appeareDate_clicked = False
if not appeareDate_clicked:
    try:
        appeareDate = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.TimePanel-ShowExtended-Button'))
        )
        appeareDate.click()
        driver.execute_script("arguments[0].onclick = function() { return false; }", appeareDate)
        appeareDate_clicked = True
        print("Bouton 'TimePanel-ShowExtended' cliqué.")
    except Exception as e:
        print(f"Erreur lors du clic sur le bouton : {e}")



element = driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(7) > div:nth-child(2) > div > div:nth-child(2) > div > div > div > div > div:nth-child(1) > div.timePanelSlider > div")
sub_element = element.find_element(By.CSS_SELECTOR,"body > div:nth-child(7) > div:nth-child(2) > div > div:nth-child(2) > div > div > div > div > div:nth-child(1) > div.timePanelSlider > div > div.gwt-SliderBar-line")
size = sub_element.size
w = size['width']
action = ActionChains(driver)
action.move_to_element_with_offset(sub_element, -1*w/2 + 80, 0).click().perform()



for _ in range(3030):  
    toggle_play_pause()  
    time.sleep(1) 
    retrieve_position_data() 
    time.sleep(1)  
    toggle_play_pause() 
    time.sleep(1) 

driver.quit()