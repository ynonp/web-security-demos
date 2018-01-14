import nacl.encoding
import sys
import binascii
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac

def read_in_chunks(file_object, chunk_size=16 * 1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 16k."""
    index = 0
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield (data, index)
        index += 1

if len(sys.argv) != 3:
    sys.exit("Usage: {} <auth_key> <input_file>".format(sys.argv[0]))

(_, key_file, input_file) = sys.argv

with open(key_file, 'rb') as f:
    auth_key = f.read()

with open(input_file, 'rb') as f:
    h = hmac.HMAC(auth_key, hashes.SHA512(), backend=default_backend())
    for chunk, _ in read_in_chunks(f):
        h.update(chunk)

    print(binascii.hexlify(h.finalize()))
