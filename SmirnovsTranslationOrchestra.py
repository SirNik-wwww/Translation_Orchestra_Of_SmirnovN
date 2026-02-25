from array import ArrayType
import array
import pandas as pd

import os
import re


#all need tables
chars_id_tab = []
chars_names_tab = []

enemies_id_tab = []
enemies_names_tab = []

items_list = []

abil_list = []

ach_id_tab = []
ach_names_tab = []
ach_desc_tab = []
ach_sub_tab = []


#C:\TranslationDecopMods\grfl\GreasyFoolsDeluxe
#C:\TranslationDecopMods\KrillPack
#C:\TranslationDecopMods\EnemyPack\NewEnemyPack
folder_with_cs_files = r'C:\TranslationDecopMods\KrillPack'




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
        potential_blocks = re.findall(r'\{[^{}]*?Item_ID\s*=.*?\}|new\s+\w*?PerformEffect_Item.*?Description\s*=\s*".*?"', content, re.DOTALL)

        fields = {
            'Item_ID': r'Item_ID\s*=\s*"(.*?)"',
            'Name': r'Name\s*=\s*"(.*?)"',
            'Description': r'Description\s*=\s*"(.*?)"',
            'Flavour': r'Flavour\s*=\s*".*?"(.*?)"'}

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
        potential_blocks = re.findall(r'new\s*Ability.*?Description\s*=\s*".*?"', content, re.DOTALL)

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



process_folder(folder_with_cs_files)


print(chars_id_tab)
print(chars_names_tab)



#_______ Characters ______________________

#Expanding lists to the same length
while len(chars_id_tab) > len(chars_names_tab):
    chars_names_tab.append('nope')
    print(chars_names_tab)

while len(chars_id_tab) < len(chars_names_tab):
    chars_id_tab.append('nope')
    print(chars_id_tab)


results = list(zip(chars_id_tab,chars_names_tab))
df = pd.DataFrame(results, columns=['id', 'name'])
df.to_excel('borchestra_chars.xlsx', index=False)
#_________________________________________


#_______ Enemies ______________________

#Expanding lists to the same length
while len(enemies_id_tab) > len(enemies_names_tab):
    enemies_names_tab.append('nope')
    print(enemies_names_tab)

while len(enemies_id_tab) < len(enemies_names_tab):
    enemies_id_tab.append('nope')
    print(enemies_id_tab)


results = list(zip(enemies_id_tab,enemies_names_tab))
df = pd.DataFrame(results, columns=['id', 'name'])
df.to_excel('borchestra_enemies.xlsx', index=False)
#_________________________________________


#_______ Items ___________________________
df = pd.DataFrame(items_list)
            # Переименуем столбцы для красоты
df.columns = ['Id', 'Name', 'description', 'subdescription']
            
df.to_excel(r'E:\TranslationOrchestraOfSmirnovN\SmirnovsTranslationOrchestra\borchestra_items.xlsx', index=False)
#_________________________________________



#_______ Abils ___________________________
df = pd.DataFrame(abil_list)
            # Переименуем столбцы для красоты
df.columns = ['Id', 'Name', 'description']
            
df.to_excel(r'E:\TranslationOrchestraOfSmirnovN\SmirnovsTranslationOrchestra\borchestra_abils.xlsx', index=False)
#_________________________________________