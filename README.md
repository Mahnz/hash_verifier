[//]: # (Generate a README file, explaining what the Python script `hash_verifier.py` does, and briefly how it works)

# Hash Verifier

Hash Verifier is a Python script realized to verify the integrity of a file. Given its path, the script is able to
compute the hash of the file and compare it with a given one (e.g., provided by the files author).
To facilitate the process, the script offers a command-line interface to guide the user in the process.

The project uses the `hashlib` library in Python. Hence, the available hash algorithms are the ones supported by
`hashlib`:

{ `sha224`, `sha256`, `md5`, `sha512`, `sm3`, `sha1`, `sha384`, `md5-sha1`, `shake_256`, `sha512_224`,
`sha3_224`, `sha3_384`, `blake2b`, `shake_128`, `ripemd160`, `sha3_512`, `sha512_256`, `sha3_256`, `blake2s` }

## How it works

The script's execution proceeds as follows:

1) The user provides the path to the file to be verified and the hash to compare with.
   It does not allow to use files in **protected directories** (e.g., `C:\Windows`, `C:\Program Files`, `/etc`, `/bin`,
   etc.).
2) The user inputs the digest provided by the author of the file.
3) The user is prompted to choose the hash algorithm to use for verification.
4) The script computes the hash of the file and compares it with the given one.

If the hashes match, the script outputs a message indicating that the file is valid.

## Usage

To use the script, run the following command in the terminal:

```bash
python hash_verifier.py
```

The script will guide you through the verification process.

