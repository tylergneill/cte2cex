# cte2cex

A tool for converting multiple Classical Text Editor (CTE) files (transcripts, editions) to a CEX library file for use in Brucheion.

Requirements:

Python 2.7 + libraries: re, json, subprocess, webbrowser, tqdm

Instructions:

1. Review "input\_guidelines.md"; optionally test compliance of individual input files ahead of time with "validate.py".

2. For one-time test use: 

* Manually place desired CTE files in folder "input\_cte\_files".
* Run cte2cex.py; optionally supply '-v' flag for run-time input validation.
* Collect output CEX from "output\_cex\_files".

3. For recurring project use:

* Create project JSON file: Supply static paths to individual CTE files and corresponding CEX catalog entries. Also supply desired filename and destination path for CEX output (e.g., .../Brucheion/cex). For new projects, update CTS protocol components as needed (see [Homer Multitext](https://www.homermultitext.org/hmt-doc/cite/texts/ctsoverview.html) and [cite-architecture.org](http://cite-architecture.org/cts/)). Choose options for handling of zero-space word separator, additional negative images, and so on.
* Run Brucheion and log in with desired "username".
(Note: usernames utilized here for projects, not people.)
* Run cte2cex.py with '-bp' flag to update Brucheion project.
(Note: contents of folder "input\_cte\_files" will be purged! Also, any preexisting CEX with same filename in destination path will be renamed with "_bkup".)
* Wait briefly until processing completes and Brucheion confirms in-browser successful execution of "load" API call. (Note: All conflicting Brucheion data in current "user" database will be overwritten. Orthography normalization will need to be re-run.)