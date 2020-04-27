# main.py

from fastapi import FastAPI
from pydantic import BaseModel
import asyncio

# Zadanie 1
# Stwórz ścieżkę '/' która zwracać będzie odpowiedź w postaci JSONa
# `{"message": "Hello World during the coronavirus pandemic!"}`
# PS 1 Zobacz co można znaleźć pod endpoitem `/docs`

app = FastAPI()
app.licznik = asyncio.Semaphore(0)
app.pacjenci = list()

@app.get("/welcome")
@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

# Zadanie 2
# Stwórz ścieżkę '/method' która zwróci nazwę metody z jaką wykonano request.
# PS Wystarczy jeśli endpoint będzie obsługiwał requesty `GET`, `POST`, `PUT`, `DELETE`
# PS2 W kodzie nie wolno użyć żadnego `ifa`

# format odpowiedzi(JSON):
# `{"method": "METHOD"}`

@app.get("/method")
async def method():
    return {"method": "GET"}

@app.post("/method")
async def method():
    return {"method": "POST"}

@app.put("/method")
async def method():
    return {"method": "PUT"}

@app.delete("/method")
async def method():
    return {"method": "DELETE"}


# Zadanie 3

# Stwórz ścieżkę `/patient`, która przyjmie request z metodą `POST` i danymi w formacie json w postaci:

# `{"name": "IMIE", "surename": "NAZWISKO"}`

# i zwróci JSON w postaci:

# `{"id": N, "patient": {"name": "IMIE", "surename": "NAZWISKO"}}`

# Gdzie `N` jest kolejnym numerem zgłoszonej osoby

# Naturalnie ścieżka ma działać dla dowolnych stringów (w kodowaniu utf-8) podanych w polach `name` i `surename`.

# PS 1 W tym zadaniu ważne jest aby znaleźć miejsce w którym będzie można zapisać ilość odwiedzin od ostatniego uruchomienia aplikacji na serwerze oraz umieć posługiwać JSONami.
# Na tym etapie kursu nie bawimy się w bazy danych. Być może spostrzeżesz bardzo ciekawe zachowanie ;-)

# PS 2 Przed uruchomieniem testów, należy zrestartować swoją aplikację, żeby licznik na początku miał wartość 0!

# class Pacjent(BaseModel):
#     imie: str
#     nazwisko: str
#     N: int

# @app.post("/patient")
# async def patient(pac: Pacjent):
#     pac.N = 0
#     return {"id": pac.N, "patient": {"name": pac.imie, "surename": pac.nazwisko}}

class Pacjent(BaseModel):
    name: str
    surename: str

class Odpowiedz(BaseModel):
    id: int
    patient: Pacjent

@app.post("/patient",response_model=Odpowiedz)
def pacjent(pt: Pacjent):

    odpowiedz = Odpowiedz(id=app.licznik._value,patient=pt)
    app.licznik.release()
    app.pacjenci.append(odpowiedz) # dla zadania 4
    return odpowiedz



# Zadanie 4 
# Stwórz ścieżkę `/patient/{pk}`, która przyjmuje request w metodą GET.

# pk, powinien być liczbą. Najlepiej intem.

# W przypadku znalezienia takiego pacjenta, odpowiedź powinna wyglądać tak:
# `{"name": "NAME", "surename": "SURENAME"}`

# W przypadku nieznalezienia należy zwrócić odpowiedni kod http:
# https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

# PS 1 Podobnie jak w poprzednim zadaniu, znajdź miejsce w aplikacji, gdzie można zapisać pacjenta

# PS 2 Zmodyfikuj endpoint POST `/patient`, tak aby zachował przesłane dane

# PS 3 Pamiętaj, aby liczyć pacjentów od 0!

@app.get("/patient/{pk}")
def zwrocPacjenta(pk: int):
    if pk > -1 and pk < len(app.pacjenci):
        return app.pacjenci[pk]

    return ""