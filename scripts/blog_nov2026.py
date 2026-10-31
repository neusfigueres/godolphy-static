#!/usr/bin/env python3
"""Artículos de blog de noviembre de 2026 sobre las funcionalidades nuevas.
Genera los borradores en borrador/AAAA-MM-DD-slug.html con el chrome de un borrador existente.
Uso: python3 scripts/blog_nov2026.py  (desde la raíz de godolphy-static)
"""
import json, re, html

SRC = 'borrador/2026-11-10-servicios-de-estetica-mas-rentables.html'
BASE = 'https://www.godolphy.com'
MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
A = lambda href, txt: f'<a href="{href}">{txt}</a>'

ARTICULOS = [
dict(
  fecha='2026-11-04', slug='tarjetas-regalo-navidad-salon-de-belleza', cat='Marketing',
  title='Tarjetas regalo de Navidad para tu salón: cómo prepararlas en noviembre',
  h1='Tarjetas regalo de Navidad para tu salón: cómo prepararlas en noviembre',
  desc='Qué tarjetas regalo preparar para Navidad y Reyes en tu salón de belleza, cuándo empezar a anunciarlas y cómo venderlas online aunque el salón esté cerrado.',
  body=f'''
    <p>Diciembre es el mes en el que más se regala, y una tarjeta regalo para un salón de belleza es de los regalos más fáciles: no hay que acertar con la talla ni con el color. Pero las ventas de Navidad no se improvisan el día 20. Se preparan en noviembre.</p>
    <p>Esta guía va de cómo organizar tu campaña de tarjetas regalo para Navidad y Reyes. Si buscas lo básico (qué tipo de tarjeta vender, caducidad, cómo llevar las cuentas), lo tienes en {A('/tarjetas-regalo-salon-de-belleza/', 'tarjetas regalo para tu salón de belleza')}.</p>

    <h2>El calendario: de noviembre a Reyes</h2>
    <table>
      <thead><tr><th>Cuándo</th><th>Qué hacer</th></tr></thead>
      <tbody>
        <tr><td>Primera quincena de noviembre</td><td>Decide los importes y los packs, prepara el texto y la imagen, y activa la venta online.</td></tr>
        <tr><td>Segunda quincena de noviembre</td><td>Empieza a anunciarlas: en el salón, en Instagram y a tu lista de clientes.</td></tr>
        <tr><td>1 al 24 de diciembre</td><td>El momento fuerte. Recuérdalo cada semana y ten el enlace siempre a mano.</td></tr>
        <tr><td>24 de diciembre al 6 de enero</td><td>Las compras de última hora y las de Reyes. La tarjeta digital es la que salva a quien llega tarde.</td></tr>
        <tr><td>Enero y febrero</td><td>Llegan las personas que la recibieron. Es tu oportunidad de convertirlas en clientes fijos.</td></tr>
      </tbody>
    </table>

    <h2>Qué tarjetas preparar</h2>
    <ul>
      <li><strong>Importes redondos y cerrados.</strong> Quien regala quiere decidir rápido. Dos o tres importes, por ejemplo 30, 50 y 80 €, se venden mejor que «el importe que quieras».</li>
      <li><strong>Un pack con nombre.</strong> «Manicura y pedicura», «Ritual facial», «Día de relax»… Un nombre ayuda a imaginar el regalo. Ponle un precio que coincida con uno de tus importes.</li>
      <li><strong>Una opción pequeña.</strong> Para el amigo invisible y los detalles de última hora, un importe bajo que cubra un servicio sencillo.</li>
      <li><strong>Caducidad clara.</strong> Decide cuánto duran y que se vea al comprarla. Si tienes dudas sobre la caducidad o el IVA de las tarjetas, consúltalo con tu gestoría.</li>
    </ul>

    <h2>Dónde venderlas</h2>
    <h3>En el salón</h3>
    <p>Un cartel junto a la caja y una frase al cobrar: «¿Ya tienes los regalos de Navidad?». Quien ya es cliente tuyo es quien más fácil la compra, porque sabe lo que regala.</p>
    <h3>Online, desde tu web de reservas</h3>
    <p>Aquí está la diferencia. Muchas tarjetas regalo se deciden la noche antes, o el 5 de enero a última hora. Si solo se pueden comprar en el salón, esa venta se pierde. Con la venta online, el cliente la compra a cualquier hora, la paga con tarjeta y la persona que la recibe la tiene en su email.</p>
    <h3>En redes y por email</h3>
    <p>Un post en Instagram con el enlace de compra, una historia cada semana de diciembre y un email a tu lista de clientes a finales de noviembre. Que el mensaje sea corto: qué regalan, cuánto cuesta y dónde se compra.</p>

    <h2>Después de Navidad: la persona que la recibe</h2>
    <p>Quien recibe una tarjeta regalo muchas veces no te conocía. Viene a probar tu salón sin que hayas pagado publicidad por traerla. Cuídala:</p>
    <ul>
      <li>Atiéndela como a un cliente nuevo: pregúntale qué le gusta y explícale qué más haces.</li>
      <li>Si no gasta todo el saldo, recuérdale que le queda para otra visita.</li>
      <li>Antes de que se vaya, ofrécele reservar la siguiente cita.</li>
    </ul>

    <h2>Cómo te ayuda Godolphy</h2>
    <p>Con Godolphy, tus clientes compran la tarjeta regalo desde tu web de reservas, a cualquier hora, y la pagan con tarjeta. El dinero llega a tu cuenta de Stripe y quien la recibe tiene el código en su email. Al reservar, introduce el código y el importe se descuenta de su cita; si sobra saldo, queda en la tarjeta para la próxima vez.</p>
    <p>Las que vendes en el salón también las creas desde el panel, incluidas las físicas, y la venta queda apuntada en la caja. Las tarjetas regalo están en los planes Pro y Max y en la prueba gratuita.</p>
    <p>Más detalles en {A('/funcionalidades/cupones-y-tarjetas-regalo/', 'cupones y tarjetas regalo')} y, paso a paso, en {A('/ayuda/tarjetas-regalo-online/', 'vender tarjetas regalo online')}.</p>
  ''',
  faq=[
    ('¿Cuándo empezar a vender tarjetas regalo de Navidad?', 'En la segunda quincena de noviembre. Así llegas a quien compra pronto y tienes tiempo de recordarlo durante todo diciembre.'),
    ('¿Qué importes funcionan mejor?', 'Dos o tres importes redondos y cerrados, y un pack con nombre. Quien regala quiere decidir rápido.'),
    ('¿Puedo vender tarjetas regalo con el salón cerrado?', 'Sí, si las vendes online desde tu web de reservas. El cliente la paga con tarjeta y la persona que la recibe tiene el código en su email.'),
    ('¿Las tarjetas regalo tienen que caducar?', 'Tú decides la caducidad, pero que se vea al comprarla. Si tienes dudas sobre la caducidad o el IVA, consúltalo con tu gestoría.'),
  ]),

dict(
  fecha='2026-11-06', slug='plan-financiero-2027-salon-de-belleza', cat='Consejos de negocio',
  title='Plan financiero 2027 para tu salón: cómo hacerlo antes de que empiece el año',
  h1='Plan financiero 2027 para tu salón: cómo hacerlo antes de que empiece el año',
  desc='Cómo hacer el plan financiero de 2027 de tu salón de belleza o centro de estética: revisar 2026, fijar objetivos mes a mes, prever gastos y comparar cada mes el plan con la realidad.',
  body=f'''
    <p>Si cada enero tu salón empieza igual que el anterior, con las mismas dudas y los mismos números, no es mala suerte: es que nadie ha decidido a dónde quiere llegar. Un plan financiero sirve exactamente para eso. Y no es cosa de grandes empresas: cuanto más pequeño es el negocio, más se nota cada euro.</p>
    <p>Noviembre y diciembre son buen momento para hacerlo: tienes casi todo el año 2026 para mirar atrás y todavía no ha empezado 2027.</p>

    <h2>1. Mira cómo te ha ido en 2026</h2>
    <p>Antes de decidir nada, apunta mes a mes lo que pasó este año:</p>
    <ul>
      <li><strong>Citas</strong> y cuántas eran de clientes que repiten.</li>
      <li><strong>Clientes nuevos.</strong></li>
      <li><strong>Ticket medio:</strong> lo que deja de media cada cita.</li>
      <li><strong>Facturación</strong> y <strong>gastos</strong>, separados por tipo: equipo, alquiler y suministros, producto, marketing y otros.</li>
    </ul>
    <p>Fíjate sobre todo en la temporada: qué meses van fuertes y cuáles flojean. Tu plan de 2027 tiene que respetarla.</p>

    <h2>2. Decide cuánto quieres crecer</h2>
    <p>Un objetivo realista se cumple; uno imposible se abandona en febrero. Empieza con un crecimiento prudente sobre lo que hiciste en 2026, por ejemplo un 5 o un 10 %, y piensa de dónde saldrá: más citas, un ticket medio más alto, más clientes que repiten o menos huecos en la agenda.</p>
    <p>Si quieres subir el ticket, aquí tienes ideas para {A('/como-subir-ticket-medio-salon', 'subir el ticket medio de tu salón')}.</p>

    <h2>3. Pon objetivos mes a mes</h2>
    <p>Un objetivo anual no se puede vigilar. Uno mensual, sí. Para cada mes de 2027 apunta:</p>
    <ul>
      <li>Citas y cuántas de clientes que repiten.</li>
      <li>Facturación.</li>
      <li>Cada tipo de gasto.</li>
      <li>Si vas a hacer una inversión (una cabina nueva, una reforma…) o a recibir un préstamo o una ayuda, en qué mes.</li>
    </ul>
    <p>Usa el mismo mes del año anterior como punto de partida, para no pedirle a agosto lo que da noviembre.</p>

    <h2>4. Los números que te dicen si vas bien</h2>
    <ul>
      <li><strong>Beneficio:</strong> facturación menos gastos. Calcúlalo sin IVA, porque el IVA no es tuyo.</li>
      <li><strong>CAC:</strong> lo que te cuesta en marketing cada cliente nuevo.</li>
      <li><strong>LTV:</strong> lo que te deja un cliente en un año. Si un cliente te deja mucho más de lo que te cuesta captarlo, merece la pena invertir en atraer más.</li>
      <li><strong>Caja acumulada:</strong> el dinero con el que cuentas mes a mes. Te avisa antes de que llegue un mes apretado.</li>
    </ul>

    <h2>5. Compáralo cada mes con la realidad</h2>
    <p>El plan no sirve si se queda en un cajón. Cada mes, y mejor aún cada semana, compara lo previsto con lo que está pasando. Si a mitad de mes vas por debajo, todavía estás a tiempo de llenar huecos o lanzar una promoción. Si esperas a diciembre, ya no.</p>

    <h2>Dos maneras de hacerlo</h2>
    <h3>Con una plantilla de Excel gratis</h3>
    <p>Si prefieres hacerlo tú, tienes la {A('/plan-financiero-salon-estetica-excel-google-sheet/', 'plantilla de plan financiero para centros de estética')}, gratis y en Excel o Google Sheets.</p>
    <h3>Con Godolphy, a partir de tus datos</h3>
    <p>En Godolphy, el Plan financiero te propone cada mes a partir de tus citas reales, respetando la temporada, y de tus gastos. Tú decides cuánto quieres crecer y ajustas lo que quieras. Si lo creas a partir de septiembre, cubre lo que queda de año y todo el siguiente, así que ya puedes preparar 2027.</p>
    <p>Después, cada mes ves en columnas el plan, la realidad y la diferencia: citas, clientes nuevos, ticket medio, facturación, gastos, beneficio, CAC, LTV y caja. Está en los planes Pro y Max y en la prueba gratuita. Más detalles en {A('/funcionalidades/plan-financiero/', 'plan financiero')} y, paso a paso, en {A('/ayuda/plan-financiero/', 'el centro de ayuda')}.</p>
  ''',
  faq=[
    ('¿Cuándo hay que hacer el plan financiero del año siguiente?', 'En noviembre o diciembre. Ya conoces casi todo el año actual y tienes tiempo de preparar el siguiente antes de que empiece.'),
    ('¿Cuánto debería crecer mi salón en 2027?', 'Depende de tu punto de partida. Un crecimiento prudente, de un 5 o un 10 %, es más fácil de cumplir. Siempre puedes subirlo.'),
    ('¿El beneficio se calcula con IVA o sin IVA?', 'Sin IVA. El IVA que cobras no es tuyo: lo ingresas a Hacienda.'),
    ('¿Qué son el CAC y el LTV?', 'El CAC es lo que te cuesta en marketing cada cliente nuevo. El LTV es lo que te deja un cliente en un año. Compararlos te dice si compensa invertir en atraer clientes.'),
  ]),

dict(
  fecha='2026-11-09', slug='cobrar-mas-caro-fin-de-semana-salon', cat='Consejos de negocio',
  title='¿Se puede cobrar más caro en fin de semana? Precios por día y hora en tu salón',
  h1='¿Se puede cobrar más caro en fin de semana? Precios por día y hora en tu salón',
  desc='Cómo poner un recargo en las horas que más se piden y un descuento en las horas flojas de tu salón: qué franjas elegir, cuánto subir o bajar y cómo contárselo a tus clientes.',
  body=f'''
    <p>Los sábados por la mañana se llenan solos. Los martes por la tarde, no. Y sin embargo, en la mayoría de salones una manicura cuesta lo mismo a cualquier hora. Ajustar el precio según el día y la hora es algo que hacen hoteles, aerolíneas o gimnasios desde hace años, y también funciona en un salón.</p>

    <h2>Dos formas de usarlo</h2>
    <ul>
      <li><strong>Un recargo en las horas que más se piden.</strong> Si el sábado por la mañana siempre está lleno, ese hueco vale más. Quien solo puede venir ese día seguirá reservando, y quien tiene horario flexible quizá prefiera venir entre semana.</li>
      <li><strong>Un descuento en las horas flojas.</strong> Una hora vacía no se recupera. Un descuento en las horas que siempre se quedan libres puede atraer a quien tiene horario flexible y llenar la agenda.</li>
    </ul>
    <p>Muchas veces funciona mejor empezar por el descuento: es más fácil de explicar y nadie se lleva una sorpresa desagradable.</p>

    <h2>Cómo elegir las franjas</h2>
    <ol>
      <li><strong>Mira tu agenda de los últimos meses.</strong> Apunta qué días y horas se llenan siempre y cuáles se quedan vacíos.</li>
      <li><strong>Empieza con una o dos franjas.</strong> Por ejemplo, el sábado por la mañana y el martes por la tarde. Si pones muchas, nadie entiende tus precios.</li>
      <li><strong>Usa porcentajes pequeños.</strong> Un 10 o un 15 % es suficiente para notar la diferencia sin cambiar tu posición de precios.</li>
      <li><strong>Revísalo al cabo de unas semanas.</strong> Si la franja con descuento se llena, ya no hace falta el descuento. Si la del recargo se vacía, bájalo.</li>
    </ol>

    <h2>Un ejemplo</h2>
    <p>Una manicura de 25 €:</p>
    <table>
      <thead><tr><th>Franja</th><th>Ajuste</th><th>Precio</th></tr></thead>
      <tbody>
        <tr><td>Sábado de 9:00 a 14:00</td><td>+10 %</td><td>27,50 €</td></tr>
        <tr><td>Martes de 15:00 a 19:00</td><td>−15 %</td><td>21,25 €</td></tr>
        <tr><td>Resto de la semana</td><td>—</td><td>25,00 €</td></tr>
      </tbody>
    </table>
    <p>Es un ejemplo: los porcentajes y las franjas los decides tú según tu agenda.</p>

    <h2>Cómo contárselo a tus clientes</h2>
    <ul>
      <li><strong>Que vean el precio final antes de reservar.</strong> Nada de sorpresas en la caja.</li>
      <li><strong>Avisa a tu clientela habitual</strong> si vas a subir el precio del fin de semana, antes de que lo vea al reservar.</li>
      <li><strong>Cuéntalo en positivo.</strong> «Los martes por la tarde, un 15 % menos» se entiende mejor que «los sábados son más caros».</li>
      <li><strong>Respeta las citas ya reservadas.</strong> Quien reservó con un precio debe pagar ese precio.</li>
    </ul>

    <h2>Cómo te ayuda Godolphy</h2>
    <p>En Godolphy creas franjas con recargo o descuento por día y hora: eliges los días, la hora de inicio y de fin, y el porcentaje. El porcentaje se aplica a cada servicio y cada extra según la hora en la que empieza la cita.</p>
    <p>En tu web de reservas, tus clientes ven el precio final al elegir la hora, sin etiquetas ni precios tachados. Las citas ya reservadas mantienen su precio. Está en los planes Pro y Max y en la prueba gratuita.</p>
    <p>Más detalles en {A('/funcionalidades/precio-por-dia-y-hora/', 'precio según día y hora')} y, paso a paso, en {A('/ayuda/precio-segun-dia-y-hora/', 'el centro de ayuda')}. Si quieres revisar antes tus precios base, mira {A('/como-calcular-los-precios-de-mis-servicios-de-belleza/', 'cómo calcular los precios de tus servicios de belleza')}.</p>
  ''',
  faq=[
    ('¿Se puede cobrar más caro en fin de semana en un salón de belleza?', 'Sí, siempre que tus clientes vean el precio final antes de reservar y respetes el precio de las citas ya reservadas.'),
    ('¿Cuánto subir o bajar el precio?', 'Empieza con porcentajes pequeños, de un 10 o un 15 %, y revísalo al cabo de unas semanas según cómo se llene tu agenda.'),
    ('¿Es mejor un recargo o un descuento?', 'Muchas veces conviene empezar por un descuento en las horas flojas: es más fácil de explicar y ayuda a llenar huecos que de otro modo se perderían.'),
    ('¿Qué pasa con las citas ya reservadas si cambio los precios?', 'Deben mantener el precio con el que se reservaron. En Godolphy, las citas ya reservadas no cambian.'),
  ]),

dict(
  fecha='2026-11-12', slug='vacaciones-bajas-equipo-salon', cat='Gestión del equipo',
  title='Vacaciones y bajas del equipo de tu salón sin perder clientes',
  h1='Vacaciones y bajas del equipo de tu salón sin perder clientes',
  desc='Cómo organizar las vacaciones del equipo de tu salón, qué hacer con las citas cuando alguien se pone de baja y cómo evitar perder clientes cuando una profesional deja el equipo.',
  body=f'''
    <p>«Mañana no vendré a trabajar.» Es uno de los mensajes que más trabajo dan en un salón: hay que mirar la agenda, llamar a cada cliente, buscar quién puede cubrir… Y lo mismo pasa, con más tiempo, con las vacaciones. Bien organizado, ninguno de los dos casos tiene por qué costarte clientes.</p>

    <h2>Vacaciones: planificar con tiempo</h2>
    <p>En España, el Estatuto de los Trabajadores establece que las vacaciones anuales no pueden ser inferiores a 30 días naturales y que cada trabajador debe conocer sus fechas al menos dos meses antes de empezar a disfrutarlas ({A('https://www.boe.es/buscar/act.php?id=BOE-A-2015-11430#a38', 'artículo 38')}). Tu convenio colectivo puede mejorar estas condiciones, así que consúltalo.</p>
    <p>Para el salón, esos dos meses son una ventaja:</p>
    <ul>
      <li><strong>Haz un calendario de vacaciones de todo el equipo</strong> a principio de año, y evita que coincidan varias personas en las semanas fuertes.</li>
      <li><strong>Bloquea las fechas en la agenda en cuanto se sepan.</strong> Si nadie puede reservar con esa persona esos días, no tendrás citas que mover.</li>
      <li><strong>Revisa qué servicios quedan cubiertos.</strong> Si la única persona que hace extensiones se va dos semanas, avísalo en tu web o en redes con tiempo.</li>
    </ul>

    <h2>Una baja o un imprevisto: actuar el mismo día</h2>
    <p>Las bajas no avisan. Cuando alguien no puede venir, lo importante es que ningún cliente se presente sin que nadie le haya dicho nada:</p>
    <ol>
      <li><strong>Mira qué citas tenía</strong> esos días.</li>
      <li><strong>Busca quién puede cubrir</strong> cada cita a la misma hora. Para el cliente, es la opción más cómoda: misma hora y mismo precio.</li>
      <li><strong>Si nadie puede, avísale cuanto antes</strong> y dale opciones: otra persona, otro día u otra hora, o cancelar sin coste.</li>
      <li><strong>Si ya había pagado algo,</strong> deja claro qué pasa con ese dinero.</li>
    </ol>

    <h2>Cuando alguien deja el equipo</h2>
    <p>Es el momento en el que más clientes se pierden: los clientes fieles de esa persona no saben si seguir viniendo. Para que se queden en el salón:</p>
    <ul>
      <li><strong>Resuelve antes todas sus citas futuras,</strong> igual que en una baja.</li>
      <li><strong>Avisa a su clientela habitual</strong> de que el resto del equipo les atenderá como siempre. Un mensaje a tiempo evita que se vayan con ella o a otro salón.</li>
      <li><strong>No borres su ficha:</strong> conserva el historial de citas y cobros.</li>
    </ul>

    <h2>Cómo te ayuda Godolphy</h2>
    <p>En Godolphy marcas la ausencia (vacaciones, baja, permiso o un día libre) y desde ese momento nadie puede reservar con esa persona esos días. Si ya tenía citas, Godolphy te las enseña y eliges qué hacer con cada una:</p>
    <ul>
      <li><strong>Pasarla a otra persona del equipo</strong> libre a la misma hora, con el mismo precio, y avisar del cambio por email.</li>
      <li><strong>Enviar un enlace por email y WhatsApp</strong> para que cada cliente elija otra persona, otro día u hora, o cancele sin coste, sin iniciar sesión.</li>
    </ul>
    <p>Si el cliente no responde, recibe un segundo aviso, y 24 horas antes de la cita Godolphy la pasa a quien esté libre o la cancela sin coste y devuelve lo pagado online.</p>
    <p>Cuando alguien deja el equipo, Godolphy te pide resolver sus citas antes de desactivar su ficha y te ofrece enviar un email a su clientela habitual. Todo esto está en todos los planes.</p>
    <p>Más detalles en {A('/funcionalidades/vacaciones-y-ausencias/', 'vacaciones y ausencias')} y, paso a paso, en {A('/ayuda/ausencias-del-equipo/', 'ausencias del equipo')} y {A('/ayuda/desactivar-profesional/', 'cuando alguien deja el equipo')}.</p>
  ''',
  faq=[
    ('¿Con cuánta antelación hay que fijar las vacaciones del equipo?', 'Según el artículo 38 del Estatuto de los Trabajadores, cada trabajador debe conocer sus fechas de vacaciones al menos dos meses antes. Tu convenio colectivo puede fijar otras condiciones.'),
    ('¿Qué hago con las citas de una profesional que se pone de baja?', 'Pásalas a otra persona del equipo libre a la misma hora o avisa a cada cliente para que elija otra persona, otro día u hora, o cancele sin coste.'),
    ('¿Cómo evito perder clientes cuando alguien deja el salón?', 'Resuelve todas sus citas futuras y avisa a su clientela habitual de que el resto del equipo les atenderá como siempre.'),
  ]),
]


def fecha_larga(f):
    a, m, d = f.split('-')
    return f'{int(d)} de {MESES[int(m)-1]} de {a}'


def build(chrome, p):
    url = f"{BASE}/{p['slug']}/"
    s = chrome
    s = re.sub(r'<title>.*?</title>', f"<title>{html.escape(p['title'])}</title>", s, count=1, flags=re.S)
    s = re.sub(r'\s*<meta (property="og:image"|name="twitter:image")[^>]*>', '', s)
    s = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + html.escape(p['desc']), s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    art = {"@context": "https://schema.org", "@type": "Article", "headline": p['h1'], "description": p['desc'], "url": url,
           "datePublished": p['fecha'], "dateModified": p['fecha'],
           "author": {"@type": "Organization", "name": "Godolphy", "url": BASE},
           "publisher": {"@type": "Organization", "name": "Godolphy", "url": BASE, "logo": {"@type": "ImageObject", "url": BASE + "/wp-images/logo.png"}}}
    faq = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p['faq']]}
    s = re.sub(r'<!-- SEO:schema-article -->.*?</script>\s*<script type="application/ld\+json">.*?</script>',
               lambda m: '<!-- SEO:schema-article -->\n  <script type="application/ld+json">\n' + json.dumps(art, ensure_ascii=False, indent=2) +
               '\n</script>\n  <script type="application/ld+json">\n' + json.dumps(faq, ensure_ascii=False) + '\n</script>', s, count=1, flags=re.S)
    faq_html = '\n'.join(f'    <h3>{html.escape(q)}</h3>\n    <p>{html.escape(a)}</p>' for q, a in p['faq'])
    i = s.index('<article'); j = s.index('<div style="margin:56px 0 0;padding:40px;background:linear-gradient')
    head = f'''<article style="max-width:780px;margin:0 auto;padding:60px 40px 80px;">

  <div style="margin-bottom:24px;">
    <a href="/blog/" style="font-size:13px;color:rgba(2,2,30,.4);text-decoration:none;">Blog</a>
    <span style="font-size:13px;color:rgba(2,2,30,.25);margin:0 6px;">/</span>
    <span style="font-size:13px;color:rgba(2,2,30,.4);">{p['cat']}</span>
  </div>

  <h1 class="font-gabarito" style="font-size:40px;font-weight:700;color:#02021e;line-height:1.15;margin:0 0 24px;">{p['h1']}</h1>

  <div style="display:flex;align-items:center;gap:16px;margin-bottom:40px;padding-bottom:32px;border-bottom:1px solid rgba(2,2,30,.08);">
    <span style="font-size:14px;color:rgba(2,2,30,.45);">{fecha_larga(p['fecha'])}</span>
    <span style="width:4px;height:4px;border-radius:50%;background:rgba(2,2,30,.2);display:inline-block;"></span>
    <span style="font-size:14px;color:rgba(2,2,30,.45);">Godolphy</span>
  </div>

  <div class="post-content">
{p['body'].rstrip()}

    <h2>Preguntas frecuentes</h2>
{faq_html}

  '''
    s = s[:i] + head + s[j:]
    out = f"borrador/{p['fecha']}-{p['slug']}.html"
    open(out, 'w', encoding='utf-8').write(s)
    return out


if __name__ == '__main__':
    chrome = open(SRC, encoding='utf-8').read()
    for p in ARTICULOS:
        print('ok', build(chrome, p))
