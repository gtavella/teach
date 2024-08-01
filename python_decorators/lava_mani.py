
def chiama_lucia():
  pass

def facciamo_la_pizza():
  pass

def lavati_le_mani():
  pass


# DECORATORE (QUELLO VERO)

def assicurati_di_lavare_mani1(fai_qualcosa):
  def nuovo_fai_qualcosa():
    # prima di fare qualcosa, 
    # mi lavo le mani 
    lavati_le_mani()
    # fai_qualcosa in questo caso e' mangia
    fai_qualcosa()
  return nuovo_fai_qualcosa
    

def mangia1():
  # visto che ho gia' lavato le mani,
  # ora posso mangiare come un.. gran signore 
  chiama_lucia() 
  facciamo_la_pizza() 


mangia1 = assicurati_di_lavare_mani1(mangia1)



# DECORATORE (ZUCCHERO SINTATTICO)

def assicurati_di_lavare_mani2(fai_qualcosa):
  def nuovo_fai_qualcosa():
    # prima di fare qualcosa, 
    # mi lavo le mani 
    lavati_le_mani()
    # fai_qualcosa in questo caso e' mangia
    fai_qualcosa()
  return nuovo_fai_qualcosa
    

@assicurati_di_lavare_mani2
def mangia2():
  # visto che ho gia' lavato le mani,
  # ora posso mangiare come un.. gran signore 
  chiama_lucia() 
  facciamo_la_pizza() 


# ****************



