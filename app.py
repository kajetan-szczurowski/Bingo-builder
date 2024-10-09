import random
    
def get_file_content_as_array(path):
    with open(path, "r", encoding='utf-8') as entries_file:
        lines = entries_file.readlines()
        return lines
    
def get_file_content_as_string(path):
    with open(path, "r", encoding='utf-8') as file:
        return file.read()
    
def save_file(path, content):
    with open(path, "w", encoding='utf-8') as file:
        file.write(content)
    
def compile_entries_lines_into_array(entries_lines):
    entries_array = []
    for line in entries_lines:
        entries_array.append(line.replace('\n',''))
    return entries_array

def get_bingo_entries(path = 'sources/entries.txt'):
    return compile_entries_lines_into_array(get_file_content_as_array(path))

def generate_bingo_html_file(entries_array, html_starting_part, html_ending_part, entry_starting_part, entry_ending_part):
    html_file = html_starting_part + "\n"
    for entry in entries_array:
        html_file += entry_starting_part + entry + entry_ending_part + "\n"
    html_file += html_ending_part
    return html_file

def generate_standard_bingo_html_file(entries_array):
    ENTRY_INTRO_TEXT = "<div class = 'bingo-chunk'><div class = 'chunk-text'>"
    ENTRY_OUTRO_TEXT = "</div></div>"
    HTML_INTRO = get_file_content_as_string('sources/intro.html')
    HTML_OUTRO = get_file_content_as_string('sources/outro.html')
    return generate_bingo_html_file(entries_array, HTML_INTRO, HTML_OUTRO, ENTRY_INTRO_TEXT, ENTRY_OUTRO_TEXT)

def encode_entries_indexes_array(indexes, BASE_LIST):
    result = []
    for index in indexes:
        result.append(BASE_LIST[index])
    return result

def generate_unique_bingos(count, BASE_LIST, export_folder_name = None):
    SHUFFLE_MAX_COUNT = 20
    list_of_taken = []
    dones_count = 0
    entries = [number for number in range(0, len(BASE_LIST))]
    while (dones_count < count):
        is_unique = False
        shuffle_count = 0
        while (not is_unique):
            print('shuffling')
            shuffle_count += 1
            if (shuffle_count > SHUFFLE_MAX_COUNT): raise Exception("Couldn't get unique arrays")
            random.shuffle(entries)
            is_unique = is_entries_array_unique(entries, list_of_taken)
        
        list_of_taken.append(entries.copy())
        dones_count += 1
        if (export_folder_name):
            save_file(export_folder_name + '/bingo_' + str(dones_count) + '.html', generate_standard_bingo_html_file(encode_entries_indexes_array(entries, BASE_LIST)))
        print('created '+ str(dones_count) + '/' + str(count) + ' bingos.')

def is_entries_array_unique(current_array, list_of_taken):
    for taken in list_of_taken:
        if taken == current_array: 
            return False
    return True






ENTRIES_IMMUTABLE_LIST = get_bingo_entries()
generate_unique_bingos(80, ENTRIES_IMMUTABLE_LIST, 'export')
