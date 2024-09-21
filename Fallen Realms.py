import tkinter as tk
import random


class Terreno:
    def __init__(self):
        self.tipos = ['Plains', 'Forest', 'Hills', 'Swamp', 'Mountain', 'Ruin']
        self.colores = {
            'Plains': 'lightgreen',
            'Forest': 'darkgreen',
            'Hills': 'sandybrown',
            'Swamp': 'darkslategray',
            'Mountain': 'gray',
            'Ruin': 'lightgray'
        }
        self.probabilidades = {
            'Plains': 0.2,
            'Forest': 0.2,
            'Hills': 0.2,
            'Swamp': 0.2,
            'Mountain': 0.1,
            'Ruin': 0.1
        }
        self.efectos = {
            'Plains': 'Movimiento normal.',
            'Forest': 'Reducción de visibilidad.',
            'Hills': 'Bonificación a la defensa.',
            'Swamp': 'Pérdida de vida al final del turno.',
            'Mountain': 'Pérdida de vida y no se puede mover.',
            'Ruin': 'Posibilidad de tesoros.'
        }

    def seleccionar_terreno(self):
        random_value = random.random()
        cumulative_probability = 0.0

        for tipo, prob in self.probabilidades.items():
            cumulative_probability += prob
            if random_value < cumulative_probability:
                return tipo
        return 'Plains'

    def generar_tablero(self, tamaño, area_max=5):
        tablero = [['' for _ in range(tamaño)] for _ in range(tamaño)]
        zonas = int((tamaño * tamaño) / (area_max * area_max))

        for _ in range(zonas):
            tipo_terreno = self.seleccionar_terreno()
            area_size = random.randint(4, area_max)
            start_x = random.randint(0, tamaño - 1)
            start_y = random.randint(0, tamaño - 1)
            self.expandir_zona(tablero, start_x, start_y, tipo_terreno, area_size)

        # Colocar un máximo de 4 ruinas en posiciones aleatorias
        for _ in range(4):
            x, y = random.randint(0, tamaño - 1), random.randint(0, tamaño - 1)
            tablero[x][y] = 'Ruin'

        # Llenar cualquier celda vacía con un tipo de terreno aleatorio
        for i in range(tamaño):
            for j in range(tamaño):
                if tablero[i][j] == '':
                    tablero[i][j] = self.seleccionar_terreno()

        return tablero

    def expandir_zona(self, tablero, x, y, tipo_terreno, area_size):
        if area_size <= 0 or x < 0 or y < 0 or x >= len(tablero) or y >= len(tablero[0]) or tablero[x][y] != '':
            return

        tablero[x][y] = tipo_terreno

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if abs(dx) != abs(dy):
                    self.expandir_zona(tablero, x + dx, y + dy, tipo_terreno, area_size - 1)

    def obtener_color(self, tipo):
        return self.colores[tipo]

    def obtener_efecto(self, tipo):
        return self.efectos[tipo]


class Juego(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fallen Realms")
        self.geometry("900x800")
        self.terreno = Terreno()
        self.tablero = None
        self.crear_pantalla_inicio()

    def crear_pantalla_inicio(self):
        self.btn_jugar = tk.Button(self, text="Jugar", command=self.iniciar_juego)
        self.btn_jugar.pack(pady=20)

        self.btn_instrucciones = tk.Button(self, text="Instrucciones", command=self.mostrar_instrucciones)
        self.btn_instrucciones.pack(pady=20)

        self.btn_salir = tk.Button(self, text="Salir", command=self.quit)
        self.btn_salir.pack(pady=20)

    def iniciar_juego(self):
        self.tablero = self.terreno.generar_tablero(25, area_max=5)
        self.limpiar_pantalla()
        self.crear_tablero()
        self.crear_muestra_terrenos()  # Muestra de terrenos también al iniciar el juego

    def mostrar_instrucciones(self):
        self.limpiar_pantalla()
        self.crear_muestra_terrenos()

    def limpiar_pantalla(self):
        for widget in self.winfo_children():
            widget.destroy()  # Limpiar la pantalla actual

        self.crear_pantalla_inicio()  # Re-crear la pantalla de inicio

    def crear_muestra_terrenos(self):
        muestra_frame = tk.Frame(self)
        muestra_frame.pack(pady=10)

        for tipo in self.terreno.tipos:
            color = self.terreno.obtener_color(tipo)
            fila_frame = tk.Frame(muestra_frame)
            fila_frame.pack(side=tk.TOP, padx=5, pady=2)

            cuadro = tk.Frame(fila_frame, width=30, height=30, bg=color, borderwidth=0)
            cuadro.pack(side=tk.LEFT)

            efecto_texto = self.terreno.obtener_efecto(tipo)
            etiqueta = tk.Label(fila_frame, text=f"{tipo}: {efecto_texto}", bg=color)
            etiqueta.pack(side=tk.LEFT)

    def crear_tablero(self):
        tablero_frame = tk.Frame(self)
        tablero_frame.pack()

        for i in range(25):
            for j in range(25):
                tipo_terreno = self.tablero[i][j]
                color = self.terreno.obtener_color(tipo_terreno)
                cuadro = tk.Frame(tablero_frame, width=30, height=30, bg=color, borderwidth=0)
                cuadro.grid(row=i, column=j)


if __name__ == "__main__":
    juego = Juego()
    juego.mainloop()
