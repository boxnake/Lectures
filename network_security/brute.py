cipher_text = "NCJAEZRCLASJLYODEPRLYZRCLASJLCPEHZDTOPDZQLNZTY"
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def get_plain_character(target, diff):
  return alphabet[(alphabet.find(target)-diff)%26]

for diff in range(1,26):
  plain_text = ''
  for i in range(len(cipher_text)):
    plain_text += get_plain_character(cipher_text[i], diff)
  print("key {0} : {1}".format(diff, plain_text))
