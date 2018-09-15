from lxml import html
import requests
from unidecode import unidecode
from pylatex import Document, Section, Subsection, Command, NewPage, LargeText, MediumText, NewLine, Package
from pylatex.utils import NoEscape, bold, verbatim
from pylatex import FlushLeft
import time

# If getting errors with SSL Certificate Verification, may have to update OpenSSL.
# To fix, run the following from the command line:
# pip install --upgrade pyopenssl
# easy_install ndg-httpsclient
# easy_install cheetah


def addMainText(doc,tree):
	# Text content is loaded in an iFrame so we have to make a separate request for that
	url2 = tree.cssselect("iframe")[0].attrib['src'] # first iframe
	url2 = url2[0:4] + url2[5:]

	url2 = tree.xpath('//div[@class="entry-content"]/p/a')
	url2 = url2[0].attrib['href']

	# print url2

	page2 = requests.get(url2)
	tree2 = html.fromstring(page2.content)

	# Prepending \n's to preserve <br> tags in text.
	for br in tree2.xpath('*//br'):
		br.tail = '\n' + br.tail if br.tail else '\n'

	# Doing this node by node because of some footnote considerations
	pnodes = tree2.xpath('//p')

	for pnode in pnodes[1:]:
		nodes = pnode.cssselect('a,span')
		if not nodes[0].text_content():
			continue

		txt = ''
		# for a in alinks:
		# 	txt += a.text_content()
		for n in nodes:
			txt += n.text_content()

		txt2 = unidecode(txt)
		left = FlushLeft()
		left.append(txt2)
		# left.append(NewLine())
		doc.append(left)

	# text = trath('//p/span/text()')

	# # if not text: # empty list, use different filter
	# # 	text = tree2.xpath('//p[@class="c2"]/span/text()')

	# for txt in text[1:]:
	# 	if not txt:
	# 		continue

	# 	# for txt in text[2:]:
	# 	txt2 = unidecode(txt)
	# 	left = FlushLeft()
	# 	left.append(txt2)
	# 	# left.append(NewLine())
	# 	doc.append(left)ee2.xp

# Scrapes one book of DE, from chapter 1 to chapterMax
def douluodalu(chStart, chEnd):
	novelTitle = "Douluo Dalu"
	author = "Tang Jia San Shao"
	baseURL = "http://bluesilvertranslations.wordpress.com/douluo-dalu-%d"

	doc = Document(documentclass='scrartcl',document_options='titlepage')
	doc.packages.append(Package('ragged2e'))
	doc.packages.append(Package('geometry',options='margin=1in'))
	# doc = Document(document_options='titlepage')

	for c in range (chStart, chEnd+1):
		url = baseURL % (c)
		print 'Parsing', url

		page = requests.get(url)
		tree = html.fromstring(page.content)

		title = tree.xpath('//h1[@class="entry-title"]/text()')
		for tit in title:
			title2 = unidecode(tit)
			Chapter = title2.split(' - ')
			Chapter = Chapter[2]

		if c == chStart: # On first chapter, create title page
			# doc.preamble.append(Command('title',LargeText(bold(Book)) + NewLine() + MediumText('Book %d: %s' % (B, Book))))
			# doc.preamble.append(Command('title',Book + NoEscape('\\') + '\\large Book %d: %s' % (B, Book)))
			doc.preamble.append(Command('title',novelTitle))
			doc.preamble.append(Command('subtitle','Chapter %d - %d' % (chStart, chEnd)))
			doc.preamble.append(Command('author', author))
			doc.preamble.append(Command('date', ''))
			doc.append(NoEscape(r'\maketitle'))
		else:
			doc.append(NewPage())

		with doc.create(Section('Chapter %d: %s' % (c,Chapter), numbering=False)):
			addMainText(doc, tree)

		time.sleep(5)

	try:
		doc.generate_pdf('%s - Chapter %d - %d' % (novelTitle,chStart,chEnd), clean_tex=False, compiler='pdflatex')
	except:
		val = raw_input('Failed to generate PDF...try again? (y/n): ')
		if val == 'y':
			doc.generate_pdf('%s - Chapter %d - %d' % (novelTitle,chStart,chEnd), clean_tex=False, compiler='pdflatex')



if __name__ == '__main__':
	douluodalu(285,311)
	# douluodalu(306,306)
	# douluodalu(306,311)
	# douluodalu(285,285)
