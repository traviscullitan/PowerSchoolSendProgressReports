import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import configparser
from datetime import date
from datetime import datetime
from collections import defaultdict
import csv

class Parent():

    def __init__(self,name=None,last_sent_date=None,guardian_id=None,student_name=None):
        self.name = name
        self.last_sent_date = last_sent_date
        self.guardian_id = guardian_id
        self.student_name = student_name

    def __repr__(self):
        return str(
            "Name: " + self.name +
            "\nlast_sent_date:" + self.last_sent_date +
            "\nguardian_id: " + self.guardian_id +
            "\nstudent_name: " + self.student_name
            )
def main():
    
    config = import_config()

    driver = setup_selenium(config)

    login_to_powerschool(driver,config)

    parents = get_parents(config)

    for parent in parents:
        print("Processing:",parent.name)
        process_parent(driver,parent,config)

    close_selenium(driver)

    write_parent_output(config,parents)

    for parent in parents:
        print(repr(parent))

def import_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config = config["DEFAULT"]
    return config

def setup_selenium(config):
    driver = webdriver.Chrome(config["CHROME_DRIVER"]) 
    return driver

def login_to_powerschool(driver,config):
    driver.get(config["HOST"] + '/admin')
    time.sleep(1) # Let the user actually see something!
    username_box = driver.find_element_by_name('username')
    password_box = driver.find_element_by_name('password')
    username_box.send_keys(config["USERNAME"])
    password_box.send_keys(config["PASSWORD"])
    password_box.submit()

def get_parents(config):

    parents = []
    with open(config["INPUT_FILE"],'r') as f:
        next(f) # skip headings
        reader=csv.reader(f,delimiter='\t')
        for firstname,lastname,last_sent_date,guardianid,student_name,grade_level in reader:
            p = Parent(firstname + " " + lastname, last_sent_date, guardianid, student_name)
            parents.append(p)

    return parents

def process_parent(driver,parent,config):
    driver.get(config["HOST"] + "/admin/contacts/edit.html#?guardianid=" + parent.guardian_id)
    time.sleep(5)
    relationship_table = wait_for_element_load_by_id(driver,config["TIMEOUT"],"relationship-table")

    relationship_table_rows = relationship_table.find_elements_by_tag_name("tr")
    for row in relationship_table_rows:
        cols = row.find_elements_by_tag_name("td")
        if len(cols) > 0:
            school = cols[0].text
            name = cols[1].text
            if school == "MS-US" and name == parent.student_name:
                print("School is MS-US and student_name is:",parent.student_name)
                buttons = row.find_elements_by_tag_name("button")
                buttons[0].click()
                edit_box = driver.find_element_by_id("psDialogDocked")
                send_parent_email_if_needed(driver,edit_box,parent,config)
                driver.get(config["HOST"] + "/admin")
                return

    driver.get(config["HOST"] + "/admin")

def send_parent_email_if_needed(driver,edit_box,parent,config):
    list_items = edit_box.find_elements_by_tag_name("li")
    data_access = list_items[2]
    try:
        data_access.click()
    except:
        print("**************Data Access Tag Not Loaded Yet********************")
        driver.save_screenshot("screenshot1.png")
    finally:
        time.sleep(3)


    try:
        data_access.click()
    except:
        print("!!!!!!!!!!!!!!!!!Data Access Tag Still Not Loaded Yet!!!!!!!!!!!!!!!!!!!!!!!!")
        driver.save_screenshot("screenshot2.png")
    finally:
        time.sleep(3)

    email_frequency = create_email_frequencies()
    selected_email_frequency_element = driver.find_element_by_id("frequency-of-emails-input")
    selected_email_frequency_number = email_frequency[Select(selected_email_frequency_element).first_selected_option.text]
    email_last_sent = datetime.strptime(parent.last_sent_date, '%m-%d-%Y')
    days_since_email_last_sent = (datetime.now() - email_last_sent).days
    assignment_details = driver.find_element_by_id("assignment-details-input")

    if assignment_details.is_selected() and days_since_email_last_sent >= selected_email_frequency_number:
        print("********\nWould have sent report for: " + repr(parent) +"*******\n")
        """
            send_now_check_box = driver.find_element_by_id("send-now-input")
            send_now_check_box.click()
            time.sleep(1)
            submit_button = driver.find_element_by_id("demographics-panel-save-button")
            submit_button.click()
            wait_for_element_to_hide_by_id(driver,config["TIMEOUT"],"loading")
        """
        parent.last_sent_date = str(date.today())
        #return

    close_button = edit_box.find_element_by_id("demographics-panel-cancel-button")
    close_button.click()
    time.sleep(1)


def create_email_frequencies():
    email_frequency = defaultdict(lambda: float("inf"))
    email_frequency["Daily"] = 1
    email_frequency["Weekly"] = 7
    email_frequency["Every two weeks"] = 14
    email_frequency["Monthly"] = 30
    return email_frequency

def wait_for_element_load_by_id(driver,timeout,id):
    element = None
    timeout = int(timeout)
    try:
        element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, id)))
    except:
        print("Page Timed Out")
    finally:
        time.sleep(3)
        element = driver.find_element_by_id(id)
        return element


def wait_for_element_to_hide_by_id(driver,timeout,id):
    timeout = int(timeout)
    try:
        WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located((By.ID, id)))
    except:
        print("Page Timed Out Waiting for Element to go invisible")
    finally:
        time.sleep(1)

def write_parent_output(config,parent_output):
    #TODO
    pass

def close_selenium(driver):
    time.sleep(5) # Let the user actually see something!
    driver.quit()

if __name__ == "__main__":
    main()



