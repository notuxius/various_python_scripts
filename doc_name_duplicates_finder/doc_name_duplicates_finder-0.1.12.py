#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  name: DNDF - Doc Name Duplicates Finder
#  purpose: finds duplicate persons in tables in doc_files_folder and shows them


# TODO refactor, optimize, translate folder names and messages, document and take more try except
# TODO maybe local global variables rename, localize, rename variables to var_name convention, make contants for messages


import os
import sys
import time
import win32com.client
from tqdm import *


def sanity_encoding(in_string):
    # TODO crunch - needed work with encoding symbols display
    out_string = in_string.replace("і", "i")
    out_string = out_string.replace("І", "I")
    out_string = out_string.replace("’", "'")
    return out_string


# file_names
all_persons = sanity_encoding("всі особи.txt")
duplicates = sanity_encoding("тимчасові дублікати.txt")
sorted_duplicates = sanity_encoding("відсортовані тимчасові дублікати.txt")
time_str = time.strftime("-%Y-%m-%d-%H-%M-%S")
final = sanity_encoding("остаточні-дублікати" + time_str + ".txt")
script_path = os.path.dirname(os.path.abspath(sanity_encoding(__file__)))
doc_files_folder = (os.path.join(script_path, sanity_encoding("ПАПКА ДЛЯ ДОКУМЕНТІВ")))
doc_files_list = []
    

# messages in english outdated
# no_doc_folder_found = "no " + doc_files_folder + " found, creating new one"
# is_empty = sanity_encoding(" is empty")
# found_temporary = sanity_encoding("found temporary Word file, skipping: ")
# found_word_2007 = sanity_encoding("found Word 2007+ document, skipping: ")
# not_a_document = sanity_encoding("not a document file, skipping: ")
# no_tables_found = sanity_encoding("no tables found in the document: ")
# processing_and_adding = sanity_encoding("processing and adding duplicates to file ")
# duplicates_opening = sanity_encoding("file containing duplicates opening")
# interrupted_not_all = sanity_encoding("interrupted, not all files processed")
# duplicates_not_found = sanity_encoding("duplicates not found")
# error_end_winword = sanity_encoding("error occured, you may End Process \"WINWORD.EXE\" in Task Manager")
# error_word_not_installed = sanity_encoding("error occurred, perhaps Word is not installed")
# enter_to_exit = sanity_encoding("Enter to exit")
# scanning = "scanning files"


# messages in ukrainian
no_doc_folder_found = sanity_encoding("не знайдено папки для документів, створюється нова\nдублікати у файлах будуть шукатися в цій папці")
empty_folder = sanity_encoding("папка для документів порожня\nдублікати у файлах будуть шукатися в цій папці")
found_temporary = sanity_encoding("знайдено тимчавий файл Word, пропускається: ")
found_word_2007 = sanity_encoding("знайдено документ Word 2007+, пропускається: ")
not_a_document = sanity_encoding("не файл документу, пропускається: ")
no_tables_found = sanity_encoding("не знайдено таблиць у документі: ")
processing_and_adding = sanity_encoding("обробляються да додаються дублікати до файлу ")
duplicates_opening = sanity_encoding("відкривається текстовий файл з дублікатами")
interrupted_not_all = sanity_encoding("перервано, не всі файли оброблено")
duplicates_not_found = sanity_encoding("дублікатів не знайдено")
error_end_winword = sanity_encoding("виникла помилка, ви можете Завершити процес \"WINWORD.EXE\" у Диспетчері завдань")
error_word_not_installed = sanity_encoding("виникла помилка, можливо Word не встановлений")
enter_to_exit = sanity_encoding("Enter щоб вийти")
scanning = sanity_encoding("скануються файли")


def init_checks():
    if os.path.isfile(all_persons):
        os.remove(all_persons)

    if os.path.isfile(duplicates):
        os.remove(duplicates)

    if os.path.isfile(sorted_duplicates):
        os.remove(sorted_duplicates)

    if os.path.isfile(final):
        os.remove(final)


    if not os.path.exists(doc_files_folder):
        print(no_doc_folder_found)
        os.makedirs(doc_files_folder)
        to_exit()


def create_files_list():
    # list files in folders os.walk()
    for doc_path, _, doc_files in os.walk(doc_files_folder):
        # rethink redo
        # print("adding path to search query: " + os.path.relpath(sanity_encoding(doc_path)))
        if os.listdir(doc_files_folder) == []:
            print(empty_folder)
            to_exit()
        else:
            for doc_name in doc_files:

                if doc_name.startswith("~$") or doc_name.startswith(".~") or doc_name.endswith(".tmp"):
                    print(found_temporary + os.path.join(os.path.relpath(sanity_encoding(doc_path)), sanity_encoding(doc_name)))
                    continue

                if doc_name.endswith(".docx"):
                    print(found_word_2007 + os.path.join(os.path.relpath(sanity_encoding(doc_path)), sanity_encoding(doc_name)))
                    continue

                # make with lower()
                if doc_name.endswith((".doc", ".DOC")):
                    doc_files_list.append(os.path.join(doc_path, doc_name))

                else:
                    print(not_a_document + os.path.join(os.path.relpath(sanity_encoding(doc_path)), sanity_encoding(doc_name)))
                    continue


def pull_name_from_table(doc_file, word):
    doc = word.Documents.Open(os.path.abspath(doc_file))

    if doc.Tables.Count < 1:
        print(no_tables_found + os.path.relpath(sanity_encoding(doc_file)))
        doc.Close()
        word.Quit()
        return False

    table = doc.Tables(1)

    # by id or what
    if table.Columns.Count < 4:
        doc.Close()
        word.Quit()
        return False


    people_list = []
    # make it for row id instead of rows count?
    for i in range(2, table.Rows.Count + 1):
        if len(table.Cell(Row=i, Column=4).Range.Text.strip()) < 3:
            continue
        else:
            people_list.append(table.Cell(Row=i, Column=4).Range.Text)


    people_list = [person.replace("\r\x07", "") for person in people_list]

    # print(people_list)
    # better formating - fixed width with person name
    with open(all_persons, "a+") as file_in:
        for item in people_list:
            item = item.strip()
            # all_persons.write(item + "\n")
            # file_in.write(item + " -> " + os.path.abspath(doc_file) + "\n")
            file_in.write(item + " -> " + os.path.relpath(doc_file) + "\n")
        file_in.close()
        doc.Close()
        word.Quit()


    # make in lower case all entries? from what file, if from same file highlight it
    lines_name_seen = {}
    with open(duplicates, "w+") as file_out:
        for line in open(all_persons, "r"):
            # print(line)
            line_split = line.split(" -> ")
            line_name = line_split[0]
            line_file = line_split[1]
            if line_name not in lines_name_seen:
                lines_name_seen[line_name] = line_file
            else:
                # line = line + "\n"
                # line = line.strip()
                # line = line + " -> " + os.path.abspath(doc_file) + "\n"

                file_out.write(line_name + " -> " + lines_name_seen[line_name] + line + "\n")

        # print(lines_name_seen)
        file_out.close()

        line_list = []
        with open(duplicates, "r") as dup:
            for line in dup:
                if len(line) > 1:
                    line_list.append(line)
            line_list.sort()
            dup.close()

        with open(sorted_duplicates, "w+") as sort_dup:
            for item in line_list:
                sort_dup.write(item)
            sort_dup.close()

        lines_name_seen_sorted = []
        with open(sorted_duplicates, "r") as uniq_dup:
            for line in uniq_dup:
                # line = line.strip()
                # if len(line) < 1:
                    # continue
                # else:
                if line in lines_name_seen_sorted:
                    # TODO replace line with line + 1 and what to do with 3 and so on lines?
                    # replace +1
                    # lines_name_seen_sorted.append(line)
                    continue
                else:
                    lines_name_seen_sorted.append(line)
            # print(lines_name_seen_sorted)

            uniq_dup.close()
        
        
        with open(final, "w+") as uniq_dup_deleted:
            # print(processing_and_adding + sanity_encoding(final))
            for item in lines_name_seen_sorted:
                item = item.replace("\n", "")
                
                # maybe add spinner
                # print("processing... " + sanity_encoding(item))
                uniq_dup_deleted.write("%s\n" % item)
            uniq_dup_deleted.close()

    # clear the screen
    # print(chr(27) + "[2J")
    # subprocess.call("cls", shell=True)

    
def create_word_instanses():
    # dont display progressbar if no files in targeted folder
    if len(doc_files_list) != 0:
        for doc_file in tqdm(doc_files_list, desc=scanning, leave=True):
            word = win32com.client.DispatchEx("Word.Application")
            word.Visible = False
            pull_name_from_table(doc_file, word)


def post_checks():
    if os.path.isfile(final) and not os.stat(final).st_size == 0:
        print(duplicates_opening)
        os.system("start " + final)

    if os.path.isfile(duplicates) and os.stat(duplicates).st_size == 0 or not os.path.isfile(duplicates):
        print(duplicates_not_found)
        
def to_exit():
    try:
        input(enter_to_exit)
        sys.exit()

    except SystemExit:
        sys.exit()
    
    except:
        pass


try:
    init_checks()
    create_files_list()
    create_word_instanses()
    post_checks()
    to_exit()

# TODO crunch rework
except SystemExit:
    sys.exit()

except KeyboardInterrupt:
    print(interrupted_not_all)
    try:
        word.Quit()
    except:
        print(error_end_winword)
        to_exit()

# TODO better error handling
except:
    try:
        word.Quit()
    except:
        print(error_word_not_installed)
        to_exit()
