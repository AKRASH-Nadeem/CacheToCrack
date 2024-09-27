# CacheToCrack

CacheToCrack is a proof-of-concept (POC) tool designed for cracking MD5 hashes through a systematic brute-force approach. This project focuses on building a logical structure for password generation and management, showcasing the effectiveness of custom algorithms in hash cracking.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Session Management](#session-management)
- [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)

## Introduction

In the world of cybersecurity, understanding the intricacies of hash functions and password cracking is essential. CacheToCrack aims to provide a user-friendly interface for users to experiment with hash cracking techniques while maintaining a focus on logical structuring and efficiency.

## Features

- **Brute-force Password Cracking:** Attempts to crack MD5 hashes using a defined character set.
- **Custom Character Sets:** Users can specify the characters to include in the cracking process.
- **Session Management:** Saves progress automatically every five minutes and upon user interruption.
- **User-Friendly Interface:** Clear prompts and feedback during the cracking process.

## Usage

To use CacheToCrack, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/CacheToCrack.git
   cd CacheToCrack
   ```

2. required packages:
    - __hashlib__ (built-in)
    - __pickle__ (built-in)
    - __argparse__ (built-in)
    - __string__ (built-in)
    - __time__ (built-in)
    - __sys__ (built-in)
    - __os__ (built-in)

3. Run the tool:
   ```bash
   python cache_to_crack.py --hash <your_md5_hash> --char <characters_to_use> --output <output_file_path>
   ```

4. Use __Session__ saving:
    ```bash
    python cache_to_crack.py --hash <your_md5_hash> --char <characters_to_use> --output <output_file_path> -n session
    ```

    To __Resume__ the session:

    ```bash
    python cache_to_crack.py -r session
    ```


## How It Works

CacheToCrack utilizes a custom class to generate all possible strings within the specified length limits and character sets. Each generated string is hashed using MD5 and compared against the target hash. If a match is found, the corresponding password is stored and displayed.

The password generation is designed to be efficient, allowing for the systematic exploration of the search space defined by the user.

## Session Management

To enhance user experience, CacheToCrack implements session management that automatically saves the current state of the cracking process. This feature allows users to pause and resume their work without losing progress. Sessions are saved every five minutes and upon receiving a termination signal (like Ctrl+C).

## Installation

Ensure you have Python 3.8 or higher installed. All required packages are built-in python so don't need to install any

## Contributing

**Contributions** are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.
I would Like if someone can help to use this script with parallel processing, Parallel processing won't be easy because the script is saving session.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
