#!/usr/bin/env python3
import argparse
import sys
import shlex
from pathlib import Path
import os

from . import aes_cipher, base64_cipher, xor_cipher


def load_banner():
    banner_path = os.path.join(os.path.dirname(__file__), "banner.txt")
    try:
        with open(banner_path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "CRYPTX - by bima"


def read_file_or_text(args):
    if args.infile:
        return Path(args.infile).read_bytes()
    if args.text:
        return args.text.encode("utf-8")
    return sys.stdin.buffer.read()


def write_output(args, data):
    if args.outfile:
        out = Path(args.outfile)
        out.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, bytes):
            out.write_bytes(data)
        else:
            out.write_text(data, encoding="utf-8")
        print(f"[OK] Saved to {out}")
    else:
        print(data.decode("utf-8") if isinstance(data, bytes) else data)

class SilentArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)

def handle(tokens):
    parser = SilentArgumentParser(add_help=False)
    sub = parser.add_subparsers(dest="cmd")

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--method", choices=["aes", "base64", "xor"])
    common.add_argument("--text")
    common.add_argument("--infile")
    common.add_argument("--outfile")

    enc = sub.add_parser("encrypt", parents=[common])
    enc.add_argument("--password")
    enc.add_argument("--key")

    dec = sub.add_parser("decrypt", parents=[common])
    dec.add_argument("--password")
    dec.add_argument("--key")

    try:
        args = parser.parse_args(tokens)
    except:
        print(f"[ERR] Invalid command: {' '.join(tokens)}")
        print("Type 'help' to see available commands.\n")
        return


    if args.cmd == "encrypt":
        data = read_file_or_text(args)

        if args.method == "aes":
            out = aes_cipher.encrypt(data, args.password)
        elif args.method == "base64":
            out = base64_cipher.encrypt(data)
        elif args.method == "xor":
            out = xor_cipher.encrypt(data, args.key)

        write_output(args, out)

    elif args.cmd == "decrypt":
        data = read_file_or_text(args)

        if args.method == "aes":
            out = aes_cipher.decrypt(data, args.password)
        elif args.method == "base64":
            out = base64_cipher.decrypt(data.decode("utf-8"))
        elif args.method == "xor":
            out = xor_cipher.decrypt(data.decode("utf-8"), args.key)

        write_output(args, out)

    else:
        print(f"[ERR] Invalid command: {' '.join(tokens)}")
        print("Type 'help' to see available commands.\n")

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(load_banner())
    print("\n Welcome to CRYPTX interactive shell")
    print("Type 'help' for commands.\n")

    while True:
        try:
            cmd = input("cryptx> ").strip()
        except EOFError:
            break

        # === Empty input (Enter) → skip ===
        if cmd == "":
            continue

        # === Exit app ===
        if cmd in ("quit", "exit"):
            print("Goodbye!")
            break

        # === Clear screen ===
        if cmd == "clear":
            os.system("cls" if os.name == "nt" else "clear")
            continue

        # === Help menu ===
        if cmd == "help":
            print("""
Available Commands:

  • Encrypt file:
       encrypt --method aes --infile input.txt --outfile out.enc --password mypass
       encrypt --method xor --infile input.txt --outfile out.enc --key 12
       encrypt --method base64 --infile input.txt --outfile out.txt

  • Encrypt text:
       encrypt --method aes --text "hello bima" --password mypass
       encrypt --method xor --text "hello" --key 10
       encrypt --method base64 --text "hello"

  • Decrypt file:
       decrypt --method aes --infile out.enc --outfile original.txt --password mypass
       decrypt --method xor --infile out.enc --outfile original.txt --key 12
       decrypt --method base64 --infile out.txt --outfile original.txt

  • Decrypt text:
       decrypt --method aes --text "<cipher>" --password mypass
       decrypt --method xor --text "7f565b..." --key 7
       decrypt --method base64 --text "aGVsbG8="

Special Commands:
  help     — show command list
  clear    — clear terminal screen
  exit     — quit CRYPTX
""")
            continue

        # === If has content, handle command ===
        handle(shlex.split(cmd))

