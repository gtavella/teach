# Come modificare una funzione senza modificarla
# Cioe' come modificarla "da fuori" senza mai toccarla dall'interno,
# e farla eseguire prima o dopo un'altra funzione
# Tutto questo senza modificare la funzione principale


# ESEMPIO 1 ***************

def func(x):
  print(x)

func(10)

def modifier(modified):
  def inner(x):
    a = x + 1
    modified(a)
  return inner

func = modifier(func)


func(10)


# ESEMPIO 2 ***************


def modifier2(modified):
  def inner(x):
    a = x + 1
    modified(a)
  return inner

@modifier2
def func2(x):
  print(x)


func2(10)


# ESEMPIO 3 ***************


def stampa_qualcosa(func):
  def inner(x, y):
    print("ecco i risultati: ")
    func(x, y)
  return inner


@stampa_qualcosa
def moltiplica(x, y):
  ris = x * y
  print(ris)


moltiplica(3, 7)



# ESEMPIO 4 ***************


def richiede_utente_loggato(prossima_funz):
  def inner(e_loggato):
    if e_loggato:  
      print("sei loggato, puoi entrare!!")
      prossima_funz(e_loggato)
    else:
      print("mi dispiace, vatindi pa casa.")

  return inner



@richiede_utente_loggato
def gestisci_pagina_home(e_loggato):
  print("io sono loggatto, quindi sono entrato muahahaha!")


gestisci_pagina_home(True)
gestisci_pagina_home(False)

