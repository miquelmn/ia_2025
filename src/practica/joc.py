""" Labyrinth game. First practice.

Author: Miquel Miró Nicolau (UIB), 2024.
"""
import random
import pygame
from importlib.resources import files

from iaLib import agent as agent_lib
from iaLib import joc


class Viatger(agent_lib.Agent):
	N_VIATGERS = 0

	def __init__(self, nom: str = None):
		super().__init__(long_memoria=1)
		if nom is None:
			Viatger.N_VIATGERS += 1
			nom = f"Agent {Viatger.N_VIATGERS}"

		self.__nom = nom

	def pinta(self, display):
		pass

	def actua(self, percepcio: dict) -> tuple[str, tuple | None]:
		return "ESPERAR", None

	@property
	def nom(self):
		return self.__nom

	@nom.setter
	def nom(self, value):
		self.__nom = value


class Casella:
	IMG_DESTI = files("practica.images") / "desti.png"
	IMG_AGENT = files("practica.images") / "robot.png"

	SIZE = (50, 50)

	def __init__(self, is_paret=False, in_agent=False, desti=False):
		if is_paret + in_agent > 1:
			raise ValueError(f"Casella incompatible {is_paret}, {in_agent}")

		self.__is_paret = is_paret
		self.__in_agent = in_agent
		self.__desti = desti

	@property
	def agent(self):
		return self.__in_agent

	@agent.setter
	def agent(self, value):
		if self.__is_paret and value:
			raise ValueError(f"Agent sobre una paret")

		self.__in_agent = value

	@property
	def desti(self):
		return self.__desti

	@desti.setter
	def desti(self, value):
		if self.__is_paret:
			raise ValueError("Destí sobre paret")
		self.__desti = value

	@property
	def paret(self):
		return self.__is_paret

	@paret.setter
	def paret(self, value):
		self.__is_paret = value

	def is_accessible(self):
		return not self.__is_paret and not self.__in_agent

	def draw(self, window, x, y):
		pygame.draw.rect(
			window,
			pygame.Color(0, 0, 0),
			pygame.Rect(
				x * Casella.SIZE[0],
				y * Casella.SIZE[1],
				Casella.SIZE[0],
				Casella.SIZE[1],
			),
			1 if not self.__is_paret else 0,
		)
		if self.__in_agent:
			img = pygame.image.load(Casella.IMG_AGENT)
			img = pygame.transform.scale(img, Casella.SIZE)
			window.blit(img, (x * Casella.SIZE[0], y * Casella.SIZE[1]))

		if self.__desti:
			img = pygame.image.load(Casella.IMG_DESTI)
			img = pygame.transform.scale(img, Casella.SIZE)
			window.blit(img, (x * Casella.SIZE[0], y * Casella.SIZE[1]))


class Laberint(joc.Joc):
	MOVS = {
		"N": (0, -1),
		"O": (-1, 0),
		"S": (0, 1),
		"E": (1, 0),
	}

	def __init__(
			self,
			agents,
			mida_taulell=(12, 12),
			pos_final=None,
			parets=None,
	):
		super().__init__(
			agents,
			(mida_taulell[0] * Casella.SIZE[0], mida_taulell[1] * Casella.SIZE[1]),
			title="Pràctica 1",
		)
		self.__acabat = False

		self.__mida_taulell = mida_taulell
		self.__caselles = [
			[Casella() for _ in range(self.__mida_taulell[1])]
			for _ in range(self.__mida_taulell[0])
		]

		self.__agents = agents
		self.__agents_pos = {}

		pos_x, pos_y = list(range(0, mida_taulell[0])), list(range(0, mida_taulell[1]))
		for a in self.__agents:
			x = pos_x.pop(random.randint(0, len(pos_x) - 1))
			y = pos_y.pop(random.randint(0, len(pos_y) - 1))

			self.__caselles[x][y].agent = True
			self.__agents_pos[a.nom] = (x, y)

		if pos_final is None:
			pos_final = (
				pos_x.pop(random.randint(0, len(pos_x) - 1)),
				pos_y.pop(random.randint(0, len(pos_y) - 1))
			)

		self.__desti = pos_final
		self.__caselles[pos_final[0]][pos_final[1]].desti = True

		self.__parets = set()
		self.__afegeix_parets(parets)

	@property
	def size(self) -> int:
		return self.__mida_taulell[0] * self.__mida_taulell[1]

	def __afegeix_parets(self, parets: list[int] = None):
		"""Afegeix les parets passades per paràmetre.

		Args:
			parets (llista d'enters): Posicions a on hi ha una paret.
		"""
		if parets is None:
			parets = [i for i in range(self.size) if random.randint(0, 2) == 0]

		for paret in parets:
			x, y = paret // self.__mida_taulell[0], paret % self.__mida_taulell[0]
			if not self.__caselles[x][y].desti and self.__caselles[x][y].is_accessible():
				self.__caselles[x][y].paret = True
				self.__parets.add((x, y))

	@property
	def pos_agents(self):
		return self.__agents_pos

	@staticmethod
	def __obte_pos(pos_original: tuple[int, int], multiplicador: int, direccio: str):
		return (
			Laberint.MOVS[direccio][0] * multiplicador + pos_original[0],
			Laberint.MOVS[direccio][1] * multiplicador + pos_original[1],
		)

	def __pos_correcte(self, pos) -> bool:
		return 0 <= pos[0] < self.__mida_taulell[0] and 0 <= pos[1] < self.__mida_taulell[1]

	def __moure_agent(
			self, direccio, nom_agent, multiplicador
	):
		""" Mou l'agent en la direcció indicada.

		Args:
			direccio (str): N,S,W,E. Els punts cardinals.
			multiplicador (int): Bot del moviment.
		"""
		pos_original = self.__agents_pos[nom_agent]
		pos_updated = self.__obte_pos(pos_original, multiplicador, direccio)

		if self.__pos_correcte(pos_updated) and self.__caselles[pos_updated[0]][pos_updated[1]].is_accessible():
			self.__caselles[pos_original[0]][pos_original[1]].agent = False
			self.__caselles[pos_updated[0]][pos_updated[1]].agent = True

			self.__agents_pos[nom_agent] = pos_updated
		else:
			raise ValueError("Posició no possible")

		return pos_original, pos_updated

	def _aplica(
			self, accio, params=None, agent_actual: str = None
	) -> None:
		if not self.__acabat:
			if accio not in ("ESPERAR", "MOURE", "BOTAR", "POSAR_PARET"):
				raise ValueError(f"Acció no existent en aquest joc: {accio}")

			if accio == "MOURE" or accio == "BOTAR":
				if params not in ("N", "S", "E", "O"):
					raise ValueError(f"Paràmetre {params} incorrecte per acció MOURE")

				pos_original, pos_updated = self.__moure_agent(
					params, agent_actual, int(accio == "BOTAR") + 1
				)

				self.__caselles[pos_original[0]][pos_original[1]].paret = True
				self.__parets.add(pos_original)

				if self.__caselles[pos_updated[0]][pos_updated[1]].desti:
					self.__caselles[pos_updated[0]][pos_updated[1]].desti = False
					self.__acabat = True
					print(f"L'agent {agent_actual} ha guanyat")

			elif accio == "POSAR_PARET":
				if params not in ("N", "S", "E", "O"):
					raise ValueError(
						f"Paràmetre {params} incorrecte per acció POSAR_PARET"
					)
				pos_original = self.__agents_pos[agent_actual]
				pos_updated = self.__obte_pos(pos_original, 1, params)

				if (
						self.__pos_correcte(pos_updated)
						and self.__caselles[pos_updated[0]][pos_updated[1]].is_accessible()
				):
					self.__caselles[pos_updated[0]][pos_updated[1]].paret = True
					self.__parets.add(pos_updated)
				else:
					raise ValueError(f"Acció no possible a la casella {pos_updated}")

	def _draw(self) -> None:
		super()._draw()
		window = self._game_window
		window.fill(pygame.Color(255, 255, 255))

		for x, row in enumerate(self.__caselles):
			for y, cas in enumerate(row):
				cas.draw(window, x, y)

	def percepcio(self):
		torn = self.__agents[self.turn % len(self.__agents)].nom

		return {
			"PARETS": self.__parets,
			"DESTI": self.__desti,
			"AGENTS": self.pos_agents,
			"MIDA": self.__mida_taulell,
			"TORN": torn
		}
