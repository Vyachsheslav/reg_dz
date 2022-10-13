import re
import csv
import pandas as pd


def read_file(file_name):
    with open(file_name,  encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


def format_number(contacts_list):
    pattern_raw = r'(\+7|8)(\s*)(\(*)(\d{3})(\)*)(\s*)' \
                            r'(\-*)(\d{3})(\s*)(\-*)(\d{2})(\s*)(\-*)' \
                            r'(\d{2})(\s*)(\(*)(доб)*(\.*)(\s*)(\d+)*(\)*)'
    pattern_new = r'+7(\4)\8-\11-\14\15\17\18\19\20'
    contacts_list_updated = list()
    for card in contacts_list:
        card_as_string = ','.join(card)        
        formatted_card = re.sub(pattern_raw, pattern_new, card_as_string)        
        card_as_list = formatted_card.split(',')        
        contacts_list_updated.append(card_as_list)
    return contacts_list_updated


def full_name(contacts_list):
    pattern_raw = r'^([А-ЯЁа-яё]+)(\s*)(\,?)([А-ЯЁа-яё]+)' \
                       r'(\s*)(\,?)([А-ЯЁа-яё]*)(\,?)(\,?)(\,?)'
    pattern_new = r'\1\3\10\4\6\9\7\8'
    contacts_list_updated = list()
    for card in contacts_list:
        card_as_string = ','.join(card)
        formatted_card = re.sub(pattern_raw, pattern_new, card_as_string)
        card_as_list = formatted_card.split(',')
        contacts_list_updated.append(card_as_list)
    return contacts_list_updated


def join_duplicates(contacts_list):
    for i in contacts_list:
        for j in contacts_list:
            if i[0] == j[0] and i[1] == j[1] and i is not j:
                if i[2] == '':
                    i[2] = j[2]
                if i[3] == '':
                    i[3] = j[3]
                if i[4] == '':
                    i[4] = j[4]
                if i[5] == '':
                    i[5] = j[5]
                if i[6] == '':
                    i[6] = j[6]
    contacts_list_updated = list()
    for card in contacts_list:
        if card not in contacts_list_updated:
            contacts_list_updated.append(card)
    return contacts_list_updated

def drop_duplicates():
    df = pd.read_csv('phonebook_update.csv',delimiter=',',error_bad_lines=False)
    df.drop_duplicates(subset=['lastname']).to_csv('phonebook.csv', index=False)


def update_phonebook(contacts_list):
    with open("phonebook_update.csv", "w",  encoding="utf-8") as f:
        data_writer = csv.writer(f, delimiter=',')
        data_writer.writerows(contacts_list)


if __name__ == '__main__':
    contacts = read_file('phonebook_raw.csv')
    contacts = format_number(contacts)    
    contacts = full_name(contacts)
    contacts = join_duplicates(contacts)    
    update_phonebook(contacts)
    drop_duplicates()
    