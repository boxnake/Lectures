import sha256

digest = sha256.get_hash_digest_from_file("hello.txt")
print(digest.hex())
digest = sha256.get_hash_digest_from_bytes(digest)
print(digest.hex())