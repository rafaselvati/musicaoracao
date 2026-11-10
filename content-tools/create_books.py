from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, Color, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER
import math, shutil, json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'private_files'
for name,file in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Serif','DejaVuSerif.ttf'),('Italic','DejaVuSerif-Italic.ttf')]:pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
W,H=420,595
GOLD=HexColor('#a67913');INK=HexColor('#292a23');MUTED=HexColor('#626357');CREAM=HexColor('#fffdf6')
styles={'body':ParagraphStyle('body',fontName='Body',fontSize=10,leading=16,textColor=INK,spaceAfter=12), 'small':ParagraphStyle('small',fontName='Body',fontSize=8,leading=13,textColor=MUTED),'title':ParagraphStyle('title',fontName='Serif',fontSize=29,leading=34,textColor=INK,spaceAfter=20), 'sub':ParagraphStyle('sub',fontName='Serif',fontSize=17,leading=23,textColor=GOLD,spaceAfter=12),'quote':ParagraphStyle('quote',fontName='Italic',fontSize=15,leading=23,textColor=GOLD,spaceAfter=18)}
class Book:
 def __init__(self,file,title):
  self.file=OUT/file;self.title=title;self.c=canvas.Canvas(str(self.file),pagesize=(W,H));self.c.setTitle(title);self.c.setAuthor('Séptimo Sentido');self.page=0;self.y=0
 def base(self,label='SÉPTIMO SENTIDO'):
  if self.page:self.c.showPage()
  self.page+=1;c=self.c;c.setFillColor(CREAM);c.rect(0,0,W,H,fill=1,stroke=0);c.setStrokeColor(HexColor('#e2d7ba'));c.line(38,551,382,551);c.line(38,37,382,37);c.setFillColor(GOLD);c.setFont('Body',7);c.drawString(38,565,label.upper());c.setFillColor(MUTED);c.drawString(38,23,'LECTURA PERSONAL • EDICIÓN EN ESPAÑOL');c.drawRightString(382,23,str(self.page).zfill(2));self.y=524
 def text(self,txt,style='body',gap=0):
  obj=Paragraph(txt,styles[style]);_,h=obj.wrap(W-76,H)
  if self.y-h<55: raise ValueError(f'Overflow {self.title} p{self.page}: {txt[:60]} y={self.y} h={h}')
  obj.drawOn(self.c,38,self.y-h);self.y-=h+styles[style].spaceAfter+gap
 def titlepage(self,title,sub,label='EDICIÓN DIGITAL'):
  self.base(label);c=self.c;c.setFillColor(CREAM);c.rect(0,0,W,H,fill=1,stroke=0)
  c.saveState();c.setFillAlpha(.20);c.drawImage(str(ROOT/'assets/celestial.jpg'),0,0,width=H*1376/768,height=H,mask='auto');c.restoreState()
  c.setStrokeColor(GOLD);c.rect(23,23,W-46,H-46);c.rect(29,29,W-58,H-58);c.setFillColor(GOLD);star=c.beginPath();star.moveTo(210,478);star.lineTo(218,456);star.lineTo(240,448);star.lineTo(218,440);star.lineTo(210,418);star.lineTo(202,440);star.lineTo(180,448);star.lineTo(202,456);star.close();c.drawPath(star,fill=1,stroke=0);self.y=530;self.text(label,'small');self.y=390
  self.text(title,'title',15);self.text(sub,'sub');self.y=145;self.text('SÉPTIMO SENTIDO','small');self.text('Fe, reflexión y prácticas para caminar con propósito.','small')
 def pageof(self,label,title,paras):
  self.base(label);self.text(title,'title')
  for v in paras:
   if isinstance(v,tuple):self.text(v[1],v[0])
   else:self.text(v)
 def lines(self,n=5):
  for i in range(n):
   if self.y<65:break
   self.c.setStrokeColor(HexColor('#ded5bc'));self.c.line(38,self.y-13,382,self.y-13);self.y-=26
 def save(self):self.c.save();return self.page
chapters=[
{'title':'El silencio','subtitle':'Haz espacio antes de buscar respuestas','ref':'Lucas 10:38-42; Salmo 46:10','anchor':'El silencio no te obliga a encontrar una respuesta. Te permite reconocer qué pregunta necesitas hacer.',
'paras':[
'Una jornada espiritual puede comenzar con algo tan sencillo como dejar el teléfono a un lado. No para demostrar disciplina, sino para reconocer cuánto de tu atención se reparte entre pendientes, conversaciones y expectativas. Cuando todo exige una respuesta inmediata, incluso la oración puede convertirse en otra tarea por terminar.',
'Hacer silencio no significa dejar la mente en blanco. Es normal recordar algo pendiente, sentir aburrimiento o notar una emoción incómoda. La práctica consiste en reconocer lo que aparece y regresar con amabilidad al momento presente. No estás fallando porque te distraes; estás aprendiendo a volver.',
'En el relato de Marta y María hay una invitación a examinar cómo atendemos lo importante. El servicio tiene valor, pero la actividad constante también puede impedirnos escuchar. Lee el pasaje completo y observa qué te despierta, sin usarlo para juzgar tu ritmo de vida ni el de otras personas.'
],
'deeper':[
'El silencio también necesita límites concretos. No tiene que durar una hora ni ocurrir en un lugar perfecto. Una silla, cinco minutos disponibles y la decisión de no abrir otra pantalla pueden ser suficientes. Si tienes responsabilidades de cuidado, elige un momento realista en lugar de esperar una calma que quizá no llegue.',
'Prueba nombrar tu estado sin corregirlo: hoy estoy cansado; hoy tengo esperanza; hoy estoy preocupado. Después formula una pregunta sencilla ante Dios. Evita forzar una interpretación de cada pensamiento. Puedes terminar la práctica sin una conclusión y aun así haber prestado atención a tu vida.',
'La pregunta que queda abierta merece respeto. Anótala y vuelve a ella otro día. Algunas respuestas requieren conversación, información o tiempo. Una pausa puede ayudarte a reconocer ese siguiente paso, pero no sustituye lo que todavía necesitas hacer.'
],
'practice':[('Preparar','Elige cinco minutos y silencia las notificaciones. Siéntate de una manera cómoda y permite que tu respiración siga su ritmo natural.'),('Reconocer','Escribe tres palabras que describan tu estado. No las conviertas en un diagnóstico ni en una explicación definitiva.'),('Preguntar','Completa: «Dios, hoy quiero hablar contigo sobre…». Escribe libremente durante dos minutos.'),('Cerrar','Elige una acción pequeña para cuidar lo que apareció: descansar, conversar, ordenar un pendiente o pedir ayuda.')],
'prayer':'Dios, aquí está mi vida tal como es hoy. Ayúdame a no huir de mis preguntas ni a exigir respuestas inmediatas. Enséñame a escuchar con humildad y a reconocer el siguiente paso que puedo dar con responsabilidad. Amén.',
'question':'¿Qué suelo hacer para evitar quedarme a solas con mis pensamientos?','action':'Reserva un momento breve para mañana y anótalo en tu agenda.'},
{'title':'El discernimiento','subtitle':'Distingue entre hechos, deseos y decisiones','ref':'Santiago 1:5; Proverbios 15:22','anchor':'Una impresión puede iniciar una reflexión; no tiene que convertirse de inmediato en una certeza.',
'paras':[
'Cuando algo nos importa mucho, es fácil buscar una confirmación en todo lo que ocurre. Una frase, una coincidencia o una emoción intensa pueden parecer respuestas definitivas. Discernir es hacer espacio entre lo que observas y el significado que le atribuyes. Ese espacio permite decidir con más cuidado.',
'La fe no exige renunciar a las preguntas. Puedes orar y revisar información, pedir consejo y reconocer que todavía no sabes. En Santiago, la petición de sabiduría abre una relación de confianza; no transforma al lector en alguien incapaz de equivocarse. La humildad forma parte del camino.',
'Empieza por separar tres niveles: el hecho comprobable, tu interpretación y la acción que estás considerando. Por ejemplo: alguien no respondió un mensaje es un hecho; ya no me valora es una interpretación; enviar diez mensajes más es una posible acción. Separarlos ayuda a no convertir una suposición en el centro de la decisión.'
],
'deeper':[
'El discernimiento madura cuando acepta otras perspectivas. Busca a alguien que pueda escucharte sin decidir por ti, que conozca el tema y que no necesite confirmar todo lo que piensas. Un consejo útil puede ser incómodo; no por eso es una amenaza para tu fe.',
'Una decisión también debe mirar sus consecuencias. Pregunta a quién afecta, qué recursos requiere y qué ocurriría si te equivocaras. Si hay urgencia artificial, miedo o presión para actuar sin comprender, toma distancia. Las decisiones importantes merecen información y tiempo cuando las circunstancias lo permiten.',
'No toda tranquilidad confirma una elección ni toda incomodidad la invalida. A veces lo responsable cuesta; otras veces una idea atractiva nos distrae de un límite. Observa la coherencia entre tus valores, los hechos y tus actos. Puedes revisar una decisión cuando aparece información nueva.'
],
'practice':[('Nombrar','Escribe una decisión concreta. Evita preguntas tan amplias como «¿qué hago con toda mi vida?».'),('Separar','Divide una hoja en hechos, interpretaciones y opciones. Escribe al menos dos interpretaciones posibles.'),('Consultar','Identifica un dato que te falta y una persona competente a quien puedas preguntar.'),('Elegir','Define un paso reversible y una fecha para revisar lo aprendido antes de comprometerte más.')],
'prayer':'Dios de sabiduría, ayúdame a reconocer lo que sé y lo que todavía supongo. Dame humildad para escuchar, valentía para preguntar y paciencia para decidir sin entregarme al miedo. Que mi fe acompañe mi responsabilidad. Amén.',
'question':'¿Qué evidencia podría hacerme cambiar de opinión?','action':'Consulta una fuente confiable o pide una segunda perspectiva antes de decidir.'},
{'title':'Tu identidad','subtitle':'Tu valor no depende de la aprobación','ref':'Efesios 2:10; Romanos 12:3-8','anchor':'Reconocer tu dignidad no requiere colocarte por encima de nadie.',
'paras':[
'La necesidad de pertenecer puede llevarnos a interpretar cada desacuerdo como una prueba de nuestro valor. Quizá aprendiste a agradar, a destacar o a ocultar partes de ti para sentirte aceptado. Mirar esos hábitos con honestidad permite reconocer qué te ayuda y qué te aleja de tus convicciones.',
'En este libro, la palabra elegido se usa como una invitación a vivir la fe con responsabilidad, amor y servicio. No describe una categoría de personas superiores ni permite concluir que quienes discrepan contigo te envidian. La dignidad que reconoces en ti también pertenece a los demás.',
'Las cartas de Pablo relacionan la vida espiritual con dones diferentes y una comunidad en la que nadie lo hace todo. Lee los pasajes sugeridos prestando atención a la humildad y al servicio. Una identidad arraigada en la fe no necesita convertir cada encuentro en una comparación.'
],
'deeper':[
'Puedes empezar distinguiendo quién eres de los papeles que desempeñas. Tu empleo, tus logros y tus responsabilidades dicen algo de tu historia, pero no la agotan. Si una etapa cambia, tus valores pueden seguir orientándote mientras construyes una nueva manera de vivirlos.',
'Reconocer fortalezas no significa negar límites. Tal vez escuchas con atención y te cuesta decir que no; quizá eres perseverante, pero necesitas aprender a descansar. Escribir ambas cosas en la misma página evita la exigencia de ser perfecto para merecer respeto.',
'Cuando aparezca una crítica, intenta separar su contenido de su tono. Puedes recoger una observación útil sin aceptar un trato humillante. También puedes reconocer un error sin convertirlo en una sentencia sobre toda tu persona. La identidad madura puede aprender y poner límites al mismo tiempo.'
],
'practice':[('Reconocer','Anota tres valores que quieras vivir. Acompaña cada uno con una conducta observable.'),('Distinguir','Escribe una etiqueta que te pesa. Describe un hecho concreto que esa etiqueta no alcanza a explicar.'),('Equilibrar','Nombra una fortaleza y una habilidad que necesitas practicar. Ninguna define por completo tu valor.'),('Servir','Elige un gesto de ayuda discreto que puedas realizar sin esperar reconocimiento.')],
'prayer':'Dios, ayúdame a recordar mi dignidad sin olvidar la de quienes me rodean. Que no dependa de la aprobación para actuar con amor, ni del orgullo para sostenerme. Enséñame a reconocer mis dones y a ofrecerlos con humildad. Amén.',
'question':'¿Cómo actuaría hoy si no necesitara impresionar a nadie?','action':'Practica un valor en una situación pequeña, sin publicarlo ni pedir reconocimiento.'},
{'title':'La fe','subtitle':'Camina sin exigir control total','ref':'Marcos 9:24; Mateo 6:25-34','anchor':'La confianza puede convivir con preguntas sinceras.',
'paras':[
'A veces imaginamos que tener fe significa sentir seguridad todo el tiempo. Cuando aparece la duda, podemos ocultarla por vergüenza o intentar llenarla de frases que no reflejan nuestro estado real. Pero una relación espiritual honesta también puede contener cansancio, preguntas y peticiones incompletas.',
'En Marcos encontramos una petición que reconoce al mismo tiempo confianza y dificultad para confiar. Lee la escena completa. Su fuerza está en la honestidad, no en una fórmula para obtener cualquier resultado. Puedes llevar a la oración aquello que todavía no sabes resolver.',
'La confianza tampoco elimina la responsabilidad cotidiana. Esperar no impide buscar trabajo, atender una conversación, consultar a un profesional o revisar tus recursos. Una vida de fe puede sostener esos actos sin prometer que todo ocurrirá según tu preferencia.'
],
'deeper':[
'Para practicar esta llave, distingue lo que puedes hacer hoy de lo que no puedes controlar. Puedes preparar una conversación, pero no elegir la respuesta de la otra persona. Puedes cumplir una tarea, pero no controlar todas sus consecuencias. Reconocer el límite evita pedirte lo imposible.',
'La gratitud puede acompañar este proceso si no se usa para negar el dolor. Agradecer una presencia, una comida o una oportunidad no obliga a llamar bueno a lo que te lastimó. Hay espacio para reconocer lo recibido y lamentar lo perdido.',
'En momentos difíciles, permite que la confianza también pase por otras personas. Pedir compañía, consejo o ayuda práctica no disminuye tu vida espiritual. A veces el siguiente paso consiste en dejar de llevar a solas una carga que necesita apoyo.'
],
'practice':[('Ordenar','Divide una hoja en «me corresponde» y «no depende de mí». Escribe una situación actual en ambas columnas.'),('Actuar','Elige una tarea de la primera columna que puedas completar en veinte minutos o menos.'),('Entregar','Lleva una preocupación de la segunda columna a la oración, sin convertirla en una promesa de resultado.'),('Acompañarte','Identifica a una persona a quien puedas pedir apoyo concreto durante esta semana.')],
'prayer':'Dios, acompáñame en lo que no comprendo. Dame fuerza para hacer lo que me corresponde y humildad para reconocer mis límites. Que la incertidumbre no me impida actuar con cuidado ni recibir la ayuda que necesito. Amén.',
'question':'¿Qué intento controlar que en realidad necesita paciencia o colaboración?','action':'Completa un paso responsable y deja por escrito lo que hoy no puedes resolver.'},
{'title':'El perdón','subtitle':'Reconoce la herida sin abandonar tus límites','ref':'Colosenses 3:12-15; Romanos 12:18','anchor':'Perdonar no te obliga a restaurar una relación insegura.',
'paras':[
'Las heridas no desaparecen por repetir una frase espiritual. Una experiencia dolorosa puede necesitar tiempo, palabras y apoyo antes de que sea posible mirarla con mayor claridad. Esta llave no te pide borrar lo ocurrido ni sentir algo para lo que todavía no estás preparado.',
'El perdón, la reconciliación y la confianza son procesos distintos. Puedes trabajar en no vivir dominado por el resentimiento sin volver a una relación dañina. La reconciliación requiere participación de las personas involucradas; la confianza necesita comportamientos consistentes, no solo una disculpa.',
'La invitación bíblica a buscar la paz no exige aceptar cualquier trato. Romanos reconoce un límite al hablar de lo que depende de cada persona. Lee ese contexto con cuidado: responsabilizarte de tus acciones no significa asumir la responsabilidad por los actos de los demás.'
],
'deeper':[
'Empieza nombrando lo que pasó con palabras concretas. En lugar de «todo está arruinado», describe la conducta que te hirió y cómo te afectó. Esto no reduce la gravedad de la experiencia; te ayuda a reconocer qué necesitas ahora.',
'Un límite puede ser una conversación, un cambio de horario, una distancia o la decisión de no participar en ciertos intercambios. Conviene que sea claro y practicable. No es una herramienta para controlar a la otra persona, sino una forma de definir qué harás para cuidarte.',
'También puedes necesitar pedir perdón. Reconoce tu acción, evita justificarla con lo que hizo el otro y ofrece una reparación posible. La otra persona tiene derecho a necesitar tiempo o a no retomar el vínculo. Si hay violencia o riesgo, prioriza tu seguridad y busca apoyo adecuado; no fuerces un encuentro.'
],
'practice':[('Nombrar','Describe una herida que puedas explorar sin desbordarte. Puedes detener la práctica en cualquier momento.'),('Diferenciar','Escribe qué necesitas soltar y qué límite necesitas conservar. No tienen que ser lo mismo.'),('Cuidar','Redacta una frase de límite: «Si ocurre…, voy a…». Elige una acción que dependa de ti.'),('Reparar','Si te corresponde reparar algo, identifica una acción concreta. No exijas perdón como recompensa.')],
'prayer':'Dios, recibe lo que todavía duele. Ayúdame a buscar paz sin negar la verdad, a poner límites sin crueldad y a reconocer mis propias responsabilidades. Dame compañía y paciencia para recorrer este proceso sin forzarme. Amén.',
'question':'¿Estoy confundiendo perdonar con permitir que todo siga igual?','action':'Escribe un límite respetuoso o una reparación posible y decide cuándo ponerla en práctica.'},
{'title':'El propósito','subtitle':'Encuentra dirección en lo cotidiano','ref':'Miqueas 6:8; Mateo 5:13-16','anchor':'Tu propósito también puede expresarse en lo pequeño y repetido.',
'paras':[
'La palabra propósito puede parecer enorme, como si existiera una misión secreta que debieras descubrir antes de empezar a vivir. Esa expectativa puede paralizarte. A veces la dirección aparece al observar qué valores quieres cuidar y qué necesidades reales están a tu alcance.',
'El lenguaje bíblico sobre justicia, misericordia y humildad acerca la vida espiritual a las relaciones concretas. No se limita a una emoción privada. Pregunta cómo se reflejan esos valores en tu manera de trabajar, escuchar, administrar tus recursos y tratar a quien no puede ofrecerte nada a cambio.',
'No necesitas convertir cada talento en un negocio ni cada experiencia difícil en una gran misión. Algunas capacidades sirven para sostener una familia, acompañar a alguien o mejorar una tarea. Su valor no depende de que sean visibles para muchas personas.'
],
'deeper':[
'Explora tres preguntas: qué te importa, qué puedes ofrecer y qué necesita tu entorno. Busca una intersección pequeña. Si te importa el aprendizaje, sabes explicar con paciencia y conoces a alguien que necesita apoyo, puedes comenzar con una conversación o una sesión breve.',
'El propósito también debe respetar tus límites. No tienes que aceptar todas las solicitudes para ser una persona generosa. El servicio que ignora tus recursos puede agotarte y terminar en resentimiento. Define una medida de tiempo y energía que puedas sostener.',
'Revisa lo que haces sin exigir resultados extraordinarios. Pregunta si fue útil, si estuvo alineado con tus valores y qué cambiarías la próxima vez. La dirección se vuelve más clara cuando dialogan la reflexión y la experiencia. Puedes modificar el camino sin considerar perdido lo aprendido.'
],
'practice':[('Explorar','Escribe un valor, una habilidad y una necesidad cercana. Usa ejemplos de tu vida actual.'),('Conectar','Diseña una acción que reúna los tres elementos y que puedas realizar esta semana.'),('Delimitar','Define cuánto tiempo dedicarás y qué no puedes asumir por ahora.'),('Revisar','Después de actuar, anota qué fue útil, qué te costó y cuál sería un siguiente paso realista.')],
'prayer':'Dios, abre mis ojos a las oportunidades de amar que están cerca. Ayúdame a ofrecer lo que tengo sin despreciar lo pequeño ni prometer lo que no puedo sostener. Que mi propósito se vuelva visible en acciones honestas. Amén.',
'question':'¿Qué necesidad concreta puedo atender sin esperar a sentirme completamente preparado?','action':'Agenda un gesto de servicio pequeño con un límite claro de tiempo.'},
{'title':'La acción','subtitle':'Convierte la reflexión en una práctica sostenible','ref':'Santiago 1:22-25; Gálatas 6:9','anchor':'Un paso posible tiene más fuerza que una promesa imposible de sostener.',
'paras':[
'Leer puede inspirar, pero la inspiración cambia de intensidad. Si tu práctica depende de sentir entusiasmo cada mañana, será difícil mantenerla en los días comunes. Esta última llave propone traducir lo aprendido en una conducta concreta, pequeña y repetible.',
'Una intención como «voy a vivir con más fe» puede orientarte, pero necesita una forma observable. «Después del desayuno, dedicaré cinco minutos a leer y escribir una pregunta» te permite saber qué harás, cuándo y durante cuánto tiempo. La precisión reduce las decisiones que debes tomar al empezar.',
'La invitación de Santiago a poner en práctica lo escuchado no exige hacer todo a la vez. Puede comenzar con una respuesta menos impulsiva, un límite claro o un gesto de servicio. El propósito del hábito es acompañar tu vida, no convertirse en una nueva manera de castigarte.'
],
'deeper':[
'Escoge una señal cotidiana que ya exista: tomar agua, terminar el desayuno o apagar la computadora. Coloca junto a ella la práctica breve que quieres incorporar. Prepara el material de antemano para no depender de encontrarlo cuando llegue el momento.',
'Diseña también una versión mínima. Si no puedes dedicar quince minutos, quizá puedas escribir una línea o hacer una oración breve. Esa flexibilidad no resta valor al proceso; permite adaptarlo a jornadas distintas. Si necesitas descansar, puedes retomar sin convertir la pausa en una deuda.',
'Revisa el hábito con curiosidad. En lugar de preguntar «¿por qué no tengo disciplina?», pregunta qué obstáculo apareció y cómo podrías ajustar el entorno. Cambia el horario, reduce la duración o pide compañía. Observa conductas y aprendizajes, no supuestas pruebas de superioridad espiritual.'
],
'practice':[('Elegir','Selecciona una sola práctica de las seis llaves anteriores. Define la versión de cinco minutos.'),('Vincular','Completa: «Después de…, voy a… durante…». Elige una señal que ocurra con frecuencia.'),('Preparar','Deja disponible el libro, el diario o el lugar que usarás. Reduce una distracción previsible.'),('Revisar','Fija una revisión dentro de siete días. Registra qué funcionó y modifica una sola cosa.')],
'prayer':'Dios, ayúdame a vivir lo que comprendo sin exigirme perfección. Dame constancia para los pasos pequeños y humildad para volver a empezar. Que mi crecimiento se refleje en el cuidado, la verdad y el amor con que actúo. Amén.',
'question':'¿Cuál es la versión más pequeña de la práctica que sí puedo sostener?','action':'Realiza tu primera práctica hoy y fija una fecha breve de revisión.'}
]
book=Book('Desbloquea_Tu_Septimo_Sentido.pdf','Desbloquea Tu Séptimo Sentido')
book.titlepage('Desbloquea Tu<br/>Séptimo Sentido','Siete llaves para una vida espiritual con propósito','EL DESPERTAR DEL ELEGIDO')
book.pageof('Bienvenida','La puerta de entrada',[
'Este libro es una invitación a mirar tu vida con atención y a cultivar tu relación con Dios mediante la reflexión, la oración y la acción. No necesitas conocimientos previos ni una historia espiritual perfecta para comenzar.',
'El «séptimo sentido» es la metáfora que organiza el recorrido: una manera de prestar atención a tu interior y discernir cómo quieres vivir. No es un sentido biológico, una técnica para adivinar acontecimientos ni una promesa de poderes sobrenaturales.',
'La expresión «elegido» apunta aquí a una vocación de amor, humildad y servicio. No te coloca por encima de otros ni convierte las críticas, las coincidencias o las dificultades en pruebas de una condición especial.',
'La propuesta principal está completa en estas páginas. Los materiales complementarios ofrecen otras formas de practicar; no son necesarios para comprender las siete llaves ni para iniciar tu camino.',
('quote','Puedes leer con preguntas. Puedes avanzar con pausas. Puedes volver a empezar.')])
book.pageof('Guía de lectura','Cómo usar este libro',[
'Cada llave incluye una reflexión, una lectura bíblica sugerida, una práctica y una oración original. Lee el pasaje bíblico completo en la traducción que utilices habitualmente: las reflexiones de este libro no son citas textuales de la Biblia.',
'Primero lee la reflexión. Después elige una sola pregunta y escribe una respuesta honesta. Termina con una acción pequeña. Es preferible aplicar una idea concreta que completar todas las páginas con prisa.',
'Puedes dedicar tres días a cada llave: uno para leer, otro para practicar y otro para revisar. Al final encontrarás una ruta de 21 días. No es un plazo para garantizar un resultado; es una organización posible para acompañar la lectura.',
'El libro se enfoca en prácticas espirituales personales. No reemplaza atención médica, psicológica ni asesoría profesional. Si una actividad te causa un malestar intenso, puedes detenerte y buscar acompañamiento adecuado.',
('sub','Tu punto de partida'),
'Completa en tu cuaderno: «Hoy me gustaría cuidar…». Escribe una intención que dependa de tus actos, no de cambiar a otra persona.'])
book.pageof('Contenido','Las siete llaves',[( 'sub',f'{i+1:02d} · {d["title"]}') for i,d in enumerate(chapters)]+[('small','Después de las siete llaves: ruta de 21 días, revisión personal y lecturas bíblicas para continuar.')])
for i,d in enumerate(chapters):
 book.pageof(f'Llave {i+1:02d} · Reflexión',d['title'],[('sub',d['subtitle'])]+d['paras'])
 book.pageof(f'Llave {i+1:02d} · Profundizar','Llévalo a tu vida',[('quote',d['anchor'])]+d['deeper'])
 book.pageof(f'Llave {i+1:02d} · Práctica','Un paso concreto',[( 'small','LECTURA BÍBLICA SUGERIDA: '+d['ref'])]+[f'<b>{j+1}. {t}.</b> {a}' for j,(t,a) in enumerate(d['practice'])]+[('sub','Una pregunta para escribir'),d['question']])
 book.pageof(f'Llave {i+1:02d} · Oración','Un momento con Dios',[('quote',d['prayer']),('sub','Tu compromiso de hoy'),d['action'],('sub','Observa sin juzgarte'),'Al terminar, describe lo que hiciste, lo que sentiste y lo que aprendiste. No necesitas demostrar una transformación extraordinaria. Un registro sencillo te ayudará a elegir cómo continuar.']);book.lines(3)
book.pageof('Ruta de aplicación','21 días, a tu ritmo',[
'Usa esta ruta como una invitación, no como una prueba. Puedes repetir un día, detenerte o extender el recorrido. No hay una clasificación de avance espiritual ni una promesa de cambio en un plazo fijo.',
'<b>Días 1-3 · Silencio.</b> Lee la primera llave; realiza una pausa breve; identifica qué distracción puedes reducir.',
'<b>Días 4-6 · Discernimiento.</b> Elige una decisión; separa hechos e interpretaciones; consulta lo que todavía no sabes.',
'<b>Días 7-9 · Identidad.</b> Reconoce tus valores; revisa una etiqueta; practica un gesto de servicio sin buscar aprobación.',
'<b>Días 10-12 · Fe.</b> Distingue responsabilidades y límites; realiza un paso concreto; pide apoyo si lo necesitas.',
'<b>Días 13-15 · Perdón.</b> Nombra una herida; identifica un límite; considera una reparación que dependa de ti.'])
book.pageof('Ruta de aplicación','Continúa con intención',[
'<b>Días 16-18 · Propósito.</b> Relaciona un valor, una habilidad y una necesidad. Realiza una acción pequeña y observa qué aprendiste.',
'<b>Días 19-21 · Acción.</b> Elige un hábito breve, vincúlalo con una rutina existente y prepara una revisión para la siguiente semana.',
('sub','Una revisión honesta'),
'¿Qué práctica pude realizar de manera concreta? ¿Qué cambió en una conversación o una decisión? ¿Qué sigue siendo difícil? ¿Necesito ajustar el ritmo o buscar compañía?',
'Evita comparar tu recorrido con el de otra persona. Puedes observar un progreso en acciones sencillas: pedir una aclaración antes de suponer, reservar un momento de oración o sostener un límite con respeto.',
('sub','Lo que viene después'),
'Conserva una sola práctica para la semana siguiente. Si quieres profundizar, vuelve a una llave y lee el pasaje bíblico en su contexto. El objetivo no es terminar rápido, sino integrar algo valioso en tu manera de vivir.'])
book.pageof('Para continuar','Lecturas y cierre',[
'<b>Silencio:</b> Lucas 10:38-42; Salmo 46:10.<br/><b>Discernimiento:</b> Santiago 1:5; Proverbios 15:22.<br/><b>Identidad:</b> Efesios 2:10; Romanos 12:3-8.<br/><b>Fe:</b> Marcos 9:24; Mateo 6:25-34.<br/><b>Perdón:</b> Colosenses 3:12-15; Romanos 12:18.<br/><b>Propósito:</b> Miqueas 6:8; Mateo 5:13-16.<br/><b>Acción:</b> Santiago 1:22-25; Gálatas 6:9.',
'Estas referencias orientan una lectura personal. Lee los pasajes completos y considera su contexto. Las explicaciones, preguntas y oraciones de esta edición son textos originales de reflexión; no se atribuyen a Dios ni a los autores bíblicos como citas literales.',
('quote','Tu próximo paso no necesita ser espectacular. Necesita ser tuyo, posible y coherente con el amor que quieres vivir.'),
'Edición digital para uso personal. © 2026 Séptimo Sentido. No se autoriza la reventa o distribución pública de estos materiales.'])
counts={book.file.name:book.save()}
# Diario con preguntas diferentes y espacio de escritura real.
diary=Book('Diario_del_Despertar.pdf','Diario del Despertar')
diary.titlepage('Diario del<br/>Despertar','21 espacios para escuchar, escribir y actuar','BONO 01 · INCLUIDO EN AMBAS EDICIONES')
diary.pageof('Antes de escribir','Este espacio es tuyo',[
'No necesitas escribir bonito ni llenar cada línea. Este diario acompaña las siete llaves del libro principal con tres momentos por llave: observar, practicar y revisar.',
'Escribe una fecha real y una respuesta que puedas reconocer como tuya. Si un tema no encaja con tu momento, cambia la pregunta. No hay respuestas correctas ni un puntaje de avance espiritual.',
'Puedes imprimir las páginas o escribir en un cuaderno siguiendo las preguntas. Este PDF está preparado para lectura e impresión; no contiene formularios interactivos.',
('sub','Mi intención para este recorrido')]);diary.lines(7)
questions=[
('¿Qué ruido ocupa mi atención hoy?','Describe una situación concreta, no toda tu vida.','¿Qué puedo dejar en pausa durante cinco minutos?'),('¿Qué apareció cuando hice silencio?','Registra una emoción sin intentar resolverla de inmediato.','¿Qué pregunta quiero llevar a la oración?'),('¿Qué espacio real puedo sostener?','Compara lo que planeaste con lo que ocurrió.','¿Qué horario o duración necesito ajustar?'),
('¿Qué decisión quiero mirar con calma?','Separa un hecho de una interpretación.','¿Qué otra explicación es posible?'),('¿Qué información me falta?','Identifica una pregunta que puedas consultar.','¿A quién puedo escuchar sin pedirle que decida por mí?'),('¿Qué paso responsable puedo dar?','Elige una acción reversible.','¿Cuándo revisaré lo que aprendí?'),
('¿Qué valor quiero expresar hoy?','Describe una conducta que lo represente.','¿Qué haría aunque nadie lo reconociera?'),('¿Qué etiqueta necesito revisar?','Escribe un hecho que esa etiqueta no cuenta.','¿Qué fortaleza y qué límite puedo reconocer a la vez?'),('¿Cómo puedo servir con humildad?','Piensa en una ayuda discreta y posible.','¿Qué aprendí al no buscar aprobación?'),
('¿Qué me corresponde hacer?','Distingue tu responsabilidad de la respuesta de otros.','¿Cuál es mi tarea más pequeña de hoy?'),('¿Qué necesito dejar de controlar?','Nombra una incertidumbre sin resolverla a la fuerza.','¿Qué apoyo concreto puedo pedir?'),('¿Qué puedo agradecer sin negar lo difícil?','Da lugar a una gratitud y a una preocupación.','¿Cómo quiero acompañarme mañana?'),
('¿Qué herida puedo nombrar con cuidado?','Elige un tema que puedas explorar sin forzarte.','¿Necesito compañía antes de seguir?'),('¿Qué límite protege mi bienestar?','Redacta lo que harás ante una conducta concreta.','¿Ese límite depende de mis acciones?'),('¿Qué reparación está en mis manos?','Distingue lo que puedes ofrecer de lo que esperas recibir.','¿Puedo respetar el tiempo de la otra persona?'),
('¿Qué necesidad cercana puedo atender?','Relaciona un valor con una habilidad.','¿Qué acción cabe en mi semana real?'),('¿Cuánto puedo ofrecer de manera sostenible?','Anota tiempo, energía y recursos disponibles.','¿Qué necesito decir que no por ahora?'),('¿Qué me enseñó la experiencia?','Describe una utilidad y una dificultad.','¿Qué cambiaría en el próximo intento?'),
('¿Qué práctica quiero conservar?','Define una versión de cinco minutos.','¿Qué rutina existente puede recordármela?'),('¿Qué obstáculo puedo reducir?','Mira el entorno antes de juzgar tu voluntad.','¿Qué versión mínima usaré en un día difícil?'),('¿Qué continúa después de estas páginas?','Nombra un aprendizaje con un ejemplo observable.','¿Cuál será mi siguiente revisión?')]
for i,(q,hint,q2) in enumerate(questions):
 diary.base(f'Día {i+1:02d} · {chapters[i//3]["title"]}');diary.text('Fecha: __________________','small');diary.text(q,'sub');diary.text(hint,'small');diary.lines(5);diary.text(q2,'sub');diary.lines(3);diary.text('Mi siguiente paso posible:','small');diary.lines(2)
for i in range(3):
 diary.pageof(f'Revisión {i+1}','Mira tu semana',[( 'sub','Una práctica que sí realicé')]);diary.lines(3);diary.text('Un obstáculo que puedo ajustar','sub');diary.lines(3);diary.text('Lo que quiero conservar la próxima semana','sub');diary.lines(3)
diary.pageof('Cierre','Mi compromiso de continuidad',[
'Completa con una acción pequeña: «Después de __________, voy a __________ durante __________. Si ese día no puedo, mi versión mínima será __________».',
('sub','Lo que aprendí de mí')]);diary.lines(5);diary.text('Una oración con mis propias palabras','sub');diary.lines(5)
counts[diary.file.name]=diary.save()
# Oraciones originales, no citas bíblicas.
prayers=[
('Para comenzar el día','Salmo 143:8','Dios, recibo este día sin saber todo lo que traerá. Ayúdame a no adelantarme con miedo ni a llenarlo de exigencias imposibles. Que pueda reconocer lo importante, cumplir lo que me corresponde y tratar con cuidado a las personas que encuentre. Cuando me distraiga, recuérdame que puedo volver. Amén.','Elige una intención concreta antes de mirar tus pendientes.','¿Cómo se vería hoy actuar con cuidado?'),
('Cuando necesito dirección','Santiago 1:5','Dios de sabiduría, acompáñame en esta decisión. Ayúdame a distinguir los hechos de mis temores y mis deseos de mis responsabilidades. Dame humildad para consultar lo que no sé y paciencia para no apresurar lo que merece atención. Que mi siguiente paso sea honesto y considerado. Amén.','Anota un dato que necesitas conocer antes de decidir.','¿Qué pregunta todavía no he hecho?'),
('Cuando me cuesta esperar','Salmo 27:14','Dios, esperar me confronta con lo que no controlo. Recibe mi impaciencia sin que tenga que esconderla. Ayúdame a cuidar mi vida mientras llega una respuesta y a reconocer las acciones que sí están en mis manos. Que la espera no me lleve a abandonarme ni a presionar a otros. Amén.','Separa una acción posible de una respuesta que no depende de ti.','¿Qué puedo atender mientras espero?'),
('Cuando me siento rechazado','Romanos 12:3-8','Dios, hoy me duele no sentirme aceptado. Ayúdame a no convertir una experiencia en una sentencia sobre mi valor. Dame claridad para aprender de una crítica útil y fortaleza para alejarme de un trato que me lastima. Que pueda reconocer mi dignidad sin negar la dignidad de los demás. Amén.','Describe lo ocurrido sin adivinar intenciones.','¿Qué necesito para responder con respeto propio?'),
('Para cuidar mis relaciones','Colosenses 3:12-15','Dios, enséñame a escuchar sin preparar de inmediato mi defensa. Ayúdame a decir la verdad con respeto, a preguntar cuando no comprendo y a reconocer mis errores. Que el deseo de tener razón no pese más que el cuidado. Dame también valor para expresar un límite cuando sea necesario. Amén.','Formula una pregunta sincera antes de afirmar una intención ajena.','¿Qué conversación necesita más escucha?'),
('Para poner un límite','Romanos 12:18','Dios, acompáñame cuando decir que no me produce culpa. Ayúdame a distinguir el amor de la obligación de complacer. Dame palabras claras, un tono respetuoso y firmeza para actuar de acuerdo con mis límites. Que no use el límite como castigo, sino como una forma de cuidar lo que puedo sostener. Amén.','Escribe una frase breve que describa tu límite y tu acción.','¿Qué parte de este límite depende de mí?'),
('Cuando necesito pedir perdón','Mateo 5:23-24','Dios, ayúdame a mirar con honestidad el daño que pude causar. Que no esconda mi responsabilidad detrás de excusas. Dame valor para reconocer mi acción, ofrecer una reparación posible y respetar el tiempo de la otra persona. Enséñame a cambiar una conducta, no solo a encontrar palabras. Amén.','Elige una reparación concreta que no exija una respuesta a cambio.','¿Qué conducta necesito cambiar?'),
('Cuando todavía me duele','Salmo 34:18','Dios, hoy no quiero fingir que todo está bien. Recibe lo que duele y ayúdame a reconocer lo que necesito. Dame compañía segura, paciencia con mi proceso y libertad para detenerme cuando sea demasiado. Que la esperanza no me obligue a negar la herida, sino que me acompañe mientras la atiendo. Amén.','Identifica un apoyo confiable o una forma sencilla de cuidarte.','¿Qué necesito pedir con claridad?'),
('Para agradecer','Salmo 103:1-5','Dios, quiero reconocer lo recibido sin ignorar lo difícil. Gracias por las presencias, los gestos y las oportunidades que sostienen mi vida. Ayúdame a no dar por hecho el cuidado de otros. Que mi gratitud pueda expresarse en palabras concretas y en una manera más generosa de actuar. Amén.','Agradece un gesto específico a alguien, sin exagerarlo.','¿Qué detalle pasó inadvertido hoy?'),
('Para servir con humildad','Miqueas 6:8','Dios, muéstrame una oportunidad cercana de ayudar. Que no desprecie lo pequeño ni convierta el servicio en una búsqueda de reconocimiento. Ayúdame a ofrecer lo que tengo con honestidad y a reconocer lo que no puedo prometer. Que mi ayuda respete la libertad y la dignidad de quien la recibe. Amén.','Pregunta qué ayuda sería útil antes de decidir por otra persona.','¿Estoy escuchando la necesidad real?'),
('Cuando estoy cansado','Mateo 11:28-30','Dios, reconozco mi cansancio. Ayúdame a no medir mi valor por lo que logro producir. Dame claridad para ordenar mis responsabilidades, pedir colaboración y hacer espacio para el descanso posible. Que pueda cuidar mi cuerpo y mi atención sin considerar la pausa una derrota. Amén.','Reduce una exigencia no esencial o pide apoyo concreto.','¿Qué carga puedo compartir?'),
('Para actuar con valentía','Josué 1:9','Dios, acompáñame en el paso que estoy evitando. Ayúdame a distinguir el riesgo real del temor a equivocarme. Dame preparación, consejo y valor para actuar de manera responsable. Que la valentía no sea imprudencia, sino la decisión de hacer lo necesario con los recursos que tengo. Amén.','Define un primer paso pequeño y reversible.','¿Qué preparación haría este paso más responsable?'),
('Para volver a empezar','Lamentaciones 3:22-23','Dios, hoy quiero volver sin castigarme por cada interrupción. Ayúdame a aprender de lo que no funcionó y a elegir un paso más sencillo. Que no necesite entusiasmo perfecto para actuar con amor. Dame paciencia para construir lo que vale la pena con actos pequeños y repetidos. Amén.','Retoma una práctica durante dos minutos.','¿Qué puedo ajustar en lugar de abandonarlo todo?'),
('Al terminar el día','Salmo 4:8','Dios, pongo ante ti lo vivido hoy: lo que agradezco, lo que me preocupa y lo que quedó pendiente. Ayúdame a reconocer mis límites y a no resolver esta noche lo que necesita otro momento. Que pueda descansar con honestidad, preparar lo necesario y recibir mañana como una nueva oportunidad. Amén.','Anota un pendiente para mañana y termina la revisión.','¿Qué puedo dejar en pausa por esta noche?')]
b=Book('Bajo_Sus_Alas.pdf','Bajo Sus Alas');b.titlepage('Bajo Sus Alas','14 oraciones para acompañar tu vida cotidiana','BONO 02 · EXPERIENCIA COMPLETA')
b.pageof('Cómo usar este libro','Ora con tus propias palabras',[
'Estas oraciones son originales y se ofrecen como punto de partida. Puedes leerlas en voz baja, adaptarlas o quedarte con una sola frase. No son fórmulas para producir un resultado ni citas literales de la Biblia.',
'Cada página incluye una lectura bíblica sugerida, una oración, una práctica y una pregunta. La lectura invita a conocer el contexto; la práctica ayuda a llevar la oración a una acción cotidiana.',
'No tienes que sentir una emoción especial para orar. Puedes hacerlo desde la gratitud, la duda, el cansancio o el silencio. Tampoco necesitas completar las oraciones en orden.',
'Elige la página que mejor acompañe tu momento. Si quieres, escribe después una oración propia que incluya algo concreto de tu vida.'])
for title,ref,prayer,action,q in prayers:b.pageof('Oración para la vida cotidiana',title,[( 'small','LECTURA SUGERIDA: '+ref),('quote',prayer),('sub','Un gesto para hoy'),action,('sub','Para escribir'),q]);b.lines(3)
b.pageof('Tu propia oración','Una conversación abierta',[
'Puedes comenzar con cuatro movimientos: nombrar cómo estás, agradecer algo concreto, pedir lo que necesitas y reconocer un paso que te corresponde dar. No hace falta usar palabras solemnes.',
('sub','Dios, hoy quiero decirte…')]);b.lines(9)
counts[b.file.name]=b.save()
# Siete noches: contenido contextualizado, sin copiar una traducción.
nights=[
('Una pausa para descansar','Salmo 4','Este salmo pasa por la dificultad, la petición y la confianza. No ofrece una vida sin tensión: permite llevar una inquietud a Dios y terminar mirando hacia el descanso. Lee el poema completo antes de elegir una frase para meditar.','A veces llevamos a la noche una conversación que ya terminó o un pendiente que no podemos resolver. La práctica no consiste en prohibirte pensar, sino en reconocer qué necesita atención mañana y qué puede descansar por ahora.','Escribe un pendiente y el primer paso para atenderlo mañana. Cierra el cuaderno.','Dios, recibe lo que no puedo resolver esta noche. Ayúdame a descansar sin negar mis responsabilidades y a retomarlas cuando corresponda. Amén.'),
('Acompañado en el camino','Salmo 23','La imagen del pastor expresa cuidado y compañía en escenarios distintos, incluso en un valle oscuro. La presencia del valle impide reducir el salmo a la promesa de una vida fácil. Lee atendiendo tanto al cuidado como a la dificultad.','Piensa en las formas concretas de compañía que has recibido: una conversación, un alimento, un consejo o una presencia silenciosa. Reconocerlas no elimina la soledad, pero puede ayudarte a identificar a quién acudir.','Anota una persona o comunidad con la que podrías conectar esta semana.','Dios, ayúdame a reconocer compañía sin exigir que desaparezcan todas mis preguntas. Dame libertad para pedir apoyo y ofrecerlo con respeto. Amén.'),
('Esperanza durante la espera','Salmo 27','El salmo reúne confianza, deseo de cercanía y petición. Su cierre invita a esperar con fortaleza. Lee sin convertir la espera en inactividad ni la confianza en una garantía de que todo ocurrirá como deseas.','La espera puede llenarse de vigilancia: revisar mensajes, anticipar respuestas o imaginar escenarios. Pregunta qué parte de esa vigilancia te ayuda y qué parte solo repite la inquietud. Puedes preparar una acción y permitirte una pausa.','Elige un momento específico para revisar el pendiente mañana, en vez de hacerlo de manera continua.','Dios, acompáñame mientras espero. Ayúdame a atender mi vida presente y a dar los pasos que sí me corresponden. Amén.'),
('Refugio en medio del ruido','Salmo 46','El poema habla de confianza en medio de imágenes de conmoción y conflicto. Su invitación a detenerse se sitúa dentro de ese contexto. No necesitas imaginar una calma perfecta para leerlo con atención.','A veces el ruido viene de fuera; otras veces lo alimentamos acumulando estímulos. Una pausa pequeña puede ayudarte a observar qué necesitas. No tienes que producir serenidad a voluntad: basta con disminuir una distracción durante unos minutos.','Deja una pantalla fuera de alcance y dedica tres minutos a una oración sencilla.','Dios, aquí estoy con el ruido que traigo. Ayúdame a hacer espacio para lo importante y a tratarme con paciencia. Amén.'),
('Reconocer lo recibido','Salmo 103','El salmo recuerda motivos de gratitud y presenta imágenes de compasión. Léelo como una invitación a recordar, no como una obligación de sentir alegría cuando estás atravesando una pérdida.','Agradecer y lamentar pueden convivir. Puedes reconocer el cuidado de alguien y, al mismo tiempo, necesitar que algo cambie. La gratitud más honesta suele ser concreta: un gesto, un alimento, un momento compartido.','Escribe tres detalles del día. Si solo encuentras uno, permite que sea suficiente.','Dios, gracias por lo que sostiene mi vida. Ayúdame a reconocerlo sin usar la gratitud para esconder lo que todavía necesita cuidado. Amén.'),
('Mirar con honestidad','Salmo 139','El salmo explora el conocimiento y la cercanía de Dios con un lenguaje poético. Su lectura puede abrir una reflexión sobre la honestidad personal. Lee también los pasajes que te resulten difíciles y considera su contexto.','Ser conocido no tiene que convertirse en una exigencia de perfección. Puedes mirar un error con responsabilidad sin humillarte. Pregunta qué ocurrió, qué efecto tuvo y qué reparación es posible; deja a un lado las etiquetas absolutas.','Identifica una conducta que quieras corregir y una reparación pequeña que puedas ofrecer.','Dios, ayúdame a mirar mi vida con verdad y compasión. Que reconocer un error abra una posibilidad de cambio, no una condena sobre mi valor. Amén.'),
('Un nuevo paso','Salmo 121','Este poema presenta la imagen del cuidado en el camino. Lee sus palabras como lenguaje de confianza y acompañamiento, no como una invitación a ignorar riesgos o responsabilidades.','Al terminar estas noches, elige algo que quieras conservar. Puede ser una lectura breve, una pregunta escrita o una oración antes de descansar. El valor está en que acompañe tu vida de manera sostenible, no en completar una secuencia perfecta.','Define una práctica de cinco minutos para la próxima semana y una fecha de revisión.','Dios, acompáñame en lo que sigue. Ayúdame a caminar con atención, a recibir apoyo y a expresar mi fe en acciones de cuidado. Amén.')]
b=Book('7_Noches_con_los_Salmos.pdf','7 Noches con los Salmos');b.titlepage('7 Noches<br/>con los Salmos','Lectura, reflexión y oración para terminar el día con intención','BONO 03 · EXPERIENCIA COMPLETA')
b.pageof('Preparación','Un cierre de día sencillo',[
'Elige un momento breve y lee el salmo completo en tu Biblia. Este material resume temas e invita a reflexionar; no reproduce una traducción bíblica ni sustituye la lectura del texto.',
'Puedes dedicar dos minutos a la lectura, tres a la reflexión y cinco a escribir y orar. Ajusta ese tiempo a tu realidad. No hay una obligación de sentir calma ni una promesa de mejorar el sueño.',
'Las siete noches pueden ser consecutivas o estar separadas. Si un pasaje despierta preguntas, anótalas y busca una explicación contextual con una persona o recurso de confianza.',
'Antes de comenzar, deja preparado un cuaderno. Termina cada noche eligiendo un paso pequeño o una pausa consciente, sin extender la práctica hasta convertirla en otra exigencia.'])
for i,(title,ref,context,reflection,action,prayer) in enumerate(nights):
 b.pageof(f'Noche {i+1} · {ref}',title,[( 'sub','Lee primero '+ref),context,reflection,('sub','Una práctica breve'),action])
 b.pageof(f'Noche {i+1} · Cierre','Lleva la lectura a tu vida',[( 'quote',prayer),('sub','Una idea que quiero conservar')]);b.lines(5);b.text('Mi paso posible para mañana','sub');b.lines(4)
b.pageof('Continuidad','Después de la séptima noche',[
'Revisa lo que escribiste. ¿Hubo una pregunta que se repitió? ¿Una práctica que resultó útil? ¿Un momento del día en el que te fue más fácil detenerte?',
'Elige una sola lectura para volver a ella la próxima semana. Puedes comparar cómo la recibes en otro momento de tu vida. No necesitas encontrar un mensaje secreto ni una explicación definitiva.',
('sub','Lecturas utilizadas'),'Salmos 4, 23, 27, 46, 103, 139 y 121. Las numeraciones siguen el uso habitual de las Biblias contemporáneas; algunas ediciones pueden presentar una numeración distinta.',
('sub','Mi práctica para continuar')]);b.lines(4)
counts[b.file.name]=b.save()
# Tarjetas: paráfrasis explícitas, referencia bíblica para leer el original.
cards=[('Haz espacio para escuchar','Lucas 10:38-42','Hoy puedo detenerme unos minutos antes de responder a todo.','¿Qué merece mi atención?'),('Pide sabiduría','Santiago 1:5','Reconocer lo que no sé también forma parte de una vida de fe.','¿Qué necesito preguntar?'),('Escucha otras perspectivas','Proverbios 15:22','Un consejo puede ampliar mi mirada sin quitarme responsabilidad.','¿A quién puedo consultar?'),('Vive con propósito','Efesios 2:10','Puedo expresar mis valores en una acción concreta de cuidado.','¿Qué bien puedo hacer hoy?'),('Honra los dones distintos','Romanos 12:3-8','Mi valor no depende de compararme con otra persona.','¿Qué puedo ofrecer con humildad?'),('Ora con honestidad','Marcos 9:24','Puedo llevar mis dudas a Dios sin fingir seguridad.','¿Qué me cuesta expresar?'),('Atiende el paso de hoy','Mateo 6:25-34','No necesito resolver todo el futuro para actuar responsablemente ahora.','¿Cuál es mi tarea posible?'),('Elige la compasión','Colosenses 3:12-15','El cuidado también puede expresarse en la forma de hablar.','¿Cómo puedo responder con respeto?'),('Busca la paz posible','Romanos 12:18','Puedo cuidar mi conducta y reconocer lo que no depende de mí.','¿Qué límite necesito respetar?'),('Camina con humildad','Miqueas 6:8','La vida espiritual se vuelve concreta en la justicia y la bondad.','¿Qué acto refleja mis valores?'),('Haz visible el cuidado','Mateo 5:13-16','Una acción generosa no necesita convertirse en una exhibición.','¿Qué ayuda sería útil?'),('Practica lo que aprendes','Santiago 1:22-25','Una idea cobra forma cuando la llevo a una decisión cotidiana.','¿Qué voy a poner en práctica?'),('No desprecies lo pequeño','Gálatas 6:9','Puedo perseverar con paciencia y revisar mi ritmo cuando lo necesito.','¿Qué paso puedo sostener?'),('Recibe el descanso','Salmo 4:8','Puedo dejar un pendiente preparado para mañana.','¿Qué puedo pausar esta noche?'),('Reconoce compañía','Salmo 23','Pedir ayuda no disminuye mi fe ni mi dignidad.','¿A quién puedo acercarme?'),('Espera con intención','Salmo 27:14','La espera puede incluir cuidado, preparación y apoyo.','¿Qué puedo atender mientras espero?'),('Haz una pausa','Salmo 46:10','No tengo que interpretar cada pensamiento para escucharlo.','¿Qué ruido puedo reducir?'),('Agradece lo concreto','Salmo 103:1-5','Puedo reconocer algo bueno sin negar lo difícil.','¿Qué gesto quiero agradecer?'),('Mira con honestidad','Salmo 139:23-24','Reconocer un error puede abrir una reparación.','¿Qué necesito corregir?'),('Camina con cuidado','Salmo 121','La confianza puede acompañar decisiones prudentes.','¿Qué preparación necesito?'),('Vuelve a comenzar','Lamentaciones 3:22-23','Una interrupción no cancela la posibilidad de retomar.','¿Cuál será mi versión mínima hoy?')]
b=Book('Palabras_de_Luz.pdf','Palabras de Luz');b.titlepage('Palabras<br/>de Luz','21 tarjetas de reflexión para volver a lo esencial','BONO 04 · EXPERIENCIA COMPLETA')
b.pageof('Guía de uso','Una idea para llevar contigo',[
'Estas tarjetas contienen reflexiones originales inspiradas en pasajes bíblicos. No son citas textuales. Cada referencia te permite buscar y leer el pasaje completo en la traducción que prefieras.',
'Elige una tarjeta, lee la referencia y lleva la pregunta a una acción concreta. Puedes imprimir las hojas y recortar por las líneas, o consultarlas en tu celular.',
'No es necesario usar todas las tarjetas en orden. Son recordatorios para la reflexión personal, no fórmulas que garanticen acontecimientos ni frases para atribuir intenciones a otras personas.'])
for n in range(0,21,3):
 b.base('Tarjetas de reflexión · Textos originales')
 for j,(title,ref,reflection,q) in enumerate(cards[n:n+3]):
  top=530-j*158;c=b.c;c.setStrokeColor(HexColor('#c4a153'));c.roundRect(32,top-145,356,145,7,fill=0,stroke=1);b.y=top-12;b.text(title,'sub');b.text(reflection,'small');b.text(q,'small');b.text('LECTURA: '+ref+' · REFLEXIÓN, NO CITA TEXTUAL','small')
counts[b.file.name]=b.save()
for file in OUT.glob('*.pdf'):
 target=ROOT.parent/'output/pdf'/file.name;target.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(file,target)
(ROOT/'content-tools/manifest.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2))
print(json.dumps(counts,ensure_ascii=False))
