class Navegador:
	"""
	Simula la navegación web con historial atrás/adelante y grafo de transiciones.
	"""
	def __init__(self):
		self.grafo = {}  # dict[str, set[str]]
		self.actual = None  # str | None
		self.pila_atras = []  # list[str]
		self.pila_adelante = []  # list[str]

	def visitar(self, url: str):
		url = url.strip()
		if not url:
			raise ValueError("La URL no puede estar vacía.")
		if self.actual is not None:
			# Registrar arista actual -> url
			if self.actual not in self.grafo:
				self.grafo[self.actual] = set()
			self.grafo[self.actual].add(url)
			self.pila_atras.append(self.actual)
			self.pila_adelante.clear()
		self.actual = url
		if url not in self.grafo:
			self.grafo[url] = set()

	def atras(self):
		if not self.pila_atras:
			return False
		self.pila_adelante.append(self.actual)
		self.actual = self.pila_atras.pop()
		return True

	def adelante(self):
		if not self.pila_adelante:
			return False
		self.pila_atras.append(self.actual)
		self.actual = self.pila_adelante.pop()
		return True

	def vecinos(self, url: str):
		return self.grafo.get(url, set())

	def historial(self):
		return {
			"atras": list(self.pila_atras),
			"actual": self.actual,
			"adelante": list(reversed(self.pila_adelante)),
		}

	def get_actual(self):
		return self.actual
