from lxml import html
import requests
from unidecode import unidecode
from pylatex import Document, Section, Subsection, Command, NewPage, LargeText, MediumText, NewLine, Package
from pylatex.utils import NoEscape, bold, verbatim
from pylatex import FlushLeft
import time


def addMainText(doc,tree):
	text = tree.xpath('//div[@id="chapterContent"]/p/span/span/text()')

	for txt in text[2:]:
		txt2 = unidecode(txt)
		left = FlushLeft()
		left.append(txt2)
		# left.append(NewLine())
		doc.append(left)

# Scrapes one book of DE, from chapter 1 to chapterMax
def zetianji(chStart, chEnd):
	novelTitle = "Ze Tian Ji (Way of Choices)"
	author = "Mao Ni"
	baseURL = "http://gravitytales.com/novel/way-of-choices/ztj-chapter-%d"

	doc = Document(documentclass='scrartcl',document_options='titlepage')
	doc.packages.append(Package('ragged2e'))
	doc.packages.append(Package('geometry',options='margin=0.5in'))
	# doc = Document(document_options='titlepage')

	for c in range (chStart, chEnd+1):
		url = baseURL % (c)
		print 'Parsing', url

		page = requests.get(url)
		tree = html.fromstring(page.content)

		title = tree.xpath('//div[@id="chapterContent"]/h1/span/span/text()')
		for tit in title:
			title2 = unidecode(tit)
			Chapter = title2.split(' - ')
			Chapter = Chapter[1]

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
	# desolateEra(34,1)
	zetianji(445,680)
 	# desolateEra(33,23)
