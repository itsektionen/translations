import json
from datetime import datetime

with open('en.json', 'r', encoding='utf-8') as f:
	en_data = json.load(f)
with open('sv.json', 'r', encoding='utf-8') as f:
	sv_data = json.load(f)

md = "# Student Translations (Swedish - English)\n\n"
md += """Translations of common student and IT-Chapter specific terms between
Swedish and English, including acronyms or shorter versions of some terms.
The words below are generated from more extensive lists containing multiple word
forms/tenses, and are presented in the indefinite singular form where applicable.

"""
md += f"**Last update**: {datetime.today().strftime('%Y-%m-%d')}\n\n"

def format_entries(data):
	if not isinstance(data, dict):
		return []

	if 'formal' in data and 'informal' in data:
		formal_entry = data['formal']
		formal = formal_entry.get('singular') or formal_entry.get('full')
		formal_short = formal_entry.get('short')

		informal_entry = data['informal']
		informal = informal_entry.get('singular') or informal_entry.get('full')
		informal_short = informal_entry.get('short')
		
		return [
			(formal, formal_short, "Formal"),
			(informal, informal_short, "Informal")
		]
	
	entry = data.get('singular') or data.get('full')
	short = data.get('short')
	return [(entry, short, None)]

def get_entries(en_items, sv_items):
	entries = []
	for key in en_items:
		if key not in sv_items:
			print(f"WARNING: English key '{key}' is not translated in Swedish.")
			continue

		sv_entries = format_entries(sv_items[key])
		en_entries = format_entries(en_items[key])

		if not sv_entries or not en_entries:
			print(f"WARNING: Translation entries missing or invalid for key '{key}'")
			continue

		for (sv, sv_short, sv_label), (en, en_short, _) in zip(sv_entries, en_entries):
			if not sv or not en:
				continue

			sv = sv + (f" ({sv_short})" if sv_short else "")
			en = en + (f" ({en_short})" if en_short else "")

			if sv_label:
				sv += f" [{sv_label}]"
			
			entries.append((sv, f"- {sv} = {en}\n"))

	return [line for _, line in sorted(entries, key=lambda x: x[0])]

for group in en_data.keys():
	if group not in sv_data:
		print(f"WARNING: Group '{group}' exists in English but not in Swedish. Skipping.")
		continue

	md += f"## {group.capitalize()}\n\n"
	
	en_items = en_data[group]
	sv_items = sv_data[group]

	if not isinstance(en_items, dict) or not isinstance(sv_items, dict):
		continue
	
	for line in get_entries(en_items, sv_items):
		md += line
	
	md += "\n"

with open('translations.md', 'w', encoding='utf-8') as f:
	f.write(md)
