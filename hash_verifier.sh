#!/bin/bash

# Function to show script usage
usage() {
    echo "Usage: $0 -f <file> -a <algorithm> -h <hash_to_compare>"
    echo "Supported algorithms: md5, sha1, sha256, sha512"
    exit 1
}

# Verifica che tutti i comandi necessari siano installati
check_requirements() {
    local commands
    if [[ "$(uname -s)" == *CYGWIN* || "$(uname -s)" == *MINGW* || "$(uname -s)" == *MSYS* ]]; then
        commands=(certutil)
    else
        commands=(md5sum sha1sum sha256sum sha512sum)
    fi
    for cmd in "${commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            echo "Error: $cmd is not installed." >&2
            exit 1
        fi
    done
}

# Funzione per calcolare l'hash di un file
calculate_hash() {
    local file=$1
    local algorithm=$2

    if [[ "$(uname -s)" == *CYGWIN* || "$(uname -s)" == *MINGW* || "$(uname -s)" == *MSYS* ]]; then
        output=$(CertUtil -hashfile "$file" $algorithm)

        echo "$output" | sed -n '2p' | tr -d ' \r\n'
    fi
}

debug=false

# Define allowed algorithms
allowed_algorithms=("md2" "md4" "md5" "sha1" "sha256" "sha384" "sha512")

# Adding command-line parameter parsing
while getopts "f:a:h:d" opt; do
    case $opt in
        f) file=$OPTARG ;;
        a) algorithm=$OPTARG ;;
        h) provided_hash=$OPTARG ;;
        *) ;;
    esac
done

# Convert algorithm to lowercase to handle case-insensitive input
algorithm=${algorithm,,}

# If parameters are not provided, request them interactively
if $debug; then
    file="C:\Users\Domenico\Desktop\Parrot-security-6.2_amd64.ova"
    algorithm="md5"
    provided_hash="17743d7852cbfed3c399de5a30c53dd1"
elif [ -z "$file" ] || [ -z "$algorithm" ]; then
    echo "======================================"
    echo "             Hash Checker"
    echo "======================================"
    echo ""
    if [ -z "$file" ]; then
        echo -n "Enter the path of the file to verify: "
        read -r file
        
        if [ -e "$file" ]; then
            echo "File found."
            break
        else
            while true; do
                echo -n "    - ERROR: file does not exist. Please try again: "
                read -r file

                if [ -e "$file" ]; then
                    echo "File found."
                    break
                fi
            done
        fi

        echo ""
    fi
    if [ -z "$algorithm" ]; then
        echo -n "Enter the hashing algorithm (MD2 - MD4 - MD5 - SHA1 - SHA256 - SHA384 - SHA512): "
        read -r algorithm

        algorithm=${algorithm,,}  # Convert to lowercase
        
        if [[ " ${allowed_algorithms[@]} " =~ " ${algorithm} " ]]; then
            break
        else
            while true; do
                echo -n "    - ERROR! Please select a valid algorithm: "
                read -r algorithm

                if [[ " ${allowed_algorithms[@]} " =~ " ${algorithm} " ]]; then
                    break
                fi
            done
        fi
        
        echo ""
    fi
fi

echo "Calculating the $algorithm hash of file..."

# Parameter checks
if [ -z "$file" ] || [ -z "$algorithm" ]; then
    echo "Error: All fields are required."
    exit 1
fi

# Controllo dei prerequisiti
check_requirements



# Calcolo dell'hash
calculated_hash=$(calculate_hash "$file" "$algorithm")

echo "Hash correctly computed.\n"
echo "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"

if [ -z "$provided_hash" ]; then
    echo -n "Enter the hash to compare: "
    read -r provided_hash
    echo ""
fi


# Compare the hash
echo "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
if [ "$calculated_hash" == "$provided_hash" ]; then
    echo "     HASHES ARE DIFFERENT!"
else
    echo "         HASHES MATCH !"
fi
