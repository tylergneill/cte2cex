# Input Guidelines for using cte2cex

The below guidelines are expressed to the cte2cex script through the list of regular expression replacements in "regex_replacements.py", which can be modified as needed.

Three types of elements:

1. Logical "chapter" (passage) identifier
2. Physical "folio" (page and line) identifier
3. Text content

Rules:

1. With exception of header material (which must be removed through regex replacements), one chapter identifier and one folio identifier are required before any text content.
2. Whitespace counts as text content and so should not be used for visual padding between elements.
3. Chapter and folio identifiers must be formatted 100% consistently.