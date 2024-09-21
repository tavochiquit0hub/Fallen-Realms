import tkinter as tk
import random


class Personaje:
    def __init__(self, nombre, vida, ataque, sprite):
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque
        self.sprite = sprite

    def atacar(self, otro):
        danio = random.randint(1, self.ataque)
        otro.vida -= danio
        return danio

    def esta_vivo(self):
        return self.vida > 0


class Bestia:
    def __init__(self, nombre, vida, ataque, sprite):
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque
        self.sprite = sprite

    def atacar(self, otro):
        danio = random.randint(1, self.ataque)
        otro.vida -= danio
        return danio

    def esta_vivo(self):
        return self.vida > 0


class Juego(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Juego por Turnos: Personajes vs Bestia")

        # Personajes
        self.personajes = [
            Personaje("Mago", vida=30, ataque=10, sprite="🧙‍♂️"),
            Personaje("Sanador", vida=25, ataque=8, sprite="💊"),
            Personaje("Arquero", vida=28, ataque=9, sprite="🏹"),
            Personaje("Asesino", vida=20, ataque=12, sprite="🗡️")
        ]

        # Bestia
        self.bestia = Bestia("Bestia", vida=50, ataque=15, sprite="🐉")

        self.turno = 0
        self.crear_widgets()
        self.actualizar_estado()

    def crear_widgets(self):
        self.info_frame = tk.Frame(self)
        self.info_frame.pack()

        self.estado_label = tk.Label(self.info_frame, text="", justify=tk.LEFT)
        self.estado_label.pack()

        # Personajes
        self.personaje_frames = []
        for personaje in self.personajes:
            frame = tk.Frame(self.info_frame)
            frame.pack(side=tk.TOP, padx=5, pady=5)
            sprite_label = tk.Label(frame, text=personaje.sprite, font=("Arial", 24))
            sprite_label.pack(side=tk.LEFT)
            nombre_label = tk.Label(frame, text=personaje.nombre, width=10, bg='lightblue')
            nombre_label.pack(side=tk.LEFT)
            vida_label = tk.Label(frame, text=f'Vida: {personaje.vida}', width=10)
            vida_label.pack(side=tk.LEFT)
            self.personaje_frames.append((frame, vida_label, personaje))

        # Bestia
        self.bestia_frame = tk.Frame(self.info_frame)
        self.bestia_frame.pack(side=tk.TOP, padx=5, pady=5)
        bestia_sprite_label = tk.Label(self.bestia_frame, text=self.bestia.sprite, font=("Arial", 24))
        bestia_sprite_label.pack(side=tk.LEFT)
        bestia_nombre_label = tk.Label(self.bestia_frame, text=self.bestia.nombre, width=10, bg='lightcoral')
        bestia_nombre_label.pack(side=tk.LEFT)
        bestia_vida_label = tk.Label(self.bestia_frame, text=f'Vida: {self.bestia.vida}', width=10)
        bestia_vida_label.pack(side=tk.LEFT)

        self.atacar_button = tk.Button(self, text="Atacar", command=self.atacar)
        self.atacar_button.pack(pady=10)

        self.mensaje_label = tk.Label(self, text="")
        self.mensaje_label.pack()

    def actualizar_estado(self):
        for frame, vida_label, personaje in self.personaje_frames:
            vida_label.config(text=f'Vida: {personaje.vida}')
        self.bestia_frame.winfo_children()[2].config(text=f'Vida: {self.bestia.vida}')

    def atacar(self):
        atacante = self.personajes[self.turno]
        danio = atacante.atacar(self.bestia)
        mensaje = f"{atacante.nombre} ataca a {self.bestia.nombre} y causa {danio} de daño."

        if not self.bestia.esta_vivo():
            mensaje += f" {self.bestia.nombre} ha caído."
            self.atacar_button.config(state=tk.DISABLED)  # Desactivar el botón al terminar el juego

        self.turno = (self.turno + 1) % len(self.personajes)
        self.actualizar_estado()
        self.mensaje_label.config(text=mensaje)

        # Ataque de la bestia
        if self.bestia.esta_vivo():
            objetivo = random.choice(self.personajes)
            danio = self.bestia.atacar(objetivo)
            self.mensaje_label.config(text=f"{self.bestia.nombre} ataca a {objetivo.nombre} y causa {danio} de daño.")
            self.actualizar_estado()

            if not objetivo.esta_vivo():
                self.mensaje_label.config(text=f"{objetivo.nombre} ha caído.")

            self.turno = (self.turno + 1) % len(self.personajes)


if __name__ == "__main__":
    juego = Juego()
    juego.mainloop()
dawdaw