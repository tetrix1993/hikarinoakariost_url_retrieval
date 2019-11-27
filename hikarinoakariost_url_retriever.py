import urllib.request
import math
from myutil.util import create_directory
from myutil.util import download_image
from myutil.util import get_response
from myutil.util import get_response_with_header
from myutil.util import is_file_exists

MAIN_PAGE_PREFIX = "https://hikarinoakariost.info/page/"
MAIN_PAGE_SUFFIX = "/"
OUT_LINK_PREFIX = "https://hikarinoakariost.info/out/?"
NOOPENER_NOREFERRER = 'rel="noopener noreferrer">'

def get_choice():
    while True:
        print("Enter your choice. Enter '0' if you are not selecting any of the choices")
        try:
            choice = int(input("Enter choice: "))
            break
        except Exception as e:
            print('Please enter a number')
            pass
    return choice
    
def process_song_page(choice, text_block):
    text = text_block[choice]
    split1 = text.split('<a href="')
    if len(split1) < 2:
        return
    page_url = split1[1].split('"')[0]
    response = get_response_with_header(page_url)
    split2 = response.split(OUT_LINK_PREFIX)
    if len(split2) < 2:
        return
    for i in range(1, len(split2), 1):
        split3 = split2[i].split('</td>')[0]
        if NOOPENER_NOREFERRER in split3:
            split4 = split3.split(NOOPENER_NOREFERRER)
            if len(split4) < 2:
                continue
            host = split4[1].split('</a>')[0]
            code = split3.split('"')[0]
            out_link = base64_decode(code)
            print(str(i) + " - " + host + " " + out_link)
    
def base64_decode(data):
    b64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    o1 = o2 = o3 = o4 = h1 = h2 = h3 = h4 = bits = i = 0
    ac = 0
    dec = ""
    tmp_arr = []
    
    if not data:
        return data
    
    while i < len(data):
        h1 = b64.index(data[i])
        i = i + 1
        h2 = b64.index(data[i])
        i = i + 1
        h3 = b64.index(data[i])
        i = i + 1
        h4 = b64.index(data[i])
        i = i + 1
        
        bits = h1 << 18 | h2 << 12 | h3 << 6 | h4
        
        o1 = bits >> 16 & 0xff
        o2 = bits >> 8 & 0xff
        o3 = bits & 0xff
        
        tmp_arr.append("")
        
        if (h3 == 64):
            tmp_arr[ac] = chr(o1)
            ac = ac + 1
        elif (h4 == 64):
            tmp_arr[ac] = chr(o1) + chr(o2)
            ac = ac + 1
        else:
            tmp_arr[ac] = chr(o1) + chr(o2) + chr(o3)
            ac = ac + 1
        
    dec = ''.join(tmp_arr)
    return dec

def get_title(choice, split2):
    title_temp = split2[choice].split('title="')
    if len(title_temp) < 2:
        return ""
    return title_temp[1].split('">')[0]

def run():
    page = 1
    choice = 1
    goto_next_page = True
    while (goto_next_page):
        print('\n>>> Loading page ' + str(page) + ' <<<\n')
        main_page_url = MAIN_PAGE_PREFIX + str(page) + MAIN_PAGE_SUFFIX
        response = get_response_with_header(main_page_url)
        split1 = response.split('<div class="td-container td-pb-article-list ">')
        if len(split1) < 2:
            return
        split2 = split1[1].split('<div class="td-module-thumb">')
        num_of_choices = len(split2) - 1
        for i in range(1, len(split2), 1):
            title = get_title(i, split2)
            if len(title) == 0:
                continue
            print(str(i) + " - " + title)
        while True:
            choice = get_choice()
            if (choice >= 1 and choice <= num_of_choices):
                title = get_title(choice, split2)
                print(title)
                process_song_page(choice, split2)
            else:
                break
        go_next_page = input('Go to next page? Y/N: ')
        if (not go_next_page in "Y") and (not go_next_page in "y"):
            goto_next_page = False
        page = page + 1

if __name__ == '__main__':
    run()
