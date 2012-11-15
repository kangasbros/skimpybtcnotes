# Skimpy Bitcoin Notes

Print cost-effective bitcoin banknotes!

This script can generate "storage sheets" and "banknotes".

## Usage & Installation

Requires reportlab PIL, qrcode and bitcoin vanitygen

## Examples

Generate one sheet of storage sheets:

    python generate.py 

Generate two sheets of foldable notes

    python generate.py -n 2 -b

Foldable sheet with all bitcoin addresses starting with "1ZZ"

    python generate.py -b -s 1ZZ

## Licence and authors

Licence is Public domain - modify and share.

This script is from the authors of [LocalBitcoins.com](https://localbitcoins.com) and [EasyWallet.org](https://easywallet.org)

[LocalBitcoins.com](https://localbitcoins.com) - set up your own local bitcoin to cash exchange and start making money!

[EasyWallet.org](https://easywallet.org) - easy browser-based bitcoin wallet solution, works on any device with a web browser!