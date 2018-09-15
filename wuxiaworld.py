from lxml import html
import requests
from unidecode import unidecode
from pylatex import Document, Section, Subsection, Command, NewPage, LargeText, MediumText, NewLine, Package
from pylatex.utils import NoEscape, bold, verbatim
from pylatex import FlushLeft
import time


def addMainText(doc,tree):
	text = tree.xpath('//div[@itemprop="articleBody"]/p/text()')

	for txt in text:
		txt2 = unidecode(txt)
		left = FlushLeft()
		left.append(txt2)
		# left.append(NewLine())
		doc.append(left)


def addMainTextV2(doc,tree):
	# Prepending \n's to preserve <br> tags in text.
	for br in tree.xpath('*//br'):
		br.tail = '\n' + br.tail if br.tail else '\n'

	pnodes = tree.xpath('//div[@itemprop="articleBody"]/p')

	for pnode in pnodes[1:]:
		nodes = pnode.cssselect('a,p')
		if not nodes[0].text_content():
			continue

		if nodes[0].text_content()[0:4] == 'Book':
			continue
		elif nodes[0].text_content()[0:7] == 'Chapter':
			continue
		elif nodes[0].text_content()[0:16] == 'Previous Chapter':
			continue

		txt = nodes[0].text_content()

		for n in nodes:
			if n.tag == 'a':
				txt = txt.replace(n.text_content(),'[' + n.text_content() + ']')

		txt2 = unidecode(txt)
		left = FlushLeft()
		left.append(txt2)
		# left.append(NewLine())
		doc.append(left)

	
	pnodes = tree.xpath('//div[@class="footnotes"]/ol/li')

	if len(pnodes) > 0:
		doc.append('--------')

	# print len(pnodes)
	for (i,pnode) in enumerate(pnodes):
		txt = '[' + str(i+1) + '] '
		txt += pnode.text_content()[0:-1]

		txt2 = unidecode(txt)
		left = FlushLeft()
		left.append(txt2)
		# left.append(NewLine())
		doc.append(left)

# Scrapes one book of DE, from chapter 1 to chapterMax
def desolateEra(bookMax, chapterMax):
	novelTitle = "Desolate Era"
	author = "I Eat Tomatoes"
	baseURL = "http://www.wuxiaworld.com/desolate-era-index/de-book-%d-chapter-%d"

	B = bookMax
	C = chapterMax
	# C = 23

	doc = Document(documentclass='scrartcl',document_options='titlepage')
	doc.packages.append(Package('ragged2e'))
	doc.packages.append(Package('geometry',options='margin=1in'))
	# doc = Document(document_options='titlepage')

	for c in range (1, C+1):
		url = baseURL % (B, c)
		print 'Parsing', url

		page = requests.get(url)
		tree = html.fromstring(page.content)

		title = tree.xpath('//div[@itemprop="articleBody"]/p/span/strong/text()')
		for tit in title:
			title2 = unidecode(tit)
			Book = title2.split(', ')
			Book = Book[1]
			Chapter = title2.split(' - ')
			Chapter = Chapter[1]

		if c == 1: # On first chapter, create title page
			# doc.preamble.append(Command('title',LargeText(bold(Book)) + NewLine() + MediumText('Book %d: %s' % (B, Book))))
			# doc.preamble.append(Command('title',Book + NoEscape('\\') + '\\large Book %d: %s' % (B, Book)))
			doc.preamble.append(Command('title',novelTitle))
			doc.preamble.append(Command('subtitle','Book %d: %s' % (B, Book)))
			doc.preamble.append(Command('author', author))
			doc.preamble.append(Command('date', ''))
			doc.append(NoEscape(r'\maketitle'))
		else:
			doc.append(NewPage())

		with doc.create(Section('Chapter %d: %s' % (c,Chapter), numbering=False)):
			addMainTextV2(doc, tree)

		time.sleep(5)

	try:
		doc.generate_pdf('%s - Book %d - %s' % (novelTitle,B,Book), clean_tex=False, compiler='pdflatex')
	except:
		val = raw_input('Failed to generate PDF...try again? (y/n): ')
		if val == 'y':
			doc.generate_pdf('%s - Book %d - %s' % (novelTitle,B,Book), clean_tex=False, compiler='pdflatex')


# Scrapes one book of ISSTH, from chapter 1 to chapterMax
def issth(bookNumber, chapterStart, chapterMax, bookTitle):
	novelTitle = "I Shall Seal The Heavens"
	author = "Er Gen"
	baseURL = "http://www.wuxiaworld.com/issth-index/issth-book-%d-chapter-%d"

	B = bookNumber
	C = chapterMax
	# C = 23

	doc = Document(documentclass='scrartcl',document_options='titlepage')
	doc.packages.append(Package('ragged2e'))
	doc.packages.append(Package('geometry',options='margin=1in'))
	# doc = Document(document_options='titlepage')

	for c in range (chapterStart, C+1):
		url = baseURL % (B, c)
		print 'Parsing', url

		page = requests.get(url)
		tree = html.fromstring(page.content)

		title = tree.xpath('//div[@itemprop="articleBody"]/p/strong')
		if not title:
			title = tree.xpath('//div[@itemprop="articleBody"]/strong')
		if not title:
			continue
		Chapter = unidecode(title[0].text_content())
		Book = bookTitle
		# for tit in title:
			
			# Chapter = title2.split(' - ')
			# Chapter = Chapter[1]

		if c == chapterStart: # On first chapter, create title page
			# doc.preamble.append(Command('title',LargeText(bold(Book)) + NewLine() + MediumText('Book %d: %s' % (B, Book))))
			# doc.preamble.append(Command('title',Book + NoEscape('\\') + '\\large Book %d: %s' % (B, Book)))
			doc.preamble.append(Command('title',novelTitle))
			doc.preamble.append(Command('subtitle','Book %d: %s' % (B, Book)))
			doc.preamble.append(Command('author', author))
			doc.preamble.append(Command('date', ''))
			doc.append(NoEscape(r'\maketitle'))
		else:
			doc.append(NewPage())

		with doc.create(Section(Chapter, numbering=False)):
			addMainTextV2(doc, tree)

		time.sleep(5)

	try:
		doc.generate_pdf('%s - Book %d - %s' % (novelTitle,B,Book), clean_tex=False, compiler='pdflatex')
	except:
		val = raw_input('Failed to generate PDF...try again? (y/n): ')
		if val == 'y':
			doc.generate_pdf('%s - Book %d - %s' % (novelTitle,B,Book), clean_tex=False, compiler='pdflatex')



if __name__ == '__main__':
	# desolateEra(34,1)
	
 	# desolateEra(33,23)
 	# desolateEra(36,30)
 	desolateEra(37,31)

	# issth(4,582,583,'Patriarch Reliance')

 	# issth(1,1,95,'Patriarch Reliance')
 	# issth(2,96,204,'Cutting Into the Southern Domain')
 	# issth(3,205,313,'The Honor of Violet Fate')
 	# issth(4,314,628,'Five Color Paragon!')
 	# issth(5,629,800,'Nirvanic Rebirth. Blood Everywhere!')
 	# issth(6,801,1004,'Fame that Rocks the Ninth Mountain; the Path to True Immortality')
 	# issth(7,1005,1211,'Immortal Ancient Builds a Bridge Leaving the Ninth Mountain!')
 	# issth(8,1212,1409,'My Mountain and Sea Realm')
 	# issth(9,1410,1557,'The Demon Sovereign Returns; the Peak of the Vast Expanse!')
 	# issth(10,1558,1614,'I Watch Blue Seas Become Lush Fields')
