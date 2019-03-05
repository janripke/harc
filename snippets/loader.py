# guess the header


class Delimiter:

    @staticmethod
    def count(s, delimiters=list()):
        result = dict()
        for char in s:
            if char in delimiters:
                if char in result.keys():
                    result[char] = result[char] + 1
                else:
                    result[char] = 1
        return result

    @staticmethod
    def guess(s, delimiters=[';', ':', ' ', '|', '~', '#']):
        result = None
        d = Delimiter.count(s, delimiters)
        if d:
            for key in d.keys():
                value = -1
                if d[key] > value:
                    result = key
                    value = d[key]
        return result


# create a dictionary containing the found delimiters and the count.
s = 'id;email;surname;my;zip'





# d = Delimiter.count(s)
# print(d)
delimiter = Delimiter.guess(s)
print(delimiter)


d = dict()
for c in s:
    if c in [';', ':', ' ', '|', '~', '#']:
        if c in d.keys():
            d[c] = d[c] + 1
        else:
            d[c] = 1

print(d)

# retrieve the winning character
result = None
for key in d.keys():
    value = -1
    if d[key] > value:
        result = key
        value = d[key]

print(result)





#
# def guess_delimiter(filename):
#     f = open(filename, 'rb')
#     line = f.readline()
#     f.close()
#     characters = []
#     for s in line:
#         found = False
#         for c in characters:
#             if c[0] == s:
#                 found = True
#             c[1] = c[1] + 1
#         if not found and s in [';', ':', ' ', '|', '~', '#']:
#             characters.append([s, 1])
#             characters.sort(reverse=True)
#     return characters[0][0]
