
test_list = [1, 2, [3], [4, [5, 6]], [[7]], 8]


def get_one_list(my_list, result):
    for value in my_list:
        if type(value) == list:
            get_one_list(value, result)
        else:
            result.append(value)


my_result = []
get_one_list(test_list, my_result)
print(my_result)