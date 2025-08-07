#! /usr/bin/python3
import argparse, os
script_dir = os.path.dirname(os.path.abspath(__file__))
buffer_size = 1024

def normalize_shift(shift, alphabet):
	while shift >= len(alphabet):
		shift -= len(alphabet)
	return shift

def strloop(target):
	while True:
		for char in target:
			yield char

def main():
	parser = argparse.ArgumentParser(
		prog = "E-Vigenere",
		description = "Vigenere encryption. Nothing really special.")
	parser.add_argument("password")
	parser.add_argument("input_file", type = argparse.FileType("r"))
	parser.add_argument("output_file", type = argparse.FileType("w"))
	parser.add_argument("-l", "--language")

	args = parser.parse_args()
	if args.language == None:
		args.language = "english"
		print(f"No language specified. Default selected: {args.language}")
	args.language = args.language.lower()
	alphabet_path = os.path.dirname(script_dir)+"/alphabets/"+args.language
	if not os.path.exists(alphabet_path):
		print("No such alphabet '{args.language}'. At path {alphabet_path}")
		return
	with open(alphabet_path) as f:
		alphabet = f.read().replace("\n", "")
	print(f"Loaded alphabet: {alphabet}")
	password = "".join([char.lower() if char.lower() in alphabet else "" for char in args.password])
	if len(password)!=len(args.password):
		if len(password)>0:
			print("Password contains characters that are not in alphabet. Theese will be removed.\nNew password: "+password)
		else:
			print("Password is made out entierly out of invalid characters. Can not continue")
			return
	input_chunk = True
	password_iterator = strloop(password)
	while input_chunk:
		input_chunk = args.input_file.read(buffer_size)
		output_chunk = []
		for input_character in input_chunk:
			if input_character.lower() not in alphabet:
				output_chunk.append(input_character)
				continue
			character = alphabet[normalize_shift(alphabet.index(input_character.lower())+alphabet.index(next(password_iterator)), alphabet)]
			if input_character.isupper():
				character = character.upper()
			output_chunk.append(character)
		args.output_file.write("".join(output_chunk))
	print("Encryption compleate.")
if __name__ == "__main__":
	main()
