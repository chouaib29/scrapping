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
        cancel_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'gm-ui-hover-effect'))
            )
        cancel_button.click()
    except Exception as e :
        print(f"Erreur lors du clic sur Cancel : {e}")

def uncheck_button_fct(index):
    try:
        competitors = competitors_table.find_elements(By.TAG_NAME, "tr")
        element = competitors[index].find_element(By.CSS_SELECTOR, 'td.MGLFIQ-jd-a > div > div') 

        WebDriverWait(driver, 10).until(EC.visibility_of(element))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element))
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(element))

        actions = ActionChains(driver)
        actions.move_to_element(element).click().perform()

    except Exception as e:
        print(f"Erreur lors de la désélection de l'élément de la ligne {index + 1} : {e}")

# Fonction pour cliquer sur le bouton play/pause
def toggle_play_pause():
    try:
        play_pause_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'playPauseButton'))
        )
        play_pause_button.click()
    except Exception as e:
        print(f"Erreur lors du clic sur Play/Pause : {e}")

# Fonction pour récupérer les informations
def retrieve_position_data():
    processed_names = set()  
    competitors = competitors_table.find_elements(By.TAG_NAME, "tr")
    element_date = driver.find_element(By.CSS_SELECTOR, ".timeLabel")
    date_text = element_date.text
    print(f"Date récupérée : {date_text}")
    #time.sleep(1)

    for i in range(len(competitors)):
        try:
            # Récupérer dynamiquement l'élément à chaque itération pour éviter l'erreur "stale element reference"
            competitors = competitors_table.find_elements(By.TAG_NAME, "tr")  # Réinitialisation à chaque itération
            first_div = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(competitors[i].find_element(By.CSS_SELECTOR, 'td.MGLFIQ-jd-a > div > div'))
            )
            first_div.click()

        except Exception as e:
            print(f"Erreur lors de l'accès ou du clic sur la cellule de la ligne {i + 1} : {str(e)}")
            continue  

        #time.sleep(1)
        canvas_elements = driver.find_elements(By.CSS_SELECTOR, '#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(3)> canvas')

        # Liste filtrée des canvas
        filtered_canvas_elements = []
        for canvas in canvas_elements:
            try:
                # Récupérer les styles calculés spécifiques
                style_values = driver.execute_script("""
                    const style = window.getComputedStyle(arguments[0]);
                    return {
                        width: style.width,
                        height: style.height,
                        zIndex: style.zIndex
                    };
                """, canvas)

                style_width = style_values["width"]
                style_height = style_values["height"]
                z_index = style_values["zIndex"]

                # Vérifier les dimensions et le z-index
                if (canvas. get_dom_attribute("width") == "37" and
                    canvas. get_dom_attribute("height") == "38" and
                    style_width == "37px" and
                    style_height == "38px" and
                    z_index == "215"):
                    filtered_canvas_elements.append(canvas)

            except Exception as e:
                print(f"Erreur lors de l'analyse d'un canvas : {e}")

        print(f"Nombre de canvas bateau : {len(filtered_canvas_elements)}")
        if filtered_canvas_elements:
            try:
                # Vérifier que le canvas(bateau) est visible et cliquable
                WebDriverWait(driver, 10).until(EC.visibility_of(filtered_canvas_elements[0]))
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(filtered_canvas_elements[0]))

                # Simuler un clic sur le canvas
                actions = ActionChains(driver)
                actions.move_to_element(filtered_canvas_elements[0]).click().perform()
                #recuperer les données voulu
                name = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(1) > td > div > div:nth-child(2)").text
                voile = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(2) > td > div > div:nth-child(2)").text
                place = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(3) > td > div > div:nth-child(2)").text
                vitesse = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(4) > td > div > div:nth-child(2)").text
                direction = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(5) > td > div > div:nth-child(2)").text
                angle = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(6) > td > div > div:nth-child(2)").text
                position_DMS = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(7) > td > div > div:nth-child(2)").text
                position_Decimal = driver.find_element(By.CSS_SELECTOR, "#googleMapsArea > div > div.gm-style > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > div > div.gm-style-iw.gm-style-iw-c > div.gm-style-iw-d > div > table > tbody > tr:nth-child(8) > td > div > div:nth-child(2)").text

                if name not in processed_names:
                    print(f"Nom : {name}, Position : {direction}")
                   
                    with open(f"{name}.txt", "a") as f:
                        f.write(f"time : {date_text}, direction: {direction}, voile: {voile}, place: {place}, vitesse: {vitesse}, angle: {angle}, position_DMS: {position_DMS}, position_Decimal: {position_Decimal}\n")

                    processed_names.add(name)
                #ajouter le sleep pour eviter le probleme de de uncheck qui ne fonctionne pas   
                time.sleep(1)
                cancel_button_fct()

            except Exception as e:
                print(f"Erreur lors de la récupération des données : {e}")
        # Désélectionner l'élément après utilisation
        uncheck_button_fct(i)

# Clique sur le bouton "Plus d'options"
more_options_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[selenium-id="moreOptionsButton"]'))
)
more_options_button.click()

# Clique sur le bouton "zoomOut"
zoomOut_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[selenium-id="zoomOutButton"]'))
)

zoomOut_button.click()
# Clique sur le bouton "settings"
settings_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[selenium-id="raceMapSettingsButton"]'))
)
settings_button.click()

# Clique sur le bouton "checkBox"
checkBox_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[selenium-id="showOnlySelectedCompetitorsCheckBox-input"]'))
)
checkBox_button.click()

# Uncheck l'aparition du tour de manoeuvre
manoeuvreVirer_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '//label[text()="Tour de pénalité"]/preceding-sibling::input[@type="checkbox"]'))
)
manoeuvreVirer_button.click()

# Uncheck l'aparition du virer de manoeuvre
manoeuvreTour_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '//label[text()="Virer"]/preceding-sibling::input[@type="checkbox"]'))
)
manoeuvreTour_button.click()

# Uncheck l'aparition de changement d'amure de manoeuvre
manoeuvreAmure_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '//label[text()="Changement d\'amure"]/preceding-sibling::input[@type="checkbox"]'))
)
manoeuvreAmure_button.click()

# Clique sur le bouton "done"
done_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[selenium-id="OkButton"]'))
)
done_button.click()

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
    except Exception as e:
        print(f"Erreur lors du clic sur le bouton afficher le temp : {e}")

element = driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(7) > div:nth-child(2) > div > div:nth-child(2) > div > div > div > div > div:nth-child(1) > div.timePanelSlider > div")
sub_element = element.find_element(By.CSS_SELECTOR,"body > div:nth-child(7) > div:nth-child(2) > div > div:nth-child(2) > div > div > div > div > div:nth-child(1) > div.timePanelSlider > div > div.gwt-SliderBar-line")
size = sub_element.size
w = size['width']
action = ActionChains(driver)
# placer le curseur sur la position voulu dans le timeLine
action.move_to_element_with_offset(sub_element, -1*w/2 + 735, 0).click().perform()

# Attendre que le tableau des concurrents soit présent
competitors_table = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div:nth-child(7) > div:nth-child(2) > div > div:nth-child(3) > div > div > div:nth-child(2) > div > div:nth-child(12) > div > div > div > div > table > tbody:nth-child(3)'))
)
#boucler sur la duré de la regate (50min) avec 30 sec avant leur debut  
for _ in range(3030):  
    toggle_play_pause()  
    time.sleep(1)  
    retrieve_position_data()  
    time.sleep(2)  
    toggle_play_pause() 
    time.sleep(1) 

driver.quit()