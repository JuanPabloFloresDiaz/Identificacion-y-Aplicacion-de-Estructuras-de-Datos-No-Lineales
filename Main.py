"""
Problema 2: Navegación web (Atrás/Adelante)

PLANTEAMIENTO Y JUSTIFICACIÓN (estructura no lineal recomendada)
----------------------------------------------------------------
- Estructura recomendada: Grafo dirigido (no lineal), complementado con dos pilas
	(historial-atrás e historial-adelante) para las operaciones de navegación.

- ¿Por qué grafo y no lista/árbol?
	* Un árbol no modela bien la navegación real: la misma página puede alcanzarse
		por múltiples rutas (múltiples "padres") y existen ciclos, lo que viola las
		restricciones de los árboles.
	* Una lista lineal pierde información de ramificaciones: al visitar una nueva
		página desde un punto intermedio, se crea una nueva rama en el historial.
	* Un grafo dirigido modela páginas como nodos y transiciones de navegación como
		aristas dirigidas (u -> v). Permite múltiples caminos entre nodos y ciclos.

- ¿Por qué además dos pilas si ya tenemos un grafo?
	* El grafo representa el mapa/conexiones entre páginas (contexto global),
		mientras que el comportamiento "atrás/adelante" es estrictamente LIFO
		(Last-In First-Out). Por eficiencia O(1) y simplicidad, se gestionan con dos
		pilas:
			- pila_atras: guarda las páginas previas al estado actual
			- pila_adelante: guarda las páginas a las que se puede volver a avanzar
	* Esto separa: (1) la topología (grafo) de (2) la mecánica de navegación (pilas).

Complejidad esperada:
- visitar(url): O(1) amortizado (push a pila_atras, limpiar pila_adelante,
	crear nodos/aristas si no existen)
- atras(): O(1) si hay elementos
- adelante(): O(1) si hay elementos
- registrar arista en el grafo: O(1) usando listas o conjuntos de adyacencia

Casos borde a contemplar:
- atras() con pila_atras vacía: no hace nada y se informa al usuario.
- adelante() con pila_adelante vacía: no hace nada y se informa al usuario.
- visitar(url) cuando no hay página actual (primera visita): solo establece
	actual=url (no se empuja nada a pila_atras) y crea el nodo en el grafo.
- visitas repetidas a la misma URL: se registran, evitando duplicar aristas si
	usamos conjuntos de adyacencia.


CÓMO LO IMPLEMENTAREMOS (plan de implementación)
-----------------------------------------------
Contrato mínimo (API de la sesión de navegación):
- Estructuras internas:
		grafo: dict[str, set[str]]  # lista de adyacencia (nodo -> vecinos)
		actual: str | None          # URL actual (None si no hay)
		pila_atras: list[str]
		pila_adelante: list[str]

- Operaciones:
		visitar(url: str) -> None
				- Si existe página actual: registrar arista actual -> url en grafo.
				- Empujar actual en pila_atras.
				- Limpiar pila_adelante (nueva rama de navegación).
				- Establecer actual = url (crear nodo si no existía en grafo).

		atras() -> None
				- Si pila_atras no está vacía:
						* Empujar actual en pila_adelante.
						* actual = pila_atras.pop().
				- Si está vacía: informar que no hay más atrás.

		adelante() -> None
				- Si pila_adelante no está vacía:
						* Empujar actual en pila_atras.
						* actual = pila_adelante.pop().
				- Si está vacía: informar que no hay más adelante.

		vecinos(url: str) -> set[str]
				- Retorna los destinos directos registrados desde url en el grafo.

- Interfaz de usuario (CLI simple):
		Comandos: visitar <url>, atras, adelante, actual, historial, vecinos <url>, salir.
		- historial mostrará: pila_atras (del más antiguo al más reciente), actual y
			pila_adelante (del más reciente al más antiguo), para transparencia.

Validaciones básicas de entrada:
- URL no vacía, sin espacios extremos.
- Comandos desconocidos: mostrar ayuda corta.

Notas de diseño:
- Usaremos conjuntos (set) para adyacencias y así evitar aristas duplicadas.
- Mantendremos la lógica acotada en una clase Navegador con los métodos descritos.
- La CLI vivirá bajo un guard if __name__ == "__main__": y no se ejecutará nada
	al importar el módulo (facilita pruebas).

Siguiente paso (cuando lo indiquen):
- Implementar la clase Navegador y la CLI según el plan anterior.
"""


# Implementación CLI para el problema 2: Navegador web
from models.Navegador import Navegador
from utils.Teclado import Teclado
from utils.Validaciones import Validaciones

def mostrar_ayuda():
	print("Comandos disponibles:")
	print("  visitar <url>      - Visitar una nueva página")
	print("  atras              - Ir a la página anterior")
	print("  adelante           - Ir a la página siguiente")
	print("  actual             - Mostrar la página actual")
	print("  historial          - Mostrar el historial de navegación")
	print("  vecinos <url>      - Mostrar destinos directos desde una página")
	print("  salir              - Terminar la sesión")

def main():
	nav = Navegador()
	print("Simulador de Navegador Web (Problema 2)")
	mostrar_ayuda()
	while True:
		try:
			entrada = Teclado.read_text("\n> ", min_length=1)
		except (EOFError, KeyboardInterrupt):
			print("\nSaliendo...")
			break
		if not entrada:
			continue
		partes = entrada.split()
		comando = partes[0].lower()
		args = partes[1:]

		if comando == "visitar":
			if not args:
				print("Falta la URL. Uso: visitar <url>")
				continue
			url = " ".join(args).strip()
			# Validar URL no vacía y sin espacios extremos
			if not Validaciones.validate_length(url, min_length=1):
				print(Validaciones.get_validation_message('empty'))
				continue
			try:
				nav.visitar(url)
				print(f"Visitando: {url}")
			except ValueError as e:
				print(e)
		elif comando == "atras":
			if nav.atras():
				print(f"Página actual: {nav.get_actual()}")
			else:
				print("No hay más páginas atrás.")
		elif comando == "adelante":
			if nav.adelante():
				print(f"Página actual: {nav.get_actual()}")
			else:
				print("No hay más páginas adelante.")
		elif comando == "actual":
			actual = nav.get_actual()
			print(f"Página actual: {actual if actual else 'Ninguna'}")
		elif comando == "historial":
			h = nav.historial()
			print("Historial atrás:", h["atras"])
			print("Página actual:", h["actual"])
			print("Historial adelante:", h["adelante"])
		elif comando == "vecinos":
			if not args:
				print("Falta la URL. Uso: vecinos <url>")
				continue
			url = " ".join(args).strip()
			if not Validaciones.validate_length(url, min_length=1):
				print(Validaciones.get_validation_message('empty'))
				continue
			vecinos = nav.vecinos(url)
			print(f"Vecinos de {url}: {sorted(vecinos) if vecinos else 'Ninguno'}")
		elif comando == "salir":
			print("Saliendo...")
			break
		else:
			print("Comando desconocido.")
			mostrar_ayuda()

if __name__ == "__main__":
	main()

