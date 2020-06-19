# Input Guidelines for using cte2cex

The below guidelines are expressed to the cte2cex script through the list of regular expression replacements in "regex_replacements.py", which can be modified as needed.

Three types of elements:

1. Logical "chapter" (passage) identifier
2. Physical "folio" (page and line) identifier
3. Text content

Rules:

1. With exception of human-readable header material at the beginning of the transcript file (which the regex replacements can help remove), one chapter identifier and one folio identifier are required before any text content.
2. Whitespace counts as text content and so should not be used for visual padding between elements.
3. Chapter and especially folio identifiers must be formatted 100% consistently. For example, in the default setup provided, folio identifiers are marked with parentheses, use underscore, and always include a line number, like "(C3D\_089v9)" or "(M3D\_100,4)", whereas chapter identifiers have curly brackets, like "{4.1.1}" or (in CTE) "{C\3.2.40\C}".

Example Text:

~~~~
(C3D_089v9){4.1.1}manaso nantaraṃ pravṛttiḥ parīkṣitavyā tatra khalu yāvad dharmādharmāśrayaśarīrādi parīkṣitam sarvāsāṃ pravṛtteḥ parīkṣā i
(C3D_090r1)ty āha pravṛttir yathoktā tathā parīkṣiteti {4.1.2}pravṛtyanantarās tarhi doṣāḥ parīkṣyantām ity ata āha tathā doṣāḥ parīkṣitā iti buddhisamānā
~~~~