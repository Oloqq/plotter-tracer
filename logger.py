from datetime import datetime
import io

path = 'logs/'+datetime.now().strftime('%d.%m.%Y %H-%M-%S')+'.txt'
log_file = io.open(path, 'w', encoding='utf-8')
latest_log = io.open('latest_log.txt', 'w', encoding='utf-8')

def log(*args, console=False):
	if console:
		print(*args)
		
	for arg in args:
		arg = str(arg)
		log_file.write(arg + ' ')
		latest_log.write(arg + ' ')
	log_file.write('\n')
	latest_log.write('\n')
	
	