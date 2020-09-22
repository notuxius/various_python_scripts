# импорт модуля для работы с XML
# не секьюрный https://docs.python.org/3/library/xml.html#xml-vulnerabilities
import xml.etree.ElementTree as XmlElementTree
# импорт HTTP клиента
import httplib2
# генерация уникальных идентификаторов
import uuid
# работа с конфигурацией
from config import ***

# задаём константу хоста
***_HOST = '***'
# путь
***_PATH = '/***_xml'
# размер блока
CHUNK_SIZE = 1024 ** 2

# функция перевода аудио в текст, выглядит долгой, лучше разделить на больше функций
# параметры: имя файла - по умолчанию ничего, биты - по умолчанию ничего, ID запроса - шестнадцатиричный вид уникального идентификатора,
# тема - по умолчанию notes, язык - русский, ключ - константа API ключа - нигде не задана
def speech_to_text(filename=None, bytes=None, request_id=uuid.uuid4().hex, topic='notes', lang='ru-RU',
               	key=***_API_KEY):

# если задано имя файла
	if filename:
		# отрываем файл для чтения в байтовом режиме. автоматически закрываем его
    	with open(filename, 'br') as file:
			# читаем байты из файла и назначаем их в переменную bytes
        	bytes = file.read()
	# если переменная bytes не назначена
	if not bytes:
		# поднимаем общее ислючение с текстом что не предоставлено имя файла
		# или байты - но лучше написать что нельзя прочитать файл
    	raise Exception('Neither file name nor bytes provided.')

	# когда гуглил эту часть - нашёл вот это) 
	# https://webcache.googleusercontent.com/search?q=cache:JLF1BlxTSiAJ:https://qna.habr.com/q/828139+&cd=1&hl=en&ct=clnk&gl=ua
	# переназначаем переменную bytes результатом конвертации содержимого переменной bytes в Pulse-code modulation
	# который в свою очередь предназначен для перевода аналового сигнала в цыфровой - согласно википедии, что странно
	# 16бит, частота дискретизации 16000Hz, convert_to_pcm16b16000r - нигде не задан - может в config?
	bytes = convert_to_pcm16b16000r(in_bytes=bytes)

	# конкатенация константы пути и форматированной строки с ID запроса, ключа, темы и языка
	url = ***_PATH + '?uuid=%s&key=%s&topic=%s&lang=%s' % (
    	request_id,
    	key,
    	topic,
    	lang
	)

	# читаем блоки из bytes в переменную chunks с размером блока заданным ранее
	# read_chunks - нигде не задан
	chunks = read_chunks(CHUNK_SIZE, bytes)

	# создаём HTTP соединение с хостом без времени ожидания
	connection = httplib2.HTTPConnectionWithTimeout(***_HOST)
	# присоединяемся к хосту
	connection.connect()
	# создаём пост запрос на URL
	connection.putrequest('POST', url)
	# добавляем заголовок в запрос с именем Transfer-Encoding и значение chunked
	# он используется для того, чтобы реципиент не ждал весь объём данных в запросе
	# а сразу работал с блоками данных  
	connection.putheader('Transfer-Encoding', 'chunked')
	# задаём тип содержимого
	connection.putheader('Content-Type', 'audio/x-pcm;bit=16;rate=16000')
	# задаём конец заголовков, скорее всего пустой строкой
	connection.endheaders()

	# для каждого блока из переменной bytes
	for chunk in chunks:
		# отправляем закодированные первые два значения длинны блока в шестнадцатиричном формате с новой строкой
    	connection.send(('%s\r\n' % hex(len(chunk))[2:]).encode())
		# отправляем блок
    	connection.send(chunk)
		# отправляем закодированную новую строку
    	connection.send('\r\n'.encode())
	# отправляем закодированный 0 и две новых закодированные строки
	connection.send('0\r\n\r\n'.encode())
	# получаем ответ после запроса
	response = connection.getresponse()

	# если ответ ОК
	if response.code == 200:
		# читаем текст ответа
    	response_text = response.read()
		# создаём XML из ответа
    	xml = XmlElementTree.fromstring(response_text)
		# если цифровое значения аттрибута success в XML это 1 
    	if int(xml.attrib['success']) == 1:
			# назначаем максимальное достоверие как минус бесконечность, в примерах чаще видел float("-inf") 
        	max_confidence = - float("inf")
			# инициализируем пустую переменную
        	text = ''
			# для каждого элемента в XML
        	for child in xml:
				# если аттрибут confidence элемента в значении числа с плавающей точкой больше чем макс достоверие
            	if float(child.attrib['confidence']) > max_confidence:
					# задаём текст этого элемента в переменную текст
                	text = child.text
					# переназначаем максимальное достоверие значением аттрибута confidence элемента в значении числа с плавающей точкой
                	max_confidence = float(child.attrib['confidence'])
	
			# если максимальное достоверие переназначено и не минус бесконечность
	        if max_confidence != - float("inf"):
				# возращаем текст элемента
            	return text
			# если максимальное достоверие не переназначено и минус бесконечность
        	else:
            	# поднимаем ислючение что текст не найден и форматированный текст ответа, разделённые новыми строками
            	raise SpeechException('No text found.\n\nResponse:\n%s' % (response_text))
		# если цифровое значения аттрибута success в XML это не 1 
    	else:
			# поднимаем ислючение речи что текст не найден и форматированный текст ответа, разделённые новыми строками
        	raise SpeechException('No text found.\n\nResponse:\n%s' % (response_text))
	# если ответ не ОК
	else:
		# поднимаем ислючение речи с неизвестной ошибкой и форматированный код и текст ответа, разделённые новыми строками
		# эта часть кода повторяется
    	raise SpeechException('Unknown error.\nCode: %s\n\n%s' % (response.code, response.read()))

# создаём класс ислючения речи, унаследованный от общего исключения
# его необходимо задать перед функцией speech_to_text
# здесь буква "с" в слове "сlass" написанна по русски
class SpeechException(Exception):
	pass
