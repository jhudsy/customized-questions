import nacl
from nacl.public import PrivateKey,PublicKey

private_key=PrivateKey.generate()
public_key=private_key.public_key

with open('private.key', 'wb') as f:
    f.write(private_key.encode(encoder=nacl.encoding.Base64Encoder))

with open('public.key', 'wb') as f:
    f.write(public_key.encode(encoder=nacl.encoding.Base64Encoder))
