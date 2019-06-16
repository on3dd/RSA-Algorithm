# coding: utf8

text = open('input.txt','r').read()
char_arr = []

for char in text:
  if len(str(ord(char))) < 3:
    char_arr.append('0' + str(ord(char)))
  else:
    char_arr.append(ord(char))

print(char_arr)
