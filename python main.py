#PROYECTO FINAL QUIZ DE GEOGRAFIA 
#Brigitte Gonzalez Alvarado
#Matricula 202607807
#Ingenieria en Sistemas y Tecnicas del la Informacion industrial
#Seccion 2       Generacion 2026
#Sede San Jose Chiapa, Puebla
#Complejo Regional Centro
#Benemerita Universidad Atonoma de Puebla
''' Proyecto de un  Quiz de Geografia mundial que permite contestar 5
preguntas aleatorias, seleccionar entre cuatro opciones, donde solo 1
es correcta, acumular puntos y perder vidas si se responde incorrectamente 
o se termina el tiempo establecido de 5 segundos, de acuerdo a las 
instrucciones de la maestra. '''

import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from pathlib import Path

ARCHIVO = Path(__file__).with_name("preguntas.txt")

# TODO: arreglar esto mañana xq ya son las 3am y no veo nada
class QuizGeografia:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Quiz de Geografía Mundial")
        self.ventana.geometry("720x500")
        self.ventana.configure(bg="#eaf2f8")
        self.inicio()

    def limpiar(self):
        for x in self.ventana.winfo_children():
            x.destroy()

    def resultados(self):
        self.activo = False
        t = int(time.time() - self.inicio_tiempo)
        mins, segs = divmod(t, 60)
        msg = "¡Se terminaron tus vidas!" if self.vidas == 0 else "¡Terminaste el juego!"
        self.limpiar()
        tk.Label(self.ventana, text="RESULTADOS", font=("Arial", 24, "bold"), bg="#eaf2f8").pack(pady=55)
        tk.Label(self.ventana, text=f"Puntaje: {self.puntos} puntos", font=("Arial", 17), bg="#eaf2f8").pack(pady=10)
        tk.Label(self.ventana, text=f"Vidas restantes: {self.vidas}", font=("Arial", 14), bg="#eaf2f8").pack(pady=8)
        tk.Label(self.ventana, text=f"Tiempo total: {mins:02d}:{segs:02d}", font=("Arial", 14), bg="#eaf2f8").pack(pady=8)
        tk.Label(self.ventana, text=msg, font=("Arial", 13), bg="#eaf2f8").pack(pady=12)
        ttk.Button(self.ventana, text="Volver al inicio", command=self.inicio).pack(pady=15)
        messagebox.showinfo("Juego terminado", msg)

    def inicio(self):
        self.activo = False
        self.limpiar()
        tk.Label(self.ventana, text="QUIZ DE GEOGRAFÍA MUNDIAL", font=("Arial", 23, "bold"), bg="#eaf2f8").pack(pady=70)
        tk.Label(self.ventana, text="Responde 5 preguntas de geografía.", font=("Arial", 14), bg="#eaf2f8").pack(pady=15)
        ttk.Button(self.ventana, text="Empezar", command=self.iniciar).pack(pady=25)
        tk.Label(self.ventana, text="Tienes 5 vidas y 5 segundos por pregunta.", bg="#eaf2f8").pack()

    def cargar_preguntas(self):
        tmp_list = []
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            for l in f:
                d = l.strip().split("|")
                if len(d) == 6 and all(d):
                    pregunta, a, b, c, d_opt, correcta = d
                    opts = [a, b, c, d_opt]
                    if correcta in opts:
                        random.shuffle(opts)
                        tmp_list.append((pregunta, opts, correcta))
        return tmp_list

    def iniciar(self):
        try:
            p_data = self.cargar_preguntas()
        except Exception as e:
            # por si no encuentra el txt
            messagebox.showerror("Error", f"No se pudo abrir el archivo.\n{e}")
            return
        if len(p_data) < 5:
            messagebox.showerror("Error", "Se necesitan al menos 5 preguntas válidas.")
            return
        self.preguntas = random.sample(p_data, 5)
        self.indice = 0
        self.puntos = 0
        self.vidas = 5
        self.inicio_tiempo = time.time()
        self.mostrar()

    def mostrar(self):
        self.activo = False
        self.limpiar()
        if self.vidas == 0 or self.indice == 5:
            self.resultados()
            return
        pregunta, opciones, correcta = self.preguntas[self.indice]
        tk.Label(self.ventana, text="QUIZ DE GEOGRAFÍA MUNDIAL", font=("Arial", 20, "bold"), bg="#eaf2f8").pack(pady=20)
        tk.Label(self.ventana, text=f"Puntos: {self.puntos}     Vidas: {self.vidas}     Pregunta: {self.indice + 1}/5", font=("Arial", 12, "bold"), bg="#eaf2f8").pack(pady=15)
        tk.Label(self.ventana, text=pregunta, font=("Times New Roman", 17, "bold"), fg="#0a0a0a", bg="#eaf2f8", wraplength=620).pack(pady=30)
        self.respuesta = tk.StringVar()
        self.opciones = ttk.Combobox(self.ventana, textvariable=self.respuesta, values=opciones, state="readonly", width=35)
        self.opciones.pack(pady=10)
        self.opciones.set("Selecciona una respuesta")
        self.reloj = tk.Label(self.ventana, bg="#eaf2f8", font=("Arial", 12, "bold"))
        self.reloj.pack(pady=15)
        ttk.Button(self.ventana, text="Responder", command=self.verificar).pack(pady=10)
        self.inicio_pregunta = time.time()
        self.activo = True
        self.contar()

    def contar(self):
        if not self.activo:
            return
        restante = 5 - int(time.time() - self.inicio_pregunta)
        if restante <= 0:
            self.activo = False
            self.vidas -= 1
            messagebox.showwarning("Tiempo agotado", "Perdiste una vida.")
            self.indice += 1
            self.mostrar()
        else:
            self.reloj.config(text=f"Tiempo restante: {restante} segundos")
            self.ventana.after(100, self.contar)

    def verificar(self):
        if not self.activo:
            return
        sel = self.respuesta.get()
        if sel == "" or sel == "Selecciona una respuesta":
            messagebox.showwarning("Atención", "Selecciona una respuesta.")
            return
        self.activo = False
        correcta = self.preguntas[self.indice][2]
        if sel == correcta:
            self.puntos += 10
            messagebox.showinfo("Correcto", "¡Ganaste 10 puntos!")
        else:
            self.vidas -= 1
            messagebox.showinfo("Incorrecto", f"La respuesta era: {correcta}")
        self.indice += 1
        self.mostrar()

if __name__ == "__main__":
    ventana = tk.Tk()
    juego = QuizGeografia(ventana)
    ventana.mainloop()