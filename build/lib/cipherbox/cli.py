#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path


from . import aes_cipher, base64_cipher, xor_cipher

def read_input(args):
    if args.infile:
        return Path(args.infile).read_bytes()
    if args.text is not None:
        return args.text.encode('utf-8')
    return sys.stdin.buffer.read()

def write_output(args, data_bytes: bytes):
    if args.outfile:
        Path(args.outfile).write_bytes(data_bytes)
        print(f"Wrote to {args.outfile}")
    else:
        # print as utf-8 if possible, otherwise base64
        try:
            print(data_bytes.decode('utf-8'))
        except Exception:
            import base64
            print(base64.b64encode(data_bytes).decode('utf-8'))

def main():
    parser = argparse.ArgumentParser(prog='cipherbox', description='Simple encryption/decryption CLI')
    sub = parser.add_subparsers(dest='cmd', required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('--method', choices=['aes', 'base64', 'xor'], required=True)
    common.add_argument('--text', help='Text input (prefer --infile for binary data)')
    common.add_argument('--infile', help='Read input from file')
    common.add_argument('--outfile', help='Write raw bytes to file')


    enc = sub.add_parser('encrypt', parents=[common], help='Encrypt data')
    enc.add_argument('--password', help='Password for AES (required for aes)')
    enc.add_argument('--key', help='Key for XOR (required for xor)')


    dec = sub.add_parser('decrypt', parents=[common], help='Decrypt data')
    dec.add_argument('--password', help='Password for AES (required for aes)')
    dec.add_argument('--key', help='Key for XOR (required for xor)')


    args = parser.parse_args()
    data = read_input(args)

    try:
        if args.cmd == 'encrypt':
            if args.method == 'aes':
                if not args.password:
                    parser.error('AES requires --password')
                out = aes_cipher.encrypt(data, args.password)
                print(out)
            elif args.method == 'base64':
                print(base64_cipher.encrypt(data))
            elif args.method == 'xor':
                if not args.key:
                    parser.error('XOR requires --key')
                print(xor_cipher.encrypt(data, args.key))

        elif args.cmd == 'decrypt':
            if args.method == 'aes':
                if not args.password:
                    parser.error('AES requires --password')
                pt = aes_cipher.decrypt(args.text or data.decode('utf-8'), args.password)
                write_output(args, pt)
            elif args.method == 'base64':
                pt = base64_cipher.decrypt(args.text or data.decode('utf-8'))
                write_output(args, pt)
            elif args.method == 'xor':
                if not args.key:
                    parser.error('XOR requires --key')
                pt = xor_cipher.decrypt(args.text or data.decode('utf-8'), args.key)
                write_output(args, pt)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)



if __name__ == '__main__':
    main()