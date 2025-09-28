from enviar_correos import enviar_archivo
from modificadora import modificar_html, modificar_pdf

# pip install reportlab PyPDF2
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# pip install Jinja2



print("pruebas------------------------------------")
usuarios= {
    "pipo123@mail.com": {
        "nombre": "Pipo",
        "contrasena": "123",
        "ubicacion": {
            "latitud": 12.34,
            "longitud": 56.78
        },
        "cultivos": {
            "maiz": 10,
            "trigo": 5
        }
    },
    "pepito321@mail.com": {
        "nombre": "Pepito",
        "contrasena": "321",
        "ubicacion": {
            "latitud": 98.76,
            "longitud": 54.32
        },
        "cultivos": {
            "soja": 8,
            "girasol": 12
        }
    },
    "alan1234@mail.com": {
        "nombre": "alan",
        "contrasena": "1234",
        "ubicacion": {
            "latitud": 19.4326,
            "longitud": -99.1332
        },
        "cultivos": {
            "arroz": 15,
            "cebada": 7
        }
    },
    "kitian379@mail.com": {
        "nombre": "kitian",
        "contrasena": "379812",
        "ubicacion": {
            "latitud": 34.0522,
            "longitud": -118.2437
        },
        "cultivos": {
            "avena": 20,
            "centeno": 10
        }
    },
    "niko023@mail.com": {
        "nombre": "niko",
        "contrasena": "02381",
        "ubicacion": {
            "latitud": 51.5074,
            "longitud": -0.1278
        },
        "cultivos": {
            "lentejas": 6,
            "garbanzos": 9
        }
    },
    "john456@mail.com": {
        "nombre": "john",
        "contrasena": "123456",
        "ubicacion": {
            "latitud": 40.7128,
            "longitud": -74.006
        },
        "cultivos": {
            "frijoles": 14,
            "maiz": 11
        }
    },
    "plim910@mail.com": {
        "nombre": "plimplomplim",
        "contrasena": "832910",
        "ubicacion": {
            "latitud": 10.0,
            "longitud": 10.0
        },
        "cultivos": {
            "trigo": 4,
            "soja": 16
        }
    },
    "caliaga2005@gmail.com": {
        "nombre": "Cristiano Alonsinhio",
        "contrasena": "$argon2id$v=19$m=65536,t=2,p=2$MsltzNCBPnAOu3WZHhLLtQ$v/m6kX1aYwgU0xy7HK84ufjCH3zIDw1J0jabcGwpu/k"
    },
    "alanomunoz@gmail.com": {
        "nombre": "Alanito Fulanito",
        "contrasena": "$argon2id$v=19$m=65536,t=2,p=2$b+FI9OjONofAY9FkoTIAIQ$k3O4hJGYksWj+BwruS+MDCORseXsG94eOjm7nQ1hIyA"
    },
    "Cristian12345678@gmail.com": {
        "nombre": "Cristian Aliaga",
        "contrasena": "$argon2id$v=19$m=65536,t=2,p=2$zW/j2Hc6eD4fBhl9hM1C/w$t6NA2IvP/isL+C8UNseNcV73T8p+er/eFzaRxrmiJEY"
    },
    "horacio31M@outlook.com": {
        "nombre": "Horacio News",
        "contrasena": "$argon2id$v=19$m=65536,t=2,p=2$3xZzlJ68XgR+MH/Zp0O5YQ$RYrGbEYKt1v1GcK8dkRe2RQ/iCkDvg9NnA8mExtQr68"
    },
    "a@a.a": {
        "nombre": "a",
        "contrasena": "$argon2id$v=19$m=65536,t=2,p=2$iUTA1JFxedbkq+881z+swQ$E1h8EgAnxUyCxbjRnbxFyE/jBfzj+zvXFaFVMfUlQjI"
    },
    "alan@munoz.cl": {
        "nombre": "Alan",
        "contrasena": "$argon2id$v=19$m=65536,t=2,p=2$lhPu14wB/1iImO+SBhr4cA$mYo5u+XdNBaz31ppgxctm+zOOG0DgrL2A0pREPQoFBg"
    },
    "pepitomargnolio@gmail.com": {
        "nombre": "Felipe Magno",
        "contrasena": "$argon2id$v=19$m=65536,t=2,p=2$rxKAXgH3582tfeykY1re1w$8vpkmyjbuOHGF4N2ZiGiObCgoqxuNjx5fv9XTiGytoI",
        "ubicacion": {
            "latitud": 10.89,
            "longitud": 5.0
        },
        "cultivos": {
            "Maiz": 20
        }
    },
    "aa@a.a": {
        "nombre": "aa",
        "contrasena": "$argon2id$v=19$m=65536,t=2,p=2$jfSremk46ykNU73gDB9qGw$i4cK5sIqvTEB+jHvWiqx90B59RGPt410yi9YEpM2U0o",
        "ubicacion": {
            "latitud": None,
            "longitud": None
        },
        "cultivos": {}
    }
}
usuario=usuarios.get("pipo123@mail.com")
clima = {"dia1": {"dia": "Lunes", "temp": 20, "max": 20, "min": 10, "estado": "Soleado"},
        "dia2": {"dia": "Martes", "temp": 20, "max": 20, "min": 10, "estado": "Soleado"},
        "dia3": {"dia": "Miercoles", "temp": 215, "max": 20, "min": 10, "estado": "Soleado"},
        "dia4": {"dia": "Jueves", "temp": 215, "max": 215, "min": 10, "estado": "Soleado"},
        "dia5": {"dia": "Viernes", "temp": 410, "max": 20, "min": 10, "estado": "Soleado"},
        "dia6": {"dia": "Sabado", "temp": 410, "max": 410, "min": 10, "estado": "Soleado"}}

#modificar_html nececita usuario ya filtrado con la informacion en diccionario y el clima em diccionario 
modificar_html(usuario,clima)

#enviar_archivo nececita el correo del detinatario y la ruta a enviar
enviar_archivo('nicolasurbina77@gmail.com','Archivos_HTML\salida.html')
enviar_archivo('nicolasurbina77@gmail.com', 'Archivos_pdf\pdf_modificado.pdf')

