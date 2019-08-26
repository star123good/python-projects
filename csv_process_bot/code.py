import csv
import sys



category = []
categ_list = []
categ_list_code = []
categ_array = {}
categ_array_code = {}
data = []
data_sku = []
data_product_id = []



def input_csv():
    with open('codes.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        index = 0
        for row in reader:
            index += 1
            if index == 1:
                continue
            category.append(row)
            
    csvFile.close()

    with open('data.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        index = 0
        for row in reader:
            index += 1
            if index == 1:
                continue
            data.append(row)
            data_sku.append(row[1])
            data_product_id.append(row[2])
            
    csvFile.close()



def category_process():
    if len(category) > 0:
        for categ in category:
            if categ[0] in categ_list :
                categ_array[categ[0]].append(categ[2])
                categ_array_code[categ[0]].append(categ[3])
            else :
                categ_list.append(categ[0])
                categ_list_code.append(categ[1])
                categ_array[categ[0]] = []
                categ_array[categ[0]].append(categ[2])
                categ_array_code[categ[0]] = []
                categ_array_code[categ[0]].append(categ[3])



def input_vaild(show_string, valid_list):
    while True:
        value = input(show_string)

        if len(valid_list) > 0:
            flag_result = True
            flag_result_temp = True

            temp_value = ''
            for valid_item in valid_list:
                if valid_item == 'PREFIX':
                    temp_value = valid_list[valid_item] + value
                    break

            for valid_item in valid_list:
                valid_result = get_valid_string(value, valid_item, valid_list[valid_item])
                if valid_result == 'OK':
                    continue
                else:
                    flag_result = False
                    print(valid_result)
                    break
            
            if flag_result == True:
                if temp_value == '':
                    pass
                else :
                    for valid_item in valid_list:
                        if valid_item == 'NONEXIST':
                            valid_result = get_valid_string(temp_value, valid_item, valid_list[valid_item])
                            if valid_result == 'OK':
                                continue
                            else:
                                flag_result_temp = False
                                print(valid_result)
                                break
            
            if flag_result == True and flag_result_temp == True:
                break
        
    return value



def get_valid_string(value, valid_type, valid_value):
    temp_list = []
    if type(valid_value) == list and len(valid_value) > 0:
        for item in valid_value:
            temp_list.append(str(item))

    if valid_type == 'EMPTY':
        if value == '' :
            return 'You must input No empty'
    elif valid_type == 'EXIST':
        if value in temp_list:
            pass
        else :
            return 'You must choice correctly'
    elif valid_type == 'NONEXIST':
        if value in temp_list:
            return 'There is existed already'
    elif valid_type == 'STRLEN':
        try:
            value = int(value)
        except ValueError:
            pass
        if type(value) == int and len(str(value)) == valid_value:
            pass
        else :
            return 'You must input ' + str(valid_value) + ' length integer'
    elif valid_type == 'INTEGER':
        temp_flag = False
        temp_value = value
        try:
            temp_value = int(temp_value)
            if len(str(temp_value)) == len(str(value)):
                temp_flag = True
        except ValueError:
            pass
        if temp_flag == False:
            return 'You must input integer'

    return 'OK'




def get_string_array(string_list):
    str_result = ""
    int_result = []
    index = 1
    for item in string_list:
        if index > 1:
            str_result += "\n"
        str_result += str(index) + ":" + item
        int_result.append(index)
        index += 1
    return (str_result, int_result)


def command_insert():
    print('''================================================
Insert a new item
================================================''')

    sku = input_vaild("Enter SKU:", {
        'EMPTY' : '',
        'NONEXIST' : data_sku
    })

    (catg_temp_str, catg_temp_int) = get_string_array(categ_list)
    catg = int(input_vaild("Choose a Catgory:\n" + catg_temp_str + "\nEnter a Catgory:", {
        'EMPTY' : '',
        'EXIST' : catg_temp_int
    }))

    (catg_temp_str, catg_temp_int) = get_string_array(categ_array[categ_list[catg-1]])
    sub_catg = int(input_vaild("Choose a Sub Catgory:\n" + catg_temp_str + "\nEnter a Sub Catgory:", {
        'EMPTY' : '',
        'EXIST' : catg_temp_int
    }))

    product_id = int(input_vaild("Enter product ID:", {
        'EMPTY' : '',
        'NONEXIST' : data_product_id,
        'STRLEN' : 8,
        'PREFIX' : categ_list_code[catg-1] + '-' + categ_array_code[categ_list[catg-1]][sub_catg-1] + '-'
    }))

    product_name = input_vaild("Enter product name:", {
        'EMPTY' : '',
    })

    stock_level = int(input_vaild("Enter stock level:", {
        'EMPTY' : '',
        'INTEGER' : ''
    }))

    data_sku.append(sku)
    data_product_id.append(categ_list_code[catg-1] + '-' + categ_array_code[categ_list[catg-1]][sub_catg-1] + '-' + str(product_id))
    data.append([
        0,
        sku,
        categ_list_code[catg-1] + '-' + categ_array_code[categ_list[catg-1]][sub_catg-1] + '-' + str(product_id),
        product_name,
        categ_list[catg-1],
        categ_array[categ_list[catg-1]][sub_catg-1],
        stock_level
    ])

    print("\nNew item inserted")



def command_delete():
    print('''================================================
Delete an item
================================================''')
    sku = input_vaild("Enter sku to delete:", {
        'EMPTY' : '',
        'EXIST' : data_sku
    })

    data_sku.remove(sku)
    index = 0
    for item in data:
        if str(item[1]) == str(sku):
            temp_product_id = item[2]
            del data[index]
        index +=1
    data_product_id.remove(temp_product_id)

    print("\nItem deleted")



def command_save():
    filePath = "data.csv"        
    with open(filePath, 'w', newline='') as csvfile:
        fieldnames = ['ROW', 'SKU', 'PRODUCT ID', 'NAME', 'CATEGORY', 'SUB-CATEGORY', 'STOCK LEVEL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        index = 0
        for item in data:
            index += 1
            writer.writerow({
                'ROW' : index, 
                'SKU' : item[1], 
                'PRODUCT ID' : item[2],
                'NAME' : item[3], 
                'CATEGORY' : item[4], 
                'SUB-CATEGORY' : item[5],
                'STOCK LEVEL' : item[6]
            })

    print('''================================================
Save file
================================================
File saved
================================================
================================================
Thank you for using Inventory Management System
================================================''')




def input_cmd():
    while True:
        print('''================================================
1: Insert a new item
2: Delete an item
3: Save data to file and exit''')
        try:
            choice_cmd = int(input("Enter choice:"))
        except ValueError:
            pass
        
        if choice_cmd == 1:
            command_insert()
        elif choice_cmd == 2:
            command_delete()
        elif choice_cmd == 3:
            command_save()
            break
        else:
            print("Invalid choice ")



def main():
    input_csv()
    category_process()
    print('''
================================================
Welcome to Inventory Management System''')
    input_cmd()

if __name__ == '__main__':
    main()