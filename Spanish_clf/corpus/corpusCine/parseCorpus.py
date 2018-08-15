import xml.etree.ElementTree as ET
import os
import csv



def load_data(corpus_dir):
	fnames = [fname for fname in os.listdir(corpus_dir) if fname.endswith('.xml')]
	movies = []

	for file_name in fnames:
		#leemos el arch como cadena
		with open('corpusCriticasCine/' +file_name, 'r', encoding = 'cp1252') as file:
			cad = file.read()
		
		try:
			root = ET.fromstring(cad)
		except Exception as e:
			print(file_name)
			print(fnames.index(file_name))
			print(cad)
			raise e



		movie = {key: root.attrib[key] for key in root.attrib}
		movie[root.tag] = root.text
		
		summary = root[0]
		
		movie[summary.tag] = summary.text
		
		body = root[1]
		
		movie[body.tag] = body.text
		
		movies.append(movie)

		
	return movies



def main():
	corpus_dir = 'corpusCriticasCine'
	movies = load_data(corpus_dir)


	keys = {key for movie in movies for key in movie.keys()}
	with open('resenas.csv', 'wb') as f:
		writer = csv.DictWriter(f, keys)
		writer.writeheader()
		for movie in movies:
			writer.writerow(movie)

if __name__ == "__main__":
	main()
