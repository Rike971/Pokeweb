import ndspy
import ndspy.rom
import ndspy.narc
import code 
import io
import codecs
import os
import json
import sys
import copy


def write_sprite_to_index(sprite_indexes, target_index):
	settings = {} ##store narc names and file id pairs

	with open(f'session_settings.json', "r") as outfile:  
		settings = json.load(outfile) 

	rom_name = settings["rom_name"]

	sprite_indexes = sprite_indexes.split(",")
	print(sprite_indexes)
	
	form_count = 0
	for sprite_index in sprite_indexes:
		is_shiny = False
		if sprite_index.split(" ")[0].lower() == "shiny":
			is_shiny = True

		sprite_index = int(sprite_index.split(" ")[-1]) 


		# sprites
		sprite_file_path = f'{rom_name}/narcs/sprites-{settings["sprites"]}.narc'
		narc = ndspy.narc.NARC.fromFile(sprite_file_path)
		
		to_copy = copy.deepcopy(narc.files[sprite_index * 20:(sprite_index + 1) * 20])

		if is_shiny:
			to_copy[18] = to_copy[19]

		narc.files[13700 + (20 * target_index): 13720 + (20 * target_index)] = to_copy

		print(f'{sprite_index * 20} {(sprite_index + 1) * 20}')
		print(f'{13700 + (20 * target_index)}: {13720 + (20 * target_index)}')

		with open(f'{rom_name}/narcs/sprites-{settings["sprites"]}.narc', 'wb') as f:
			f.write(narc.save())

		#icons
		sprite_file_path = f'{rom_name}/narcs/icons-{settings["icons"]}.narc'
		narc = ndspy.narc.NARC.fromFile(sprite_file_path)
		
		icon_offset = 8

		to_copy = narc.files[sprite_index * 2 + icon_offset:(sprite_index + 1) * 2 + icon_offset]
		narc.files[1378 + (2 * target_index): 1380 + (2 * target_index)] = to_copy

		with open(f'{rom_name}/narcs/icons-{settings["icons"]}.narc', 'wb') as f:
			f.write(narc.save())

		target_index += 1





