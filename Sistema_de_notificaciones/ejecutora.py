from pruebas_pdf import crear_pdf
from enviar_correos import main
print("pruebas------------------------------------")


usuarios = {"nombre": "nicolas", "apellido": "Urbina", "correo": "nicolasurbina77@gmail.com","cultivos":{"cultivo1": "tomate","cultivo2": "lechuga", "cultivo3": "fresa"},}
clima = {"dia1": {"dia": "Lunes", "temp": 20, "max": 20, "min": 10, "estado": "Soleado"},
        "dia2": {"dia": "Martes", "temp": 20, "max": 20, "min": 10, "estado": "Soleado"},
        "dia3": {"dia": "Miercoles", "temp": 215, "max": 20, "min": 10, "estado": "Soleado"},
        "dia4": {"dia": "Jueves", "temp": 215, "max": 215, "min": 10, "estado": "Soleado"},
        "dia5": {"dia": "Viernes", "temp": 410, "max": 20, "min": 10, "estado": "Soleado"},
        "dia6": {"dia": "Sabado", "temp": 410, "max": 410, "min": 10, "estado": "Soleado"}}
crear_pdf(clima, usuarios)
main('alanmcabelo@gmail.com')
