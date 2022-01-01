import os
import sys
import hashlib


dict_files = {}


def delete_files(num_vs_filepath):
    free_space = 0
    while True:
        print("Delete files?")
        delete_files_req = input()
        if delete_files_req == "yes" or delete_files_req == "no":
            print("")
            break
        print("\nWrong option\n")

    if delete_files_req == "yes":
        while True:
            print("Enter file numbers to delete:")
            delete_files_req = input().split()
            if len(delete_files_req) == 0:
                print("\nWrong option\n")
                continue
            all_inputs_good = True
            try:
                for num in delete_files_req:
                    if int(num) not in num_vs_filepath:
                        all_inputs_good = False
                        print("\nWrong option\n")
                        break
                if all_inputs_good:
                    break
            except ValueError:
                print("\nWrong option\n")

        for num, filepath in num_vs_filepath.items():
            if str(num) in delete_files_req:
                free_space += os.path.getsize(filepath)
                os.remove(filepath)

        print("\nTotal freed up space: {} bytes".format(free_space))


def print_by_size(dict_f, file_f, sorting_o, is_hash):
    dict_f_copy = dict_f.copy()
    if file_f != "":
        for key in dict_f.keys():
            if key.split(".")[-1] != file_f:
                del dict_f_copy[key]
    sizes_list = list(dict.fromkeys(list(dict_f_copy.values())))
    if sorting_o == '1':
        sizes_list.sort(reverse=True)
    else:
        sizes_list.sort()
    if not is_hash:
        for size in sizes_list:
            print(size, "bytes")
            for key, value in dict_f_copy.items():
                if value == size:
                    print(key)
            print("")
    else:
        dict_files_hash = {}
        dict_size_hash = {}
        num_vs_filepath = {}
        for key, value in dict_f_copy.items():
            hash_result = hashlib.md5(open(key, 'rb').read()).hexdigest()
            dict_files_hash[key] = hash_result
            if value in dict_size_hash:
                dict_size_hash[value].append(hash_result)
            else:
                dict_size_hash[value] = [hash_result]
        for k, v in dict_size_hash.items():
            dict_size_hash[k] = list(dict.fromkeys(v))
        num_of_files = 0
        for size in sizes_list:
            print(size, "bytes")
            for h in dict_size_hash[size]:
                if sum(k == h for k in dict_files_hash.values()) > 1:
                    print("hash:", h)
                    for key, value in dict_files_hash.items():
                        if value == h:
                            num_of_files += 1
                            print(str(num_of_files) + ".", key)
                            num_vs_filepath[num_of_files] = key
            print("")
        delete_files(num_vs_filepath)


try:
    for root, dirs, files in os.walk(sys.argv[1], topdown=True):
        for name in files:
            dict_files[os.path.join(root, name)] = os.path.getsize(os.path.join(root, name))
except IndexError:
    print("Directory is not specified")


print("Enter file format:")
file_format = input()

print("\nSize sorting options:\n1. Descending\n2. Ascending\n")
while True:
    print("Enter a sorting option:")
    sorting_option = input()
    if sorting_option == "1" or sorting_option == "2":
        print("")
        break
    print("\nWrong option\n")

print_by_size(dict_files, file_format, sorting_option, False)

while True:
    print("\nCheck for duplicates?")
    check_duplicates = input()
    if check_duplicates == "yes" or check_duplicates == "no":
        print("")
        break
    print("\nWrong option\n")

if check_duplicates == "yes":
    print_by_size(dict_files, file_format, sorting_option, True)
