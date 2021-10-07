# !usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import json
import subprocess
import webbrowser
import datetime
import time
from tqdm import tqdm
# import validation2
# from validate_structure import validate_structure
# from validate_content import validate_content

# command-line flags
for arg in sys.argv:
	if ".json" in arg: 				# mandatory project config file
		config_fn = arg
		break
else:
	print("no project config file")
	exit()
do_validation = "-v" in sys.argv	# validation flag -v
# force_proceed = "-f" in sys.argv
do_full_update = "-u" in sys.argv	# full update flag -u
# full_update = "--full_update" in sys.argv

# load config variables
config_data = open(config_fn,'r').read()
config = json.loads(config_data)
Br_path = config["Brucheion_cex_folder_abs_path"]
cex_fn = config["cex_output_fn"]
port_num = config["port_num"]
input_path = config["input_folder_abs_path"]
output_path = config["output_folder_abs_path"]
all_fns = config["input_files_individual_abs_paths"]
cex_catalog_info = config["cex_catalog_info"]
siglum_to_sliced_img_fn_abbrv = config["siglum_to_sliced_img_fn_abbrv"]
destroy_zero_space_word_separator = config["destroy_zero_space_word_separator"]
browser_choice = config["browser_choice"]
do_renormalize = config["renormalize"]
do_git_push = config["git_push_changes"]	# requires preexisting local Git repository

# import regex_replacements from separate .py file
package = config["regex_replacements_fn"]
if package[-3:] == ".py": package = package[:-3] # confirm .py, remove extension
else: print("regex_replacements_fn not '.py'"); exit()
attribute = "regex_replacements" # list attribute to import from package, name fixed here
regex_replacements = getattr(__import__(package, fromlist=[attribute]), attribute)

# prepare some helpful regex strings
sigla_regex = '(?:(?:' + ')|(?:'.join([str(x) for x in config["siglum_to_sliced_img_fn_abbrv"].keys()]) + '))' # e.g. "(C3D|D1E|J1D|M2D|...)"

# file management functions for full update
def clear_input_folder(): subprocess.call("rm %s/*.*" % input_path, shell='True')
def populate_input_folder():
	for fn in all_fns: subprocess.call('cp %s %s' % (fn, input_path), shell='True')
def replace_cex():
	subprocess.call("mv %s/%s %s/%s_bkup.cex" % (Br_path, cex_fn, Br_path, cex_fn[:cex_fn.find(".")]), shell='True')
	subprocess.call("mv %s/%s %s" % (output_path, cex_fn, Br_path), shell='True')
def reload_cex():
	api_load_call = "http://localhost:%s/load/%s" % (port_num, cex_fn[:cex_fn.find(".")])
	webbrowser.get(browser_choice).open_new_tab(api_load_call)
def renormalize():
	api_normalize_call = "http://localhost:7000/normalizeAndSave/all/"
	webbrowser.get(browser_choice).open_new_tab(api_normalize_call)
def push_changes():
	current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	subprocess.call("git -C %s add %s" % (Br_path, cex_fn), shell='True')
	subprocess.call('git -C %s commit -m "updated %s"' % (Br_path, current_time), shell='True')
	subprocess.call("git -C %s push -u origin master" % Br_path, shell='True')

extract_folio_num_and_side_regex = '%s_(\d+[_\d]*?[ab]?[rv,])' % sigla_regex # e.g. "101r" of "101r1", "3_08v" of "3_08v2", "103," of "103,4"
extract_line_num_regex = '%s_\d+[_\d]*?[ab]?[rv,](\d+)' % sigla_regex # e.g. "1", "2", "3" above

# function for enriching incoming data so as to enable display of line numbers in Brucheion View mode
def folio_breaks_for_all_passages(file_data):

#  	import pdb;pdb.set_trace()
	line_counter = 0
	improved_file_data = []
	current_siglum = current_folio_num_and_side = ''
	for line in file_data:
		result = re.findall(sigla_regex, line)
		if result != []:					# if folio boundary found, switch to using it
			current_siglum = result[0]
			try:
				current_folio_num_and_side = re.findall(extract_folio_num_and_side_regex, line)[0]
				line_counter = int(re.findall(extract_line_num_regex, line)[0])
			except IndexError: exit()
		else: line_counter += 1 			# otherwise, just do the next line on the same folio
		line = re.sub('({[^}]*?})(?!(\(%s[^\)]+?\)))(.)' % current_siglum, '\\1(%s_%s%d)\\3' % (current_siglum, current_folio_num_and_side, line_counter), line) # insert new material as applicable
		improved_file_data.append(line)
	return improved_file_data


# BEGIN CONVERSION

if do_full_update:
	clear_input_folder()
	populate_input_folder()

# (filenames should already be consistently symmetrical and alphabetical)
fns_to_skip = ['.DS_Store', '.gitkeep']
input_fns = [os.path.join(input_path,fn) for fn in os.listdir(input_path) if fn not in fns_to_skip]
input_fns.sort()

# import pdb;pdb.set_trace()


# READ IN

print("reading in files...")

ctsdata_buffer = ''

for fn in tqdm(input_fns):
	file_data = open(fn, 'r').read()

	# cleaning round 1 (regex_replacements[0]): eliminate unused material; light standardization
	for pattern, replacement in regex_replacements[0]:
		if "_\d+" in pattern: # _\d+ is indicative of a regex that needs further sigla detail
			pattern = pattern % sigla_regex
		file_data = re.sub(pattern, replacement, file_data, flags=re.MULTILINE)

	if do_validation:
		pass
# 		print "validating structure of", fn
# 		validation2.validate_structure(file_data)
# 		print "validating content of", fn
# 		validation2.validate_content(file_data)

	# add additional folio markers and line numbers
	file_data = '\n'.join(folio_breaks_for_all_passages(file_data.split('\n')))

	ctsdata_buffer = ctsdata_buffer + (file_data + '\n')

ctsdata_buffer = ctsdata_buffer[:-1] # exclude final newline

# duplicate buffer for seperate processing of two cex data blocks: relations and ctsdata
relations_buffer = ctsdata_buffer


# RELATIONS

# import pdb;pdb.set_trace()

# cleaning round 2 (regex_replacements[1]): simplify to three element types for Brucheion relations
for pattern, replacement in regex_replacements[1]:
	if "_\d+" in pattern: pattern = pattern % sigla_regex
	relations_buffer = re.sub(pattern, replacement, relations_buffer, flags=re.MULTILINE)
identifiers_and_content = relations_buffer.split('\n')

relations_buffer = ''  # reset for reuse
prev_textual_identifier = identifiers_and_content[0]
prev_object_identifier = identifiers_and_content[1]

for curr_identifier_or_content in identifiers_and_content[2:]:


# 	import pdb;pdb.set_trace()

	try:

		if curr_identifier_or_content == '...':
			relations_buffer = relations_buffer + (prev_textual_identifier + '\t' + prev_object_identifier + '\n')

		elif curr_identifier_or_content[0]=='{':
			prev_textual_identifier = curr_identifier_or_content

		elif curr_identifier_or_content[0]=='(':
			prev_object_identifier = curr_identifier_or_content
# 			prev_object_identifier = re.findall("(.*?)[rv,]\d+\)", curr_identifier_or_content)[0] + ')'
# 			import pdb;pdb.set_trace()

	except IndexError:
		print("curr_identifier_or_content: ", curr_identifier_or_content)
		import pdb;pdb.set_trace()


relations_buffer = relations_buffer[:-1] # exclude final newline
relations_buffer = re.sub(r'[{}\(\)]', '', relations_buffer, flags=re.MULTILINE)

print("processing relations...")

# import pdb;pdb.set_trace()


relations_buffer_cex = '#!relations' + '\n'
for relation in tqdm(relations_buffer.split('\n')):

	textual_identifier, object_identifier = relation.split('\t')
	object_id_prefix = object_identifier[:object_identifier.find('_')]
	object_id_suffix = object_identifier[object_identifier.find('_'):]

	formatted_relation = ''.join([
		config["base_protocol_namespace_workPrefix"],
		object_id_prefix,
		":",
		textual_identifier,
		"#",
		config["relations_verb"],
		"#",
		config["base_protocol_imageArchiveName"],
		siglum_to_sliced_img_fn_abbrv[object_id_prefix],
		'img.positive:',
		siglum_to_sliced_img_fn_abbrv[object_id_prefix],
		object_id_suffix,
	])

	if object_id_prefix in config["witnesses_with_negatives"]:
		formatted_relation = formatted_relation + '\n' + formatted_relation.replace('positive','negative')

	relations_buffer_cex = relations_buffer_cex + formatted_relation + '\n'

relations_buffer_cex = relations_buffer_cex[:-1] # exclude final newline
relations_buffer_cex = relations_buffer_cex


# CTSDATA

# cleaning round 3 (regex_replacements[2]): format textual content for Brucheion ctsdata
for pattern, replacement in regex_replacements[2]:
	if "_\d+" in pattern: pattern = pattern % sigla_regex
	ctsdata_buffer = re.sub(pattern, replacement, ctsdata_buffer, flags=re.MULTILINE)

print("processing ctsdata...")

ctsdata_buffer_cex = '#!ctsdata' + '\n'
curr_witness = ''
for node in tqdm(ctsdata_buffer.split('\n')):

	try: textual_identifier, content = node.split('\t')
	except: import pdb; pdb.set_trace()

	witness_for_this_node = re.search(sigla_regex, content[:20])
	if witness_for_this_node != None and witness_for_this_node.group() != curr_witness:
		curr_witness = witness_for_this_node.group()

	formatted_node = ''.join([
		str(config["base_protocol_namespace_workPrefix"]),
		curr_witness,
		':',
		textual_identifier,
		'#',
		content,
	])

	ctsdata_buffer_cex = ctsdata_buffer_cex + formatted_node + '\n'
ctsdata_buffer_cex = ctsdata_buffer_cex[:-1] # exclude final newline

if destroy_zero_space_word_separator:
	ctsdata_buffer_cex = ctsdata_buffer_cex.replace('\x1d','')


# CATALOG

ctscatalog_buffer = """#!ctscatalog
urn#citationScheme#groupName#workTitle#versionLabel#exemplarLabel#online#lang
"""

ctscatalog_buffer = ctscatalog_buffer + '\n'.join(x for x in config["cex_catalog_info"])

# combine content
cex_total_content = ('\n'*2).join([
	ctscatalog_buffer,
	ctsdata_buffer_cex,
	relations_buffer_cex,
])


# FINISH

# save results
ctsdata_output_fn = os.path.join(output_path, cex_fn)
ctsdata_output_f = open(ctsdata_output_fn, 'w')
ctsdata_output_f.write(cex_total_content)
ctsdata_output_f.close()

if do_full_update:
	replace_cex()
	time.sleep(2)
	reload_cex()
	if do_renormalize:
		time.sleep(2)
		renormalize()
		time.sleep(10)
	if do_git_push:
		time.sleep(2)
		push_changes()
		time.sleep(10)
