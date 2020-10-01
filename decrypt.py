import nacl
from nacl.public import PrivateKey,SealedBox
import base64
import sys
from os import path

with open(sys.argv[1], "rb") as key_file:
    private_key = PrivateKey(key_file.read(),encoder=nacl.encoding.Base64Encoder)

if path.exists(sys.argv[3]):
  print(f"file {sys.argv[3]} already exists")
  sys.exit(-1)

with open(sys.argv[3],"w") as output_file:

  with open(sys.argv[2],"rb") as file:
    for line in file.readlines():
      sb=SealedBox(private_key)
      unencrypted=sb.decrypt(line,encoder=nacl.encoding.Base64Encoder)
      print("".join(chr(x) for x in unencrypted),file=output_file)
