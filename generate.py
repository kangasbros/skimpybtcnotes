# coding=utf-8
# vim: ai ts=4 sts=4 et sw=4

import os
import sys
import re
import commands
import urllib2
from time import sleep
import random
import codecs
import base64

import urllib
import re
import qrcode
import StringIO
import subprocess

 # coding=utf-8
# vim: ai ts=4 sts=4 et sw=4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm  
from reportlab.platypus import Frame, Image
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-n", "--num_pages", dest="num_pages",
                  help="number of pages", type="int", default=1)
parser.add_option("-p", "--vanitygen_path", dest="vanitygen_path",
                  help="vanitygen executable path", type="string", default="vanitygen")
parser.add_option("-s", "--vanitygen_start", dest="vanitygen_start",
                  help="vanitygen bitcoin address pattern", type="string", default="1")
parser.add_option("-b", "--bank_notes",help="print foldable banknotes instead of storage sheets", 
                      action="store_true", dest="bank_notes", default=False)

(options, args) = parser.parse_args()

pdfmetrics.registerFont(TTFont('UbuntuM', 'Ubuntu-M.ttf'))
pdfmetrics.registerFont(TTFont('UbuntuBI', 'Ubuntu-BI.ttf'))

def print_notes_pdf(num_pages = 1):
    banknote_series = base64.b64encode(os.urandom(8))
    c = canvas.Canvas("banknotes.pdf", pagesize=A4)
    c.setFont("UbuntuM", 6)
    for page_num in range(0, num_pages):
        c.drawString(0.5*cm, (29.7-0.7)*cm, "Series: "+banknote_series+" Page: "+str(page_num))
        addresses = []
        for i in range(0, (3*9)):
            output = subprocess.Popen([options.vanitygen_path, options.vanitygen_start], stdout=subprocess.PIPE).communicate()[0]
            address = re.compile(u"(1[\w]{25,45})").search(output).group(1)
            addresses.append(address)
            privkey = re.compile(u"(5[\w]{45,75})").search(output).group(1)
            width, height = (16.8*cm, 9*cm)
            x = i % 3
            y = (i - (i % 3)) / 3
            top = (29.7 - 1 - 3*y)*cm
            left = (1+6.3*x)*cm

            print x, y, top, left
            
            # c.drawCentredString(((1+(20/3)*(i%3)))*cm, (29.7-2*((i-i%3)/3))*cm, address)
            # c.drawCentredString(((1+(20/3)*(i%3)))*cm, (29.7-1*((i-i%3)/3))*cm, privkey)

            img = qrcode.make(address, box_size=2)
            output = StringIO.StringIO()
            img.save(output, "PNG")
            output.seek(0)
            c.drawImage(ImageReader(output), left+0.3*cm, top-2.7*cm, 2.4*cm, 2.4*cm, None)

            img = qrcode.make(privkey, box_size=2)
            output = StringIO.StringIO()
            img.save(output, "PNG")
            output.seek(0)
            c.drawImage(ImageReader(output), left+3.1*cm, top-2.7*cm, 2.4*cm, 2.4*cm, None)

            addr_split = int(len(address)/2)
            addr_part1 = address[:addr_split]
            addr_part2 = address[addr_split:]
            print address, addr_part1, addr_part2

            c.drawCentredString(left+1.5*cm, top-0.45*cm, addr_part1)
            c.drawCentredString(left+1.5*cm, top-2.7*cm, addr_part2)

            privkey_split = int(len(privkey)/3)
            privkey_parts = (privkey[:privkey_split], privkey[privkey_split:privkey_split*2], 
                privkey[privkey_split*2:privkey_split*3])

            print privkey, privkey_parts

            c.drawCentredString(left+4.3*cm, top-0.2*cm, privkey_parts[0])
            c.drawCentredString(left+4.3*cm, top-0.45*cm, privkey_parts[1])
            c.drawCentredString(left+4.3*cm, top-2.7*cm, privkey_parts[2])

            c.saveState()
            c.rotate(90)
            c.setFont("UbuntuBI", 12)
            c.drawCentredString((top - 1.5*cm), -(left + 3.0*cm), unicode("bitcoin"))
            c.restoreState()
            c.setFont("UbuntuM", 6)
        c.showPage()
        c.setFont("UbuntuM", 6)
        c.drawString(0.5*cm, (29.7-0.7)*cm, "Series: "+banknote_series+" Page: "+str(page_num))
        for i in range(0, (3*9)):
            address = addresses[i]
            x = i % 3
            y = (i - (i % 3)) / 3
            top = (29.7 - 1 - 3*y)*cm
            left = (1+6.3*x)*cm

            print x, y, top, left

            img = qrcode.make(address, box_size=2)
            output = StringIO.StringIO()
            img.save(output, "PNG")
            output.seek(0)
            c.drawImage(ImageReader(output), left+0.3*cm, top-2.7*cm, 2.4*cm, 2.4*cm, None)

            addr_split = int(len(address)/2)
            addr_part1 = address[:addr_split]
            addr_part2 = address[addr_split:]
            print address, addr_part1, addr_part2

            c.drawCentredString(left+1.5*cm, top-0.45*cm, addr_part1)
            c.drawCentredString(left+1.5*cm, top-2.7*cm, addr_part2)

            c.saveState()
            c.rotate(90)
            c.setFont("UbuntuBI", 12)
            c.drawCentredString((top - 1.5*cm), -(left + 3.0*cm), unicode("bitcoin"))
            c.restoreState()
            c.setFont("UbuntuM", 6)

            for k in range(1, 6):
                c.line(left+3.3*cm, top-0.3*cm-0.45*k*cm, left+5.9*cm, top-0.3*cm-0.45*k*cm)

        c.showPage()
    c.save()
    # return response

def print_banknotes_pdf(num_pages = 1):
    banknote_series = base64.b64encode(os.urandom(8))
    c = canvas.Canvas("banknotes.pdf", pagesize=A4)
    for page_num in range(0, num_pages):
        c.setFont("UbuntuM", 6)
        c.drawString(0.5*cm, (29.7-0.7)*cm, "Series: "+banknote_series+" Page: "+str(page_num))
        for i in range(0, (2*9)):
            output = subprocess.Popen([options.vanitygen_path, options.vanitygen_start], stdout=subprocess.PIPE).communicate()[0]
            address = re.compile(u"(1[\w]{25,45})").search(output).group(1)
            privkey = re.compile(u"(5[\w]{45,75})").search(output).group(1)
            width, height = (16.8*cm, 9*cm)
            x = i % 2
            y = (i - (i % 2)) / 2
            top = (29.7 - 1 - 3*y)*cm
            left = (1+9.3*x)*cm

            print x, y, top, left

            c.line(left-0.5*cm, top, left+0.2*cm, top)
            c.line(left, top+0.5*cm, left, top-0.2*cm)
            c.line(left-0.5*cm+9.3*cm, top-3*cm, left+0.2*cm+9.3*cm, top-3*cm)
            c.line(left+9.3*cm, top+0.5*cm-3*cm, left+9.3*cm, top-0.2*cm-3*cm)

            c.line(left+3*cm, top-0.9*cm, left+3*cm, top-2.1*cm)
            c.line(left+6*cm, top-0.9*cm, left+6*cm, top-2.1*cm)
            
            # c.drawCentredString(((1+(20/3)*(i%3)))*cm, (29.7-2*((i-i%3)/3))*cm, address)
            # c.drawCentredString(((1+(20/3)*(i%3)))*cm, (29.7-1*((i-i%3)/3))*cm, privkey)

            img = qrcode.make(address, box_size=2)
            output = StringIO.StringIO()
            img.save(output, "PNG")
            output.seek(0)
            c.drawImage(ImageReader(output), left+0.3*cm, top-2.7*cm, 2.4*cm, 2.4*cm, None)

            img = qrcode.make(privkey, box_size=2)
            output = StringIO.StringIO()
            img.save(output, "PNG")
            output.seek(0)
            c.drawImage(ImageReader(output), left+6.3*cm, top-2.8*cm, 2.4*cm, 2.4*cm, None)

            addr_split = int(len(address)/2)
            addr_part1 = address[:addr_split]
            addr_part2 = address[addr_split:]
            print address, addr_part1, addr_part2

            c.drawCentredString(left+1.5*cm, top-0.45*cm, addr_part1)
            c.drawCentredString(left+1.5*cm, top-2.7*cm, addr_part2)

            privkey_split = int(len(privkey)/3)
            privkey_parts = (privkey[:privkey_split], privkey[privkey_split:privkey_split*2], 
                privkey[privkey_split*2:privkey_split*3])

            print privkey, privkey_parts

            c.drawCentredString(left+7.5*cm, top-0.3*cm, privkey_parts[0])
            c.drawCentredString(left+7.5*cm, top-0.55*cm, privkey_parts[1])
            c.drawCentredString(left+7.5*cm, top-2.8*cm, privkey_parts[2])

            c.setFont("UbuntuBI", 14)
            c.drawCentredString(left+4.5*cm, top-0.6*cm, unicode("bitcoin"))

            for k in range(2, 6):
                c.line(left+3.3*cm, top-0.3*cm-0.45*k*cm, left+5.7*cm, top-0.3*cm-0.45*k*cm)

            # c.saveState()
            # c.rotate(90)
            # c.setFont("UbuntuBI", 12)
            # c.drawCentredString((top - 1.5*cm), -(left + 3.0*cm), unicode("bitcoin"))
            # c.restoreState()
            c.setFont("UbuntuM", 6)
        c.showPage()
    c.save()
    # return response

if __name__ == '__main__':
    if options.bank_notes:
        print_banknotes_pdf(options.num_pages)
    else:
        print_notes_pdf(options.num_pages)
