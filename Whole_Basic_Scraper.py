import urllib.request
import ssl
import re

# Constants

SURROUND = 'class="category-page__member-link" title=".*?">'
APPEARANCE_START = 42
APPEARANCE_END = -2
BASE_URL = 'https://dc.fandom.com/wiki/Category:character/Appearances'
SITE_MAP = 'https://dc.fandom.com/sitemap-newsitemapxml-NS_0-id-1-14098.xml'
GET_CHAR_NAME_START = 27
GET_CHAR_NAME_END = -6

# Appearance Finding
def open_webpage(url):
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        html = urllib.request.urlopen(url, context=ctx).read()
        return html
    except:
        print('Could not open', url)

def find_appearances(html):
    try:
        all_appearances = set()
        all_substrings = re.findall(SURROUND, str(html))
        for sub in all_substrings:
            all_appearances.add(sub[APPEARANCE_START:APPEARANCE_END])
        return all_appearances
    except:
        print('Could not find all appearances')

def do_the_whole_thing(url):
    return find_appearances(open_webpage(url))

# Establish Dictionary (Time = ~25 min)
def establish():
    my_character_dict = {}
    html = str(open_webpage(SITE_MAP))
    characters = re.findall('https://dc.fandom.com/wiki/.*?</loc>', html)
    print(characters[:4])
    for character in characters:
        character = character[GET_CHAR_NAME_START:GET_CHAR_NAME_END]
        char_list = character.split('_')
        name = character
        if len(char_list) > 1:
            if char_list[1][0] == '(':
                name = char_list[0]
            else:
                name = char_list[0] + ' ' + char_list[1]
        try:
            if name in my_character_dict:
                my_character_dict[name] |= do_the_whole_thing(BASE_URL.replace('character', character))
            else:
                my_character_dict[name] = do_the_whole_thing(BASE_URL.replace('character', character))
        except:
            pass
            # print('Failed for', character)
    return my_character_dict

final_dict = establish()

def find_intersection(chars):
    if len(chars) < 1:
        return set()
    result = mydata[chars[0]]
    for char in chars[1:]:
        result = result & mydata[char]
    return result
