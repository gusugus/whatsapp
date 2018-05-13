#encoding: utf-8
#https://github.com/sukiweb/CreandoUnChatbotEnPython/blob/master/Creando_un_bot_experto_en_Cruceros.ipynb

from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import ListTrainer
import logging
import sys, select
reload(sys)  
sys.setdefaultencoding('utf-8')

DEFAULT_RESPONSE = 'Disculpa, no he entendido lo que ha querido decir. Puede replantearlo.'
class Bott:
	
	logging.basicConfig(filename='myapp.log', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
	logger=logging.getLogger(__name__)

	
	def quitaNoAlfaNum(self, texto):
		import re
		tmp = re.compile(r'\W+', re.UNICODE).split(texto)
		return ''.join(str(e+" ") for e in tmp)
	
	def __init__(self, nombre_db):
		self.nombre_db = self.quitaNoAlfaNum(nombre_db)+"db"
		print "*"+self.nombre_db+"*"
		
		self.chatbot = ChatBot(
		    "Chat",

		    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
		    database_uri='mongodb://localhost:27017/',
		    database='chat_2',
		    
		    #TRAINING
		    trainer='chatterbot.trainers.ListTrainer',
		    #input_adapter="chatterbot.input.TerminalAdapter",
		    #output_adapter="chatterbot.output.TerminalAdapter",  
		    
		    logic_adapters=[
			{
			    "import_path": "chatterbot.logic.BestMatch",
			    "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
			    "response_selection_method": "chatterbot.response_selection.get_most_frequent_response"
			},
			
			{
			    'import_path': 'chatterbot.logic.LowConfidenceAdapter',
			    'threshold': 0.55,
			    'default_response': DEFAULT_RESPONSE
			},
			{
			    'import_path': 'chatterbot.logic.SpecificResponseAdapter',
			    'input_text': 'Quiero guardar una cita',
			    'output_text': 'Puede guardar una cita en http://google.com'
			},
		    ],
		    
		    preprocessors=[
			'chatterbot.preprocessors.clean_whitespace'
		    ],
		    
		    #read_only=True,
		)
		#DEFAULT_SESSION_ID = chatbot.default_conversation_id

		from chatterbot.trainers import ChatterBotCorpusTrainer

		self.chatbot.set_trainer(ChatterBotCorpusTrainer)
		self.chatbot.train("./cruises_es.yml")
		#conv = open('chats.txt','r').readlines()
		#self.train(conv)
		# Start by training our bot with the ChatterBot corpus data
		self.chatbot.train('chatterbot.corpus.english')
		self.chatbot.train('chatterbot.corpus.spanish')

	'''
	conversation = [
	"Hello",
	"Hi there!",
	"How are you doing?",
	"I'm doing great.",
	"That is good to hear",
	"Thank you.",
	"You're welcome."
	]

	chatbot.set_trainer(ListTrainer)
	chatbot.train(conversation)
	'''
	#request = raw_input("Escriba su pregunta: ")
	'''
	response = chatbot.get_response(None)
	response = u' '.join((response.text, '')).encode('utf-8').strip()
	imprimir 'Bot: '+response
	'''


	#ORIGINAL
	def responder(self, pregunta):
                #mandan en espanol
                pregunta_tmp = pregunta
                try:
                        #print("Estoy traduciendo al ingles")
                        from translate import Translator
                        translator= Translator(to_lang="en")
                        pregunta = translator.translate(pregunta_tmp) #pregunta en ingles
                except:
                        #Si hay error en la traduccion
                        print "Error en traduccion al ingles"
                        pregunta = pregunta_tmp
                #Si no hay traduccion, mando la pregunta en espanol
                if pregunta == "":
                        pregunta = pregunta_tmp
                
                
                
		if pregunta == DEFAULT_RESPONSE:
			response = ""
		#imprimir("Pregunta..."+pregunta)
		#imprimir("Estamos en chatbot")
		#pregunta = pregunta.replace('á','&atilde;').replace('é','&etilde;').replace('í','&itilde;').replace('ó','&otilde;').replace('ú','&utilde;').replace('ñ','&ntilde;')
		pregunta= u' '.join((pregunta, '')).encode('utf-8').strip()
                #print("Tengo la respuesta")
		response = self.chatbot.get_response(pregunta)
		response = response.text.replace('&atilde;','á').replace('&etilde;','é').replace('&itilde;','í').replace('&otilde;','ó').replace('&utilde;','ú').replace('&ntilde;','ñ')
		#response = response.encode("utf-8",'replace')
                response_tmp = response
                #SI LA RESPUESTA ES EN INGLES, LA TRADUZCO....
		#SI ES ESPANOL, ME DEVUELVE LO MISMO
		try:
                        #print("Estoy traduciendo al espanhol")
                        from translate import Translator
                        translator= Translator(to_lang="es")
                        response = translator.translate(response) # la respuesta es el ingles
                except:
                        #Si hay error en la traduccion
                        print "Error en traduccion a español"
                        response = response_tmp
		response = u' '.join((response, '')).decode('utf-8').strip()
		#imprimir response


		#print("Estoy por enviar la respuesta: "+response)
		return response
	
	#drop database....
	#mongo chat_2 --eval "db.dropDatabase()"

	#entrenando 
	#http://chatterbot.readthedocs.io/en/stable/examples.html


	#pregunta = raw_input("Ingrese su respuesta y luego su pregunta\n ")
	#response = chatbot.get_response("Si, como todos")
	#imprimir "Su respuesta:"+response
	'''
	while True:
		pregunta = raw_input("Human: ")
		response = responder(pregunta)
		imprimir "Bot: "+response
	'''
	#CONVERSATION_ID = self.chatbot.storage.create_conversation()

	#training
	#HUMAN:BOT
	def training(self, input_):
		#FIJARSE EN FUNCIONES->ENVIAR_MENSAJE
		tmp = input_.split("kkk")
		human = tmp[0]
		bot = tmp[1]
		
		human_ = Statement(human)
		#statement, response = chatbot.generate_response(input_statement, CONVERSATION_ID)
		bot_ = Statement(bot)
		self.chatbot.learn_response(bot_, human_)
		#chatbot.storage.add_to_conversation(CONVERSATION_ID, statement, response1)
		exists = self.chatbot.storage.find(bot_.text)
		print("Human: "+human_.text)
		print("Bot: "+bot_.text)
		return "Aprendido: "+exists.text

        def trainWhats(self, input_):
                print "Training alone whatsapp"

