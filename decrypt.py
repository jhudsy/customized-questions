from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import sys
from os import path

with open(sys.argv[1], "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

if path.exists(sys.argv[3]):
  print(f"file {sys.argv[3]} already exists")
  sys.exit(-1)

with open(sys.argv[3],"w") as output_file:

  with open(sys.argv[2],"rb") as file:
    for line in file.readlines():
      encrypted=base64.b64decode(line)

      unencrypted = private_key.decrypt(
        encrypted,
        padding.OAEP(
          mgf=padding.MGF1(algorithm=hashes.SHA256()),
          algorithm=hashes.SHA256(),
          label=None
        )
      )
      print("".join(chr(x) for x in unencrypted),file=output_file)
