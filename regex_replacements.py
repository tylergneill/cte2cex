#!/usr/bin/env python
# -*- coding: utf-8 -*-

regex_replacements = [

	# 0: eliminate unused material; light standardization
	[
		(r'\xef\xbb\xbf',''),	# BOM
		(r'\r\n', '\n'),	# Windows- > Linux-style line break

		(r'CTE_[\s\S]*?{Text\\', ''),	# CTE header
		(r'\\Text}[\s\S]*', ''),	# CTE footer

		(r'(({F[^\\]*?\\)|(\\F}))', ''),	# CTE text formatting markup
		(r'{P\\[^\\]*?\\P}', ''),	# CTE paragraph formatting markup
		(r'{C(N1)?\\([^\\]*?)\\C}', '{\\2}'), 	# CTE passage ("chapter") identifier markup
		(r'{E6[^\\]*?\\([^\\]*?)\\E}', '\\1'), 	# CTE hyperlink markup (e.g. Dropbox links)
		(r'{S\\[^\\]*?\\S}', ''),	# CTE special line break

		(r'^Transcript.*', ''),	# human-readable header note
		(r'^Critical.*', ''),	# human-readable header note
		(r'^\^\[Sources.*', ''),	# human-readable header note
		(r'^[^\n]*?missing.*\n', ''),	# human-readable note mid-transcript
		(r'\^\[[pnv](?!(\^\]))[\s\S]*?\^\]', ''), # human-readable note mid-transcript

		(r'\^\"', '^'),	# escaped half-punctuation mark ^
		(r'\^\+', '-'),	# escaped hyphen
		(r'–', '_'),	# n-dash

		(r'\t', ''),	# tab
		(r'\n{2,}', '\n'),	# multiple line breaks
		(r'\A\s*', ''),	# file-initial whitespace

		(r'\A(\(%s_\d+[^\)]*?\))([^{]{0,250})({([^}]*?)})', '\\3\\1\\2'),
		(r'(\(%s_\d+[^\)]*?\))({([^}]*?)})', '\\2\\1'), # object (folio) identifer templates

		(r'\n{2,}', '\n'),	# multiple line breaks
		(r'\s*\Z', ''),	# file-final whitespace
		(r'^ *', ''),	# line-initial space
	],

	# 1: simplify to three element types for CEX !relations block
	[
		(r'(\(?{[^}]*?}\)?)', '\n\\1\n'),	# passage identifiers
		(r'(\(%s_\d+[^\)]*?[rv]?)(,?\d+?\))', '\n\\1)\n'),	# object identifiers
		(r'^\s*', ''),	# line-initial whitespace
		(r'^(?!(\(%s_\d+[^\)]*?\))|({[^}]*?})).+', '...'),	# specific content details
		(r'(\n\.\.\.){2,}', '\\1'),	# consecutive lines of content
		(r'([rv])\d+\)', '\\1)'),	# object (folio) identifer line numbers
		
	],

	# 2: format textual content for CEX !ctsdata block
	[
		(r'\n', '-NEWLINE-'),	# encoding of newline
		(r'(-NEWLINE-)?{([^}]*?)}', '\n\\2\t'),	# two columns: passage identifier, rest
		(r'\((%s_\d+[^\)]*?)\)', '{\\1}'),	# encoding of in-line object identifer
		(r'^\s*', ''),	# line-initial whitespace
	],

]