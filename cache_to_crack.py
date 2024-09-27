import hashlib
import pickle
import argparse
import string
import time
import sys
import os

lower = string.ascii_lowercase
upper = string.ascii_uppercase
num = string.digits
symbols = "!@#$%^&*?,()-=+[]/;"

class AllStrings:
    def __init__(self, chars="0123456789", min_len=4, max_len=4):
        self.indices = [0] * min_len
        self.chars = chars
        self.max_len = max_len

    def __iter__(self):
        return self

    def __next__(self):
        s = ''.join([self.chars[n] for n in self.indices])
        for m in range(len(self.indices)):
            self.indices[m] += 1
            if self.indices[m] < len(self.chars):
                break
            self.indices[m] = 0
        else:
            if len(self.indices) >= self.max_len:
                raise StopIteration
            self.indices.append(0)
        return s

def timer(start, end):
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)

def crack_looper(all_strings, hashtocrack, outputfile, sessionfile, save_interval=300):
    try:
        start_time = time.time()
        last_save_time = start_time

        for s in iter(all_strings):
            print(f"\rTrying password: {s[::-1]}", end='', flush=True)
            password = s[::-1]
            hashofpassword = hashlib.md5(password.encode("UTF-8")).hexdigest()

            if hashofpassword == hashtocrack:
                print(f"\n[+] Found password: {password}")
                with open(outputfile, "w") as h:
                    h.write(f"{password} : {hashtocrack}")
                break

            # Save the session every 5 minutes or as needed
            if time.time() - last_save_time > save_interval:
                save_session(all_strings, sessionfile, hashtocrack, outputfile)
                last_save_time = time.time()

    except KeyboardInterrupt:
        print("\n[!] Saving session due to keyboard interrupt...")
        save_session(all_strings, sessionfile, hashtocrack, outputfile)
        sys.exit()

def save_session(all_strings, sessionfile, hashtocrack, outputfile):
    with open(sessionfile, "wb") as f:
        pickle.dump(all_strings, f)
    with open(f"{sessionfile}.info", "w") as g:
        g.write(f"{hashtocrack}\n{outputfile}")
    print(f"\n[!] Session saved to {sessionfile}")

def recrack(resumesession):
    try:
        with open(f"{resumesession}.info", "r") as f:
            info = f.read().splitlines()
            hashtocrack = info[0]
            outputfile = info[1]
    except Exception as error:
        print(error)
        sys.exit()

    try:
        with open(resumesession, "rb") as f:
            all_strings = pickle.load(f)
        print(f"[+] Resuming session from {resumesession}")
        crack_looper(all_strings, hashtocrack, outputfile, resumesession)
    except IOError:
        print("Session file not found or corrupted.")
        sys.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--min", type=int, dest="min_len", help="Minimum length of chars")
    parser.add_argument("--max", type=int, dest="max_len", help="Maximum length of chars")
    parser.add_argument("--char", "-c", dest="chars", help="Characters to use in brute force")
    parser.add_argument("--hash", dest="hash", help="MD5 hash to crack")
    parser.add_argument("-n", dest="newsession", help="Session name with path")
    parser.add_argument("-r", dest="resumesession", help="Path of session file")
    parser.add_argument("--output", "-o", dest="outputfile", help="Path of output file")
    args = parser.parse_args()

    char_sets = {"lower": lower, "upper": upper, "num": num, "symbol": symbols}
    characters = ""

    if args.resumesession:
        recrack(args.resumesession)
    elif args.hash and args.outputfile and args.chars:
        if args.min_len and args.max_len:
            if args.min_len > args.max_len:
                print("[-] --max must be greater than or equal to --min")
                sys.exit()

            for c in args.chars.split(","):
                if c in char_sets:
                    characters += char_sets[c]
                else:
                    print(f"Charset {c} not in list")
                    sys.exit()

            print(f"Performing attack with '{characters}'")
            sessionfile = args.newsession if args.newsession else "None"
            all_strings = AllStrings(chars=characters, min_len=args.min_len, max_len=args.max_len)
            crack_looper(all_strings, args.hash, args.outputfile, sessionfile)
        else:
            print("[-] --min and --max are required with --char")
            sys.exit()
    else:
        parser.print_help()
