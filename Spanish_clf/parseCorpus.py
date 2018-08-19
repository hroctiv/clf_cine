import xml.etree.ElementTree as ET
import os
import csv



def load_data(corpus_dir):
	fnames = [fname for fname in os.listdir(corpus_dir) if fname.endswith('.xml')]
	movies = []
	err_count = 0
	for i_file, file_name in enumerate(fnames):
		#leemos el arch como cadena
		with open(corpus_dir +file_name, 'r', encoding = 'cp1252') as file:
			cad = file.read()
		
		try:
			root = ET.fromstring(cad)
		except Exception as e:
			#print(file_name)
			#print(fnames.index(file_name))
			#print(cad)
			#print(e)
			err_count += 1
			continue



		movie = {key: root.attrib[key] for key in root.attrib}
		movie['index_in_corpus'] = i_file
		movie['file_name'] = file_name
		movie[root.tag] = root.text
		
		summary = root[0]
		
		movie[summary.tag] = summary.text
		
		body = root[1]
		
		movie[body.tag] = body.text
		
		movies.append(movie)
	print("total reviews:",len(fnames))
	print("ok:",len(movies))
	print("errors:", err_count)
		
	return movies



def main():
	corpus_dir = 'corpus/corpusCine/corpusCriticasCine/'
	movies = load_data(corpus_dir)


	keys = {key for movie in movies for key in movie.keys()}
	with open('corpus/corpusCine/resenas.csv', 'w') as f:
		writer = csv.DictWriter(f, keys, delimiter='|', quotechar='^')
		writer.writeheader()
		for movie in movies:
			writer.writerow(movie)

if __name__ == "__main__":
	main()
