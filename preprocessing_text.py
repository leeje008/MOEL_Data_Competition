import re
from konlpy.tag import Okt


def text_clean(text):
    pattern = '([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)' # E-mail제거
    text = re.sub(pattern, '', text)
    pattern = '(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+' # URL제거
    text = re.sub(pattern, '', text)
    pattern = '([ㄱ-ㅎㅏ-ㅣ]+)'  # 한글 자음, 모음 제거    
    text = re.sub(pattern, '', text)
    pattern = '([a-zA-Z0-9]+)'   # 알파벳, 숫자 제거  
    text = re.sub(pattern, '', text)
    pattern = '<[^>]*>'         # HTML 태그 제거
    text = re.sub(pattern, '', text)
    pattern = '[^\w\s]'         # 특수기호제거
    text = re.sub(pattern, '', text)
    return text  

def clean_text(text):
    '''
    텍스트에 있는 특수 문자 제거
    '''
    text = re.sub(r'[^\w\s]', '', text.lower())
    return text

def remove_stopwords(text, stopwords):
    '''
    불용어 제거
    text: 불용어 제거를 할 텍스트 데이터
    stopwords: 불용어 목록들
    '''
    words = text.split()
    filtered_words = [word for word in words if word not in stopwords]
    return ' '.join(filtered_words)

def extract_nouns(text):
    '''
    한국어 명사 추출
    '''
    okt = Okt()
    return okt.nouns(text)
