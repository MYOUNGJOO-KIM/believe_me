#from selenium.webdriver.common.by import By
import ssl
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib.request
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import machine
import pytesseract
from PIL import Image
import os
import imghdr

tesseractOcrPath = '/opt/homebrew/bin/tesseract' #'/usr/local/bin/tesseract' 

pytesseract.pytesseract.tesseract_cmd = tesseractOcrPath

def get_image_files():
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']  # 이미지 파일 확장자 목록을 원하는 대로 수정하세요.
    image_files = []
    for file_name in os.listdir('.'):  # 현재 폴더의 파일 목록을 얻습니다. 다른 폴더를 대상으로 하려면 해당 경로를 입력하세요.
        file_ext = os.path.splitext(file_name)[1]
        if os.path.isfile(file_name) and file_ext.lower() in image_extensions:
            image_files.append(file_name)
    return image_files

# SSL 인증서 검증 비활성화
ssl._create_default_https_context = ssl._create_unverified_context
driver = webdriver.Chrome()
#driver.get("http://www.python.org")

driver.get('https://www.google.com/search?q=썸톡&tbm=isch')


# 이미지 크롤링
scroll_pause_time = 1  # 스크롤 후 대기할 시간 (초)
scroll_count = 2  # 스크롤 횟수

# 대기 시간 설정 (초 단위)
wait_time = 10


# 스크롤을 scroll_count만큼 반복하여 이미지 로드
for _ in range(scroll_count):
    # 스크롤 높이 가져오기
    last_height = driver.execute_script("return document.body.scrollHeight")

    # 스크롤 내리기
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 이미지 로딩을 기다림
    time.sleep(scroll_pause_time) 

    
    # 리스트 이미지 요소 선택
    #images = driver.find_elements(By.CSS_SELECTOR, 'img.rg_i')

    # 요소가 나타날 때까지 대기
    images = WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'img.rg_i'))
    )

    # 상세보기 이미지 크롤링
    # for image in list_images:
    #     # 이미지 클릭하여 상세보기로 이동
    #     image.click()

    #     # 상세보기 이미지 요소 선택
    #     detail_image = driver.find_element(By.CSS_SELECTOR, 'img.r48jcc')

        # 이미지 크롤링 또는 다운로드 작업 수행
        # ...

        # 이전 페이지로 돌아가기
        #driver.back()

    ## 새로 로드된 이미지 찾기
    #images = driver.find_elements(By.CSS_SELECTOR, 'img.rg_i')

    for i, image in enumerate(images):
        # 이미지 클릭하여 상세보기로 이동
        image.click()
        #img = driver.find_element(By.CSS_SELECTOR, 'img.iPVvYb')

        img = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'img.iPVvYb'))
        )

        try:
            #image_url = image.get_attribute('src')

            # 상세보기 이미지 요소 선택
            img_url = img.get_attribute('src')

            if img_url is not None:
                urllib.request.urlretrieve(img_url, f'image_{i}.jpg')
        except NoSuchElementException:
            print(f"Failed to retrieve image URL for image_{i}")

    # 스크롤 후 스크롤 높이 체크
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break  # 더 이상 스크롤할 수 없음

# 웹 드라이버 종료
driver.close()




# 여기부터 이미지 가공

# 현재 실행 중인 파이썬 파일의 경로
current_path = os.path.dirname(os.path.abspath(__file__))

# 이미지 파일의 상대적인 경로
#image_path = os.path.join(current_path, '이미지파일.jpg')

# 이미지 파일의 절대 경로
#absolute_path = os.path.abspath(image_path)

folder_path = ''  # 이미지 파일들이 있는 폴더 경로
#image_extensions = ['.jpg', '.jpeg', '.png']  # 이미지 파일의 확장자들
print("current_path : ", current_path)
print("folder_path : ", folder_path)

# 폴더 내의 파일 목록 조회
#file_list = os.listdir(folder_path)





# 이미지 파일 리스트 얻기
image_list = get_image_files()

# 출력
for image in image_list:
    print(image)


print("image_list : ", image_list)

lines = []

# 이미지 파일 개수 카운트
image_count = 0
for img_name in image_list:
    image_count += 1

    # 이미지 열기
    image_path = os.path.join(folder_path, img_name)# f'image_{i}.jpg'
    image = Image.open(image_path)

    # 이미지에서 텍스트 추출
    text = pytesseract.image_to_string(image, lang='kor+eng')#오류나면 eng

    # 추출된 텍스트 출력
    #print(text)


    lines.append(text)


print(f"폴더 내의 이미지 파일 개수: {image_count}")
print(lines)
        
# 추출된 텍스트 저장
output_file = current_path+'/test.txt' #'출력 파일 경로'


with open(output_file, "w", encoding="utf-8") as file:
    for line in lines:
        file.write(line + "\n")

    
print(f"파일 test.txt이(가) 생성되었습니다.")











time.sleep(500)

#mac에서 셀레니움 설정할 때
# cd selenium/bin
#source activate


#다음에 할 거는
#1. 이미지의 최소사이즈를 설정하는 기능 추가 필요
#2. 만약 불가능하다면 머신러닝으로 글자만 추려내는게 가능한지 알아봐야 함.
#3. chatGPT도 그림에서 글자만 떼는게 가능한지 알아보기
#4. 한국어도 추가해야 함