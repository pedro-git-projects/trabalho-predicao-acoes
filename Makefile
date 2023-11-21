run:
	python main.py

doc:
	pdoc --output-dir ./docs/ ./preprocessadores/ouro.py ./preprocessadores/petroleo.py ./preditor/preditor.py ./comparador/comparador.py
	
