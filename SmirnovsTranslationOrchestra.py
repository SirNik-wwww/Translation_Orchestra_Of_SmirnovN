from array import ArrayType
import array
from pathlib import Path
import pandas as pd

import os
import re


were_files_found = 0



#all need tables
chars_id_tab = []
chars_names_tab = []

enemies_id_tab = []
enemies_names_tab = []

items_list = []

abil_list = []
abil_list_alt = []

ach_list = []
ach_secret_list = []

print("Paste path to folder with files.... (like C:\\TranslationDecopMods\\New folder\\The Cool Mod\\Cool mod)")
path = input("...")

#C:\TranslationDecopMods\grfl\GreasyFoolsDeluxe
#C:\TranslationDecopMods\KrillPack
#C:\TranslationDecopMods\EnemyPack\NewEnemyPack



#clean_path = path.strip('"').strip("'")

folder_with_cs_files = Path(path)





#_________________________________________________________________________________
#______      For Characters                                   ____________________
#_________________________________________________________________________________

# getting names
def extract_char_name(file_path):
    pattern =  re.compile(r'new\s+Character\s*\(\s*"([^"]+)"\s*,\s*"[^"]+"\s*\)')

    with open(file_path, 'r', encoding='utf-8-sig') as f:
        content = f.read()
        matches = re.findall(pattern, content)


        for match in matches:
            chars_names_tab.append(match)

# getting id
def extract_char_id(file_path):
    pattern =  re.compile(r'new\s+Character\s*\(\s*"[^"]*"\s*,\s*"([^"]+)"\s*\)')

    with open(file_path, 'r', encoding='utf-8-sig') as f:
        content = f.read()
        matches = re.findall(pattern, content)


        for match in matches:
            chars_id_tab.append(match)
#__________________________________________________      END      ________________



#_________________________________________________________________________________
#______      For Enemies                                      ____________________
#_________________________________________________________________________________

def extract_enemies(file_path):
    pattern =  re.compile(r'new\s+Enemy\s*\(\s*"([^"]+)"\s*,\s*"[^"]+"\s*\)')
    pattern_2 =  re.compile(r'new\s+Enemy\s*\(\s*"[^"]*"\s*,\s*"([^"]+)"\s*\)')

    with open(file_path, 'r', encoding='utf-8-sig') as f:
        content = f.read()
        matches = re.findall(pattern, content)
        matches_2 = re.findall(pattern_2, content)

# getting names
        for match in matches:
            enemies_names_tab.append(match)

# getting id
        for match2 in matches_2:
            enemies_id_tab.append(match2)
#__________________________________________________      END      ________________



#_________________________________________________________________________________
#______            For Items                                  ____________________
#_________________________________________________________________________________
def parse_items_to_excel(file_path):
    try:
        # 1. read
        content = ""
        for enc in ['utf-8', 'windows-1251']:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    content = f.read()
                break
            except Exception:
                continue
        
        if not content:
            print("Error: Could not read file.")
            return

        # 2. find
        new_content = content.replace(r'\"', r'\!').strip()
        potential_blocks = re.findall(r'Item_ID\s*=.*?Description\s*=\s*".*?"', new_content, re.DOTALL)


        fields = {
            'Item_ID': r'Item_ID\s*=\s*"(.*?)"',
            'Name': r'Name\s*=\s*"(.*?)"',
            'Description': r'Description\s*=\s*"(.*?)"',
            'Flavour': r'Flavour\s*=\s*"(.*?)"'}

        for block in potential_blocks:
            #block2 = block.replace('r3511', '"')
            data = {}
            for key, pattern in fields.items():
                match = re.search(pattern, block)
                if match:

                    # change \n to enter
                    val = match.group(1).replace('\\n', '''
''').strip()
                    
                    data[key] = val
                    print(data)
                else:
                    data[key] = None

            # add to list what will be upload text to exel tablet
            items_list.append(data)

    except Exception as e:
        print(f"An error occurred: {e}")
#__________________________________________________      END      ________________



#_________________________________________________________________________________
#______            For Abilities                              ____________________
#_________________________________________________________________________________
def parse_abil_to_excel(file_path):
    try:
        # 1. read
        content = ""
        for enc in ['utf-8', 'windows-1251']:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    content = f.read()
                break
            except Exception:
                continue
        
        if not content:
            print("Error: Could not read file.")
            return

        # 2. find
        new_content = content.replace(r'\"', r'\!').strip()
        potential_blocks = re.findall(r'new\s*Ability.*?Visuals\s*=', new_content, re.DOTALL)

        fields = {
            'Abil_ID': r'new\s*Ability\("(.*?)"',
            'Name': r'Name\s*=\s*"(.*?)"',
            'Description': r'Description\s*=\s*"(.*?)"'}

        for block in potential_blocks:
            data = {}
            for key, pattern in fields.items():
                match = re.search(pattern, block)
                if match:
                    # change \n to enter
                    val = match.group(1).replace('\\n', '''
''').strip()
                    data[key] = val
                    print(data)
                else:
                    data[key] = None

            # add to list what will be upload text to exel tablet
            abil_list.append(data)

    except Exception as e:
        print(f"An error occurred: {e}")
#__________________________________________________      END      ________________

#_________________________________________________________________________________
#______            For Abilities Alt                          ____________________
#_________________________________________________________________________________
def parse_abil_to_excel_alt(file_path):
    try:
        # 1. read
        content = ""
        for enc in ['utf-8', 'windows-1251']:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    content = f.read()
                break
            except Exception:
                continue
        
        if not content:
            print("Error: Could not read file.")
            return

        # 2. find
        new_content = content.replace(r'\"', r'\!').strip()
        potential_blocks = re.findall(r'new\s*Ability.*?Visuals\s*=', new_content, re.DOTALL)

        fields = {
            'Abil_ID': r'new\s*Ability\(.*?,\s*"(.*?)"',
            'Name': r'new\s*Ability\("(.*?)"',
            'Description': r'Description\s*=\s*"(.*?)"'}

        for block in potential_blocks:
            data = {}
            for key, pattern in fields.items():
                match = re.search(pattern, block)
                if match:
                    # change \n to enter
                    val = match.group(1).replace('\\n', '''
''').strip()
                    data[key] = val
                    print(data)
                else:
                    data[key] = None

            # add to list what will be upload text to exel tablet
            abil_list_alt.append(data)

    except Exception as e:
        print(f"An error occurred: {e}")
#__________________________________________________      END      ________________



#_________________________________________________________________________________
#______            For Achivments                             ____________________
#_________________________________________________________________________________
def parse_ach_to_excel(file_path):
    try:
        # 1. read
        content = ""
        for enc in ['utf-8', 'windows-1251']:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    content = f.read()
                break
            except Exception:
                continue
        
        if not content:
            print("Error: Could not read file.")
            return

        # 2. find
        new_content = content.replace(r'\"', r'\!').strip()
        potential_blocks = re.findall(r'new\s*ModdedAchievements.*?\);', new_content, re.DOTALL)


        fields = {
            'Ach_ID': r'ModdedAchievements\(.*?\),\s*"(.*?)"',
            'Name': r'ModdedAchievements\("(.*?)",\s*"',
            'Description': r'ModdedAchievements\(".*?",\s*"(.*?)",\s*ResourceLoader'}


        for block in potential_blocks:
            #block2 = block.replace('r3511', '"')
            data = {}
            for key, pattern in fields.items():
                match = re.search(pattern, block)
                if match:

                    # change \n to enter
                    val = match.group(1).replace('\\n', '''
''').strip()
                    
                    data[key] = val
                    print(data)
                else:
                    data[key] = None

            # add to list what will be upload text to exel tablet
            ach_list.append(data)

    except Exception as e:
        print(f"An error occurred: {e}")

# for secret description
def parse_ach_secret_to_excel(file_path):
    try:
        # 1. read
        content = ""
        for enc in ['utf-8', 'windows-1251']:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    content = f.read()
                break
            except Exception:
                continue
        
        if not content:
            print("Error: Could not read file.")
            return

        # 2. find
        new_content = content.replace(r'\"', r'\!').strip()
        potential_blocks = re.findall(r'new\s*ModdedAchievements.*?SecretDescription\s*=\s*".*?"', new_content, re.DOTALL)


        fields = {
            'Ach_ID': r'ModdedAchievements\(.*?\),\s*"(.*?)"',
            'Name': r'SecretDescription\s*=\s*"(.*?)"'}

        for block in potential_blocks:
            #block2 = block.replace('r3511', '"')
            data = {}
            for key, pattern in fields.items():
                match = re.search(pattern, block)
                if match:

                    # change \n to enter
                    val = match.group(1).replace('\\n', '''
''').strip()
                    
                    data[key] = val
                    print(data)
                else:
                    data[key] = None

            # add to list what will be upload text to exel tablet
            ach_secret_list.append(data)

    except Exception as e:
        print(f"An error occurred: {e}")
#__________________________________________________      END      ________________
















# run all checks
def process_folder(folder_path):

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.cs'):
                    file_path = os.path.join(root, file)

                    extract_char_name(file_path)
                    extract_char_id(file_path)

                    extract_enemies(file_path)

                    #extract_item_id(file_path)
                    #extract_item_name(file_path)
                    #extract_item_plus(file_path)
                    parse_items_to_excel(file_path)

                    parse_abil_to_excel(file_path)
                    parse_abil_to_excel_alt(file_path)

                    parse_ach_to_excel(file_path)

                    parse_ach_secret_to_excel(file_path)


                    global were_files_found 
                    were_files_found = 1
                    




process_folder(folder_with_cs_files)










if were_files_found == 1:
    #_______ Characters ______________________

    #Expanding lists to the same length
    while len(chars_id_tab) > len(chars_names_tab):
        chars_names_tab.append('nope')

    while len(chars_id_tab) < len(chars_names_tab):
        chars_id_tab.append('nope')

    results = list(zip(chars_id_tab,chars_names_tab))
    df = pd.DataFrame(results, columns=['id', 'text'])
    df.to_excel('borchestra_chars.xlsx', index=False)
    #_________________________________________



    #_______ Enemies ______________________

    #Expanding lists to the same length
    while len(enemies_id_tab) > len(enemies_names_tab):
        enemies_names_tab.append('nope')

    while len(enemies_id_tab) < len(enemies_names_tab):
        enemies_id_tab.append('nope')

    results = list(zip(enemies_id_tab,enemies_names_tab))
    df = pd.DataFrame(results, columns=['id', 'text'])
    df.to_excel('borchestra_enemies.xlsx', index=False)
    #_________________________________________



    #_______ Items ___________________________
    if items_list:
        df = pd.DataFrame(items_list)
    else:
        results = list(zip(['null', 'null'],['null', 'null'],['null', 'null'],['null', 'null']))
        df = pd.DataFrame(results, columns=['id', 'text', 'description', 'subDescription'])

    df.columns = ['id', 'text', 'description', 'subDescription']
            
    df.to_excel('borchestra_items.xlsx', index=False)
    #_________________________________________



    #_______ Abils ___________________________
    if abil_list:
        df = pd.DataFrame(abil_list)
    else:
        results = list(zip(['null', 'null'],['null', 'null'],['null', 'null']))
        df = pd.DataFrame(results, columns=['id', 'text', 'description'])

    df.columns = ['id', 'name', 'description']       
    df.to_excel('borchestra_abils.xlsx', index=False)


    if abil_list_alt:
        df = pd.DataFrame(abil_list_alt)
    else:
        results = list(zip(['null', 'null'],['null', 'null'],['null', 'null']))
        df = pd.DataFrame(results, columns=['id', 'text', 'description'])

    df.columns = ['id', 'name', 'description']       
    df.to_excel('borchestra_abils_alt_ver.xlsx', index=False)
    #_________________________________________



    #_______ Achivments ______________________
    
    if ach_list:
        df = pd.DataFrame(ach_list)
    else:
        results = list(zip(['null', 'null'],['null', 'null'],['null', 'null']))
        df = pd.DataFrame(results, columns=['id', 'text', 'description'])

    df.columns = ['id', 'text', 'description']
    df.to_excel('borchestra_achivments.xlsx', index=False)
    

    if ach_secret_list:
        df = pd.DataFrame(ach_secret_list)
    else:
        results = list(zip(['null', 'null'],['null', 'null']))
        df = pd.DataFrame(results, columns=['id', 'text'])
        
    df.columns = ['id', 'text']  
    df.to_excel('borchestra_achivments_secret.xlsx', index=False)
    #_________________________________________

    
    
    print('''







Success!

Whats all!

Done!
''')



if were_files_found == 0:
    print('''

No files found
''')



