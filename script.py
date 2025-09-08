from pathlib import Path
from datetime import datetime, timedelta
import shutil

DIR_ORIGIN = Path('home/valcann/backupsFrom')
DIR_DESTINATION = Path('home/valcann/backupsTo')
LOG_ORIGIN = Path('home/valcann/backupsFrom.log')
LOG_DESTINATION = Path('home/valcann/backupsTo.log')

DATE_LIMIT = datetime.now() - timedelta(days=3)

DIR_ORIGIN.mkdir(exist_ok=True, parents=True)
DIR_DESTINATION.mkdir(exist_ok=True, parents=True)

with LOG_ORIGIN.open('a') as log:
  log.write('Informações dos arquivos em home/valcann/backupsFrom:\n')
  for file in DIR_ORIGIN.iterdir():
    if file.is_file():
      stat = file.stat()

      name = file.name
      size = stat.st_size
      creation_date = datetime.fromtimestamp(stat.st_ctime)
      modify_date = datetime.fromtimestamp(stat.st_mtime)
      log.write(f'Nome: {name} - Tamanho: {size} bytes - Data de criação: {creation_date} - Data de moficação: {modify_date} \n')
  log.write('\n')
print(f'Informações LISTADAS em {LOG_ORIGIN}')

with LOG_DESTINATION.open('a') as log:
  log.write('Arquivos DELETADOS de home/valcann/backupsFrom:\n')
  for file in DIR_ORIGIN.iterdir():
    date = datetime.fromtimestamp(file.stat().st_ctime)
    if file.is_file() and date < DATE_LIMIT:
      log.write(f'Nome: {file.name} \n')
      file.unlink()
  log.write('\n')
print(f'Nome dos arquivos DELETADOS em {LOG_DESTINATION}')

with LOG_DESTINATION.open('a') as log:
  log.write('Arquivos MOVIDOS de home/valcann/backupsFrom:\n')
  for file in DIR_ORIGIN.iterdir():
    date = datetime.fromtimestamp(file.stat().st_ctime)
    if file.is_file() and date >= DATE_LIMIT:
      detiny_path = DIR_DESTINATION / file.name
      log.write(f'Nome: {file.name} \n')
      shutil.copy2(file, detiny_path)
      file.unlink()
  log.write('\n')
print(f'Nome dos arquivos MOVIDOS em {LOG_DESTINATION}')