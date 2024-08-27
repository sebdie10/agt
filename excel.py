from openpyxl import Workbook


def Crear_Excel(informacion):
  print(informacion)

  book = Workbook()

  hoja = book.active
  #informacion = eval(informacion)

  hoja['A1'] = 'Tipo'
  hoja['B1'] = 'Marca'
  hoja['C1'] = 'Modelo'
  hoja['D1'] = 'Nº Serie'
  hoja['E1'] = 'Stock'
  hoja['F1'] = 'Ubicacion'

  t = 1
  n = 0

  for dato in informacion:
    print(dato)
    t += 1
    hoja[f'A{t}'] = dato[1]
    hoja[f'B{t}'] = dato[2]
    hoja[f'C{t}'] = dato[3]
    hoja[f'D{t}'] = dato[4]
    hoja[f'E{t}'] = dato[5]
    hoja[f'F{t}'] = dato[6]
  book.save('InventarioGC.xlsx')
