import hashlib
import os


def sanitize_filepath(filepath: str) -> str | None:
    """Remove any double quotes present in the path."""

    # Check if the path is enclosed in double quotes
    path = filepath.strip().strip('"').strip("\n")

    # Check if the path is not a directory
    if os.path.isdir(path):
        print("  > ERROR: Cannot compute the hash of a directory!\n")
        return None

    # Check if the path refers to protected paths (system directories) for both Windows and Linux
    protected_paths = [
        "C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)", "C:\\ProgramData",
        "/bin", "/boot", "/dev", "/etc", "/lib", "/lib64", "/opt", "/proc", "/root", "/sbin", "/sys", "/usr", "/var"
    ]
    for protected_path in protected_paths:
        if path.startswith(protected_path):
            print("  > ERROR: Protected directories cannot be used!\n")
            return None

    # Check if the path refers to a valid file
    if not os.path.isfile(path):
        print("  > ERROR: The path inserted does not refer to a valid file!\n")
        return None

    return path


def sanitize_hash(_hash: str) -> str | None:
    """Remove any spaces or double quotes present in the hash."""

    _hash = _hash.strip().strip('"').strip("\n").replace(" ", "")

    # Check if the hash is valid
    if len(_hash) == 0:
        print("  > ERROR: The hash provided is empty!\n")
        return None

    return _hash


def calculate_file_hash(filepath: str, hash_function: str) -> str | None:
    """Compute the hash of the file using the provided algorithm."""

    hash_func = getattr(hashlib, hash_function)
    hasher = hash_func()

    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        print(f"  > ERROR: {e}")
        return None


def main():
    # print("       _   _           _       _   _           _  __ _                 ")
    # print("      | | | |         | |     | | | |         (_)/ _(_)                ")
    # print("      | |_| | __ _ ___| |__   | | | | ___ _ __ _| |_ _  ___ _ __       ")
    # print("      |  _  |/ _` / __| '_ \  | | | |/ _ \ '__| |  _| |/ _ \ '__|      ")
    # print("      | | | | (_| \__ \ | | | \ \_/ /  __/ |  | | | | |  __/ |         ")
    # print("      \_| |_/\__,_|___/_| |_|  \___/ \___|_|  |_|_| |_|\___|_|         ")

    print("\n<- - - - - - - - - - - - - - VERIFY THE INTEGRITY OF A FILE USING ITS HASH - - - - - - - - - - - - - ->\n")

    while True:
        filepath = input("Enter the path of the file (double quotes will be removed): ")
        filepath = sanitize_filepath(filepath)

        if filepath is not None:
            print(f"Path sanitized: {filepath}")
            break

    print()
    while True:
        provided_hash = input("Enter the provided digest: ")
        provided_hash = sanitize_hash(provided_hash)

        if provided_hash is not None:
            break

    print("\n<- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ->\n")

    print("Available Hash functions:\n", hashlib.algorithms_available, "\n")
    while True:
        hash_function = input("Enter the hash algorithm to use: ").strip().lower().replace("\n", "")

        if hash_function not in hashlib.algorithms_available:
            print("  > ERROR: The hash function selected is not valid (or not supported).\n")
        else:
            break

    file_hash = calculate_file_hash(filepath, hash_function)
    if file_hash is None:
        return

    print("\n<- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ->\n")

    print(f"PROVIDED HASH: {provided_hash}")
    print(f"COMPUTED HASH: {file_hash}")

    if file_hash == provided_hash:
        print("\nResult  -->  DIGESTS ARE EQUAL. Integrity verified.")
    else:
        print("\nResult  -->  DIGESTS ARE DIFFERENT! Integrity compromised.")


if __name__ == "__main__":
    main()
