__author__ = 'ganlu'

aid_retry_list_path = "log/aid_retry_list.txt"
tid_retry_list_path = "log/tid_retry_list.txt"

def check_not_found(input_file, output_file):
    aid_not_found_list = open(input_file, "r")
    aid_retry_list = open(output_file, "w")
    print input_file
    for line in aid_not_found_list:

        if 'failed' in line:
            line = line.replace("failed[not found]:", "").replace("failed[mbid not found]:", "").strip() + '\n'
            aid_retry_list.write(line)
