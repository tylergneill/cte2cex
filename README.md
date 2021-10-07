# cte2cex

A tool for converting multiple Classical Text Editor (CTE) and/or plain-text files (transcripts, editions) to a CEX library file for use in [a visualization-only fork of Brucheion VRE](https://github.com/tylergneill/Brucheion_tgn/tree/exp).

Requirements:

Python 2.7 + libraries `re`, `json`, `subprocess`, `webbrowser`, `tqdm`

Instructions:

1. Make sure input data is properly formatted.

* For this, review `input_guidelines.md`. 
* Optionally test compliance of individual input files for compatibility with `regex_replacements.py` and project config file ahead of time with `validation.py`.

2. Create project JSON file.

* Choose project name for output filename.
* Supply static paths for individual input (e.g. CTE) files as well as output path (e.g., `Brucheion\cex`).
* Prepare static CEX catalog entries.
* Update CTS protocol components as needed (see [Homer Multitext](https://www.homermultitext.org/hmt-doc/cite/texts/ctsoverview.html) and [cite-architecture.org](http://cite-architecture.org/cts/) for background on CITE architecture).
* Choose options for handling of zero-space word separator, additional negative images, orthography normalization, and so on.

3. For recurring project use:

* Start Brucheion and log in to desired project (formerly "username").
* Run `cte2cex.py`, specifying project json file and `-u` flag as arguments; optionally supply `-v` flag for run-time input validation.
> Note: With `-u` flag, contents of folder `tmp\input_cte_files` will be purged! Also, any preexisting CEX with same filename in output path will be renamed with "_bkup". Most importantly, all conflicting Brucheion data in the current "user" database will be overwritten.
* Observe progress in command line window, wait for confirmation of success in loading (and re-normalization, if applicable) in a new tab in the browser.

4. For one-time test use:

* Manually place desired input files in input folder.
* Run `cte2cex.py` *without* the `-u` flag; optionally supply `-v` flag for run-time input validation.
* Collect output CEX from `tmp\output_cex_files`.
> Note: Nothing more will be automatically done with the resulting output file.