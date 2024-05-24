import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re
from urllib.parse import unquote

regex_pattern_email = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
fb_pattern = r'(facebook\.com|fb\.com)'
linkedin_pattern = r"linkedin.com"
youtube_pattern = r"youtube.com"
instagram_pattern = r"instagram.com"
pinterst_pattern = r"pinterest\.com|pin\.it"
contact_number_pattern = r"(\+91)?\-?\d{2}\-[\d ]+|\b\d{3}[-.]?\d{3}[-.]?\d{4}\b|[ \d+]{8,16}"
contact_number_pattern1 = r"tel:([\+\d ]+)"
contact_number_pattern2 = r"\/\/wa.me\/(\d+)"

def strip_set(inp_set):
    return {st.strip() for st in inp_set}

def preprocess_email(in_email):
    skip_pattern = r"\.(jpg|jpeg|png|gif|bmp|tiff?|webp|svg|mp3|wav|flac|aac|ogg|wma|mp4|avi|mkv|mov|wmv|flv|webm|pdf|docx?|xlsx?|pptx?|txt|csv|rtf|zip|rar|7z|tar|gz|bz2|xz|exe|dll|bat|sh|msi|app|ttf|otf|woff|woff2)$"
    if re.search(skip_pattern, in_email):
        return ""
    return re.sub(r"^%20", "", in_email)

def search_add(pattern, inputs, collections):
    mat = re.search(pattern, inputs)
    if mat:
        collections.add(mat.group())

def search_and_input_add(pattern, inputs, collections):
    mat = re.search(pattern, inputs)
    if mat:
        collections.add(inputs)

def extraction(driver):
    all_emails = set()
    all_youtube_links = set()
    all_fb_links = set()
    all_instagram_links = set()
    all_pinterst_links = set()
    all_contact_numbers = set()

    dd = driver.find_elements(By.TAG_NAME, "a")

    for d in dd:
        vaa = d.get_attribute("href")
        if str(vaa) != "None":
            search_add(regex_pattern_email, vaa, all_emails)

            mat_email = re.search(regex_pattern_email, vaa)
            if mat_email:
                all_emails.add(preprocess_email(mat_email.group()))

            search_and_input_add(fb_pattern, vaa, all_fb_links)
            search_and_input_add(instagram_pattern, vaa, all_instagram_links)
            search_and_input_add(youtube_pattern, vaa, all_youtube_links)
            search_and_input_add(pinterst_pattern, vaa, all_pinterst_links)

            for con in re.finditer(contact_number_pattern1, vaa):
                all_contact_numbers.add(con.group(1))

            decode_url = unquote(vaa)
            for con in re.finditer(contact_number_pattern2, decode_url):
                all_contact_numbers.add(con.group(1))

    body_text = driver.find_element(By.TAG_NAME, 'body').text

    email_match_body = re.findall(regex_pattern_email, body_text)
    if len(email_match_body) > 0:
        for e in email_match_body:
            all_emails.add(preprocess_email(e))

    for e in re.finditer(contact_number_pattern, body_text):
        all_contact_numbers.add(e.group())

    full_text = driver.page_source
    email_match_body = re.findall(regex_pattern_email, full_text)

    if len(email_match_body) > 0:
        for e in email_match_body:
            all_emails.add(preprocess_email(e))

    filtered_numbers = [number.strip() for number in all_contact_numbers if 8 < len(number) < 16]

    to_return = {}
    to_return["Facebook_links"] = strip_set(all_fb_links) if len(all_fb_links) > 0 else ""
    to_return["All_Emails"] = strip_set(all_emails) if len(all_emails) > 0 else ""
    to_return["Instagram_links"] = strip_set(all_instagram_links) if len(all_instagram_links) > 0 else ""
    to_return["Youtube_links"] = strip_set(all_youtube_links) if len(all_youtube_links) > 0 else ""
    to_return["Pinterest_links"] = strip_set(all_pinterst_links) if len(all_pinterst_links) > 0 else ""
    to_return["Contact_Numbers"] = strip_set(filtered_numbers) if len(filtered_numbers) > 0 else ""

    return to_return

def main():
    st.title("Web Data Extractor")

    # Add a selectbox to the sidebar:
    site = st.selectbox(
        'Select a website:',
        ("https://www.sundarisilks.com/",
         "http://www.kpssilksaree.com/",
         "https://www.pothys.com/?utm_source=gmb&utm_medium=organic&utm_campaign=sulekhapromanage-pothys",
         "https://tulsisilks.co.in/",
         "https://www.palamsilk.com/",
         "https://rmkv.com/")
    )

    if st.button('Extract Data'):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get(site)
        data = extraction(driver)
        st.write(data)
        driver.quit()

if __name__ == "__main__":
    main()
