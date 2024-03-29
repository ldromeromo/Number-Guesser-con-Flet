''' 
    Adivinador de números enteros
    ---------------
    Autor: Laura Daniela Romero Montañez

    Descripción:
    Este proyecto es una aplicación interactiva desarrollada en Python, utilizando la biblioteca Flet, diseñada para adivinar un número que el usuario piensa, 
    dentro de un rango del 0 al 1000. La interfaz gráfica facilita la interacción del usuario con la aplicación, permitiéndole indicar si el número presentado 
    por la aplicación es mayor, menor o igual al número que tiene en mente. Este proceso se repite hasta que la aplicación adivina correctamente el número, 
    demostrando un ejemplo práctico de cómo la lógica de programación y las interfaces de usuario pueden trabajar juntas para resolver un problema.

    Funcionalidades:
    - Generación Aleatoria de Números: Al inicio, la aplicación selecciona un número aleatorio dentro del rango especificado como su primera adivinanza.
    - Interacción del Usuario: El usuario interactúa con la aplicación a través de botones para indicar si el número mostrado es el correcto, o si el número 
      que piensa es mayor o menor al mostrado.
    - Ajuste de Adivinanzas: Basándose en la retroalimentación del usuario, la aplicación ajusta su rango de adivinanza y selecciona un nuevo número dentro de 
      este rango.
    - Historial de Intentos: La aplicación muestra un historial de los números que ha adivinado durante el intento actual, proporcionando una visión clara del 
      proceso de adivinanza.
    - Animación de Cierre: Una vez que el número es adivinado correctamente, se muestra una animación de celebración antes de cerrar automáticamente la aplicación.
    
    Métodos:
    - main(page: ft.Page): Método principal que configura la página, incluyendo el título, alineación, e inicializa los componentes de la UI y la lógica del juego.
    - update_guess(new_guess): Actualiza la adivinanza actual con un nuevo número y lo añade al historial de intentos visible para el usuario.
    - closing_animation(): Limpia la interfaz y muestra una animación de celebración con un mensaje de felicitación antes de cerrar la aplicación.
    - correct_guess(_): Función llamada cuando el usuario indica que la adivinanza es correcta. Inicia la secuencia de cierre.
    - up_guess(_), down_guess(_): Ajustan el rango de adivinanza basándose en la retroalimentación del usuario (si el número pensado es mayor o menor) y generan una 
      nueva adivinanza dentro del nuevo rango.
'''

import flet as ft
import random
import os
import time
import subprocess

def main(page: ft.Page):
    page.title = "Adivinador de números enteros"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    min_guess = 0
    max_guess = 1000
    guess = random.randint(min_guess, max_guess)
    attempts_history = []

    attempts_container = ft.Column(
        spacing=20,
        height=160,
        width=150,
        scroll=ft.ScrollMode.ALWAYS
    )
    
    def update_guess(new_guess):
        nonlocal guess
        guess = new_guess
        guess_field.value = str(guess)
        attempts_container.controls.append(ft.Text(guess))
        attempts_history.append(guess)
        page.update()

    def closing_animation():
        page.clean()
        icon = ft.Icon(ft.icons.CELEBRATION, size=30)
        page.add(icon)
        page.add(ft.Text("¡Felicidades! Se ha acertado el número.", size=16))
        page.add(ft.Text("Gracias por jugar, cerraremos la aplicación..."))
        page.update() 
        time.sleep(2)  
        subprocess.call('taskkill /F /T /PID %d' % os.getpid(), shell=True)
        
    def correct_guess(_):
        print("Se encontro el número correcto")
        closing_animation()

    def up_guess(_):
        nonlocal min_guess, max_guess
        if min_guess <= max_guess:
            min_guess = guess + 1
            new_guess = random.randint(min_guess, max_guess)
            update_guess(new_guess)
        else:
            print("¡Ya no hay más números para adivinar!")

    def down_guess(_):
        nonlocal min_guess, max_guess
        if min_guess <= max_guess:
            max_guess = guess - 1
            new_guess = random.randint(min_guess, max_guess)
            update_guess(new_guess)
        else:
            print("¡Ya no hay más números para adivinar!")

    guess_field = ft.TextField(value=str(guess), width=100, text_align="center")

    tittle_container = ft.Row(
        controls=[
            ft.Column(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("Adivinador de números enteros", size=20, weight="bold"),
                            ft.Text("Piensa en un número entero, entre el 0 y 1000.")
                        ],
                        spacing=10,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )
    
    main_container = ft.Row(
        controls=[
            ft.Column(
                controls=[
                    guess_field,
                    ft.Row([
                        ft.ElevatedButton(text="Correcto", on_click=correct_guess),
                        ft.IconButton(icon=ft.icons.SWIPE_UP, on_click=up_guess),
                        ft.IconButton(icon=ft.icons.SWIPE_DOWN, on_click=down_guess),
                    ])
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Column(
                controls=[
                    ft.Text("Historias de intentos"),
                    attempts_container
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                width="max-content"
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    page.add(tittle_container, main_container)

# Run the application loop
ft.app(target=main)
