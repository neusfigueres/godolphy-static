#!/usr/bin/env python3
"""Genera las páginas nuevas de /funcionalidades/ (oct. 2026) a partir del chrome de
cupones-y-tarjetas-regalo. Textos comprobados contra el panel y el centro de ayuda.
Uso: python3 scripts/build_feature_pages.py   (desde la raíz de godolphy-static)
"""
import html, json, os, re

SRC = 'funcionalidades/cupones-y-tarjetas-regalo/index.html'
BASE = 'https://www.godolphy.com'
SIGNUP = 'https://app.godolphy.com/auth/sign-up'

ICONS = {
    'ticket': '<path d="M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M13 5v2M13 17v2M13 11v2"/>',
    'percent': '<line x1="19" x2="5" y1="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
    'receipt': '<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/><path d="M16 8H8M16 12H8M13 16H8"/>',
    'tag': '<path d="M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 .586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 0-3.42z"/><circle cx="7.5" cy="7.5" r=".5" fill="#fff"/>',
    'chart': '<path d="M3 3v16a2 2 0 0 0 2 2h16"/><path d="m19 9-5 5-4-4-3 3"/>',
    'bulb': '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6M10 22h4"/>',
    'clock': '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    'plane': '<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>',
    'upload': '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/>',
    'cash': '<rect width="20" height="12" x="2" y="6" rx="2"/><circle cx="12" cy="12" r="2"/><path d="M6 12h.01M18 12h.01"/>',
    'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    'shield': '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
}

CHIP = '<a href="{href}" style="display:inline-block;padding:10px 18px;border-radius:999px;background:#f3eeff;color:#631cff;font-weight:600;font-size:15px;text-decoration:none;">{text}</a>'
PRO_MAX = 'Incluido en los planes Pro y Max, y en la prueba gratuita.'


def img(src, alt, mobile=False):
    w = 'max-width:340px;' if mobile else ''
    return (f'<div class="feat-img" style="padding:24px;min-height:0;"><img src="{src}" alt="{html.escape(alt)}" loading="lazy" '
            f'style="width:100%;{w}height:auto;display:block;border-radius:14px;box-shadow:0 18px 50px rgba(2,2,30,.12);background:#fff;" /></div>')


def roles_card():
    rows=[('Propietaria','Lo puede hacer todo: configuración, servicios, equipo, ventas, marketing, análisis y el plan.'),
          ('Recepcionista','Agenda, citas, clientes, cobros y caja. Sin configuración ni borrar datos.'),
          ('Profesional','Su calendario y su perfil. Nada más.')]
    li=''.join(f'<div style="padding:18px 20px;border-radius:16px;background:#fff;border:1px solid rgba(99,28,255,.12);margin-bottom:12px;"><div style="font-weight:700;color:#631cff;font-size:15px;margin-bottom:4px;">{a}</div><div style="color:rgba(2,2,30,.7);font-size:15px;line-height:1.55;">{b}</div></div>' for a,b in rows)
    return f'<div class="feat-img" style="padding:28px;min-height:0;display:block;">{li}</div>'


PAGES = [
  dict(slug='bonos-de-sesiones', icon='ticket', card='Bonos de sesiones',
    title='Bonos de sesiones para centros de estética y peluquerías | Godolphy',
    desc='Vende bonos de 5 o 10 sesiones en tu centro y en tu web de reservas. Cada cita descuenta una sesión sola, con avisos de caducidad y comisiones por sesión.',
    h1='Bonos de sesiones para tu centro de estética',
    lead='Cobra los tratamientos por adelantado y que tu clientela vuelva hasta terminarlos. Cada cita descuenta una sesión sola.',
    plan=PRO_MAX,
    sections=[
      ('Crea tus bonos en un minuto.', ['Elige el servicio (o varios equivalentes, como el láser de axilas y el de ingles), el número de sesiones, el precio y la caducidad. Godolphy te enseña al momento cuánto sale cada sesión.',
        'Si cambias un bono, solo afecta a las ventas nuevas: los ya vendidos mantienen sus sesiones, su precio y su caducidad.'], img('/ayuda/img/bonos-nuevo-tipo.jpg', 'Crear un tipo de bono en Godolphy')),
      ('Véndelos en el centro o en tu web.', ['En el salón, lo vendes en segundos y el cobro va a la Caja, separado de los servicios. En tu web de reservas aparece el menú Bonos: tu clientela lo compra con tarjeta y lo tiene en su perfil.',
        'Al comprarlo recibe el email «Tu bono está listo», con las sesiones y la caducidad.'], img('/ayuda/img/bonos-booking.jpg', 'Menú Bonos en la web de reservas, en el móvil', True)),
      ('Cada cita descuenta una sesión.', ['Si reserva online con su cuenta, el bono paga la sesión solo y el depósito se calcula sobre lo que queda. Desde el panel, con un clic en «Usar bono». ¿Te has equivocado? «Devolver sesión» lo deshace con su tique rectificativo.',
        'Las cancelaciones siguen tu política: si se cancela a tiempo, la sesión vuelve al bono.'], img('/ayuda/img/bonos-usar-bono.jpg', 'Pagar una cita con una sesión del bono')),
      ('Que no se pierda ninguna sesión.', ['La lista de vendidos te enseña los bonos activos, los agotados y los que caducan en 30 días. Tu clientela recibe avisos 30 y 7 días antes de que caduque.',
        'La comisión de la profesional se calcula sobre el valor de cada sesión hecha, y cada sesión genera su tique con Verifactu.'], img('/ayuda/img/bonos-vendidos.jpg', 'Lista de bonos vendidos con las sesiones que quedan')),
    ],
    seo=('Bonos de sesiones: cobra por adelantado y fideliza', [
      'Los <strong>bonos de sesiones</strong> son el formato natural para los tratamientos que se hacen en varias visitas: depilación láser, presoterapia, faciales, masajes. Quien compra un bono de 5 o 10 sesiones vuelve hasta terminarlo, y tú cobras por adelantado.',
      'Con Godolphy no necesitas tarjetas de cartón ni hojas de cálculo para saber cuántas sesiones le quedan a cada persona: el bono vive en su ficha, se descuenta solo en cada cita y avisa antes de caducar. Funciona junto a los <a href="/funcionalidades/cupones-y-tarjetas-regalo/" style="color:#631cff;font-weight:600;text-decoration:none;">cupones y las tarjetas regalo</a> y a los <a href="/funcionalidades/pagos-y-depositos/" style="color:#631cff;font-weight:600;text-decoration:none;">pagos y depósitos</a>.']),
    faq=[
      ('¿Puedo vender bonos en mi web de reservas?', 'Sí. Activa «Vender en el booking» en el tipo de bono y aparecerá el menú Bonos en tu web. Se paga con tarjeta a través de tu cuenta de Stripe.'),
      ('¿Qué pasa si cancelan una cita pagada con bono?', 'Sigue tu política de cancelación: si cancelas tú o se cancela a tiempo, la sesión vuelve al bono. Si se cancela tarde o no se presentan, la sesión se pierde.'),
      ('¿Cuánto vale cada sesión?', 'El precio del bono dividido entre sus sesiones. Ese valor es el que cuenta para el tique y para la comisión de la profesional.'),
      ('¿Qué planes incluyen los bonos?', 'Los planes Pro y Max, y la prueba gratuita de 30 días.'),
    ],
    links=[('/ayuda/crear-y-vender-bonos/', 'Crear y vender bonos'), ('/ayuda/bonos-en-el-booking/', 'Vender bonos en el booking'), ('/ayuda/usar-bono-en-una-cita/', 'Usar un bono en una cita')]),

  dict(slug='comisiones', icon='percent', card='Comisiones del equipo',
    title='Comisiones para el equipo de tu salón: fijas o por tramos | Godolphy',
    desc='Calcula cada mes las comisiones de tu equipo con un porcentaje fijo o por tramos, sobre lo cobrado de las citas completadas y sin IVA. Exporta el informe para la nómina.',
    h1='Comisiones del equipo, calculadas solas',
    lead='Godolphy calcula cada mes lo que gana cada profesional según lo cobrado de sus citas completadas. Sin hojas de cálculo ni discusiones.',
    plan=PRO_MAX,
    sections=[
      ('Porcentaje fijo o por tramos.', ['Para cada profesional eliges su sistema: un porcentaje fijo, tramos que premian a quien más factura (por ejemplo, 20 % hasta 2.000 € y 30 % a partir de ahí) o sin comisión.',
        'Tú decides si los extras y los recargos a domicilio también generan comisión.'], img('/ayuda/img/comisiones-tramos.jpg', 'Comisión por tramos de una profesional')),
      ('Reglas claras para todo el equipo.', ['Solo cuentan las citas completadas, en el mes de la cita, sobre lo cobrado sin IVA y menos las devoluciones. Las canceladas y las no presentadas no generan comisión.',
        'Si una cita completada aún no tiene el cobro apuntado, el informe te avisa para que no se quede fuera.'], img('/ayuda/img/comisiones-informe.jpg', 'Informe mensual de comisiones')),
      ('Cada profesional ve lo suyo.', ['Desde «Mis comisiones», cada profesional consulta en el móvil lo que ha generado y sus citas, sin ver los datos de nadie más. La recepcionista no ve las comisiones.',
        'Exporta el informe o el detalle de cada profesional en CSV para la nómina o la factura de una freelance.'], img('/ayuda/img/comisiones-mis-comisiones.jpg', 'Mis comisiones, visto por una profesional en el móvil', True)),
    ],
    seo=('Comisiones de peluquería y estética sin errores', [
      'Calcular las <strong>comisiones de las profesionales</strong> a mano es lento y genera dudas cada fin de mes. Godolphy lo hace solo con los datos de la agenda y de los cobros, con las mismas reglas para todo el equipo.',
      'Las sesiones de bono y lo pagado con tarjeta regalo también cuentan, y los cupones se descuentan antes de calcular. Todo encaja con tu <a href="/funcionalidades/equipo-y-horarios/" style="color:#631cff;font-weight:600;text-decoration:none;">gestión del equipo y los horarios</a>.']),
    faq=[
      ('¿Sobre qué se calcula la comisión?', 'Sobre lo cobrado de las citas completadas de cada profesional, sin IVA y menos las devoluciones, en el mes de la cita.'),
      ('¿Puedo poner comisiones por tramos?', 'Sí. Cada tramo se aplica solo a la parte que supera su importe, como en el IRPF.'),
      ('¿Las profesionales ven sus comisiones?', 'Sí, cada una en «Mis comisiones», solo con sus datos. La recepcionista no las ve.'),
      ('¿Qué planes incluyen las comisiones?', 'Los planes Pro y Max, y la prueba gratuita de 30 días.'),
    ],
    links=[('/ayuda/comisiones/', 'Comisiones de las profesionales, paso a paso'), ('/funcionalidades/equipo-y-horarios/', 'Equipo y horarios')]),

  dict(slug='gastos', icon='receipt', card='Gastos con IA',
    title='Gastos de tu salón con IA: facturas y extracto del banco | Godolphy',
    desc='Sube tus facturas en foto o PDF, o el extracto del banco en Excel o CSV, y la IA registra los gastos de tu salón. Así ves tu beneficio real cada mes.',
    h1='Tus gastos, registrados por la IA',
    lead='Haz una foto a la factura o sube el extracto del banco. Godolphy registra el gasto y te enseña tu beneficio real cada mes.',
    plan=PRO_MAX,
    sections=[
      ('Una foto y listo.', ['Sube hasta 5 facturas o tiques a la vez, en foto o PDF. La IA lee el proveedor, la fecha, la base, el IVA y propone la categoría. Tú solo revisas y guardas.',
        'El archivo original queda guardado junto al gasto, por si lo necesitas para tu gestoría.'], img('/ayuda/img/gastos-revisar-factura.jpg', 'Revisar una factura leída por la IA')),
      ('O importa el extracto del banco.', ['Sube el Excel o CSV que descargas de tu banco: Godolphy te propone los cargos con su proveedor y categoría, y deja como pendiente lo que no sabe clasificar.',
        'Si un gasto ya está apuntado, te avisa de que puede estar repetido.'], img('/ayuda/img/gastos-revisar-extracto.jpg', 'Revisar los cargos del extracto del banco')),
      ('Tu beneficio real, sin IVA.', ['Los gastos fijos (alquiler, nóminas, luz) se apuntan una vez y cuentan cada mes. Todo se suma sin IVA, repartido en cinco categorías.',
        'Con tus gastos reales, Análisis IA calcula tu beneficio, y Precios y el Plan financiero trabajan con tus números de verdad.'], img('/ayuda/img/gastos-lista.jpg', 'Gastos del mes por categoría')),
    ],
    seo=('Control de gastos para peluquerías y centros de estética', [
      'Saber cuánto facturas es fácil; saber <strong>cuánto ganas</strong> no tanto. Para eso necesitas tus gastos al día, y nadie quiere pasar facturas a mano a una hoja de cálculo.',
      'Con Godolphy, los gastos viven en el mismo sitio que tu agenda y tus cobros. Así el beneficio sale solo en <a href="/funcionalidades/facturacion-y-reporte/" style="color:#631cff;font-weight:600;text-decoration:none;">tus informes</a>, en la <a href="/funcionalidades/calculadora-de-precios/" style="color:#631cff;font-weight:600;text-decoration:none;">calculadora de precios</a> y en tu <a href="/funcionalidades/plan-financiero/" style="color:#631cff;font-weight:600;text-decoration:none;">plan financiero</a>.']),
    faq=[
      ('¿Qué puede leer la IA?', 'Facturas y tiques en foto o PDF (hasta 5 a la vez) y extractos del banco en Excel o CSV.'),
      ('¿Los gastos cuentan con IVA?', 'No. Para el beneficio cuenta la base, sin IVA.'),
      ('¿Tengo que subir el alquiler cada mes?', 'No. Márcalo como gasto que se repite cada mes y contará todos los meses.'),
      ('¿Qué planes incluyen Gastos?', 'Los planes Pro y Max, y la prueba gratuita de 30 días.'),
    ],
    links=[('/ayuda/gastos/', 'Gastos, paso a paso'), ('/funcionalidades/calculadora-de-precios/', 'Calculadora de precios'), ('/funcionalidades/plan-financiero/', 'Plan financiero')]),

  dict(slug='calculadora-de-precios', icon='tag', card='Calculadora de precios',
    title='Calculadora de precios para tu salón: coste real y margen | Godolphy',
    desc='Descubre cuánto te cuesta de verdad cada servicio con tus horarios, tus citas y tus gastos, qué servicios te hacen perder dinero y qué precio cobrar para ganar el margen que quieres.',
    h1='¿Cuánto te cuesta de verdad cada servicio?',
    lead='Godolphy calcula el coste real de cada servicio con tus datos y te dice qué precio cobrar para ganar el margen que quieres.',
    plan=PRO_MAX,
    sections=[
      ('Con tus números, no con medias.', ['El coste por hora del equipo, los costes fijos del local y tu ocupación salen de tus horarios, tus citas y tus gastos. Cada dato te dice de dónde viene, y puedes cambiarlo.',
        'Añade el coste de producto de cada servicio para afinar el cálculo.'], img('/ayuda/img/precios-resumen.jpg', 'Precios: tus números y los servicios a revisar')),
      ('Descubre lo que te hace perder dinero.', ['Cada servicio muestra lo que te cuesta, su margen y su beneficio, con una etiqueta: Pierdes dinero, Por debajo de tu margen o Bien. Muchas veces son los servicios cortos y los extras.',
        'Tú decides el margen que quieres: en general o para cada servicio.'], img('/ayuda/img/precios-producto-margen.jpg', 'Coste de producto y margen de un servicio')),
      ('Cambia el precio con un clic.', ['Si estás de acuerdo con el precio recomendado, pulsa «Aplicar». Godolphy te pide confirmación y actualiza tu catálogo y tu web de reservas. Las citas ya reservadas mantienen su precio.'], img('/ayuda/img/precios-resumen.jpg', 'Precio recomendado de cada servicio')),
    ],
    seo=('Cómo calcular el precio de tus servicios de belleza', [
      'Poner precios mirando a la competencia es arriesgado: tu alquiler, tu equipo y tu ocupación no son los suyos. La <strong>calculadora de precios</strong> de Godolphy reparte tus costes reales entre las horas de servicio y te dice cuánto cuesta cada uno.',
      'Funciona mejor con tus <a href="/funcionalidades/gastos/" style="color:#631cff;font-weight:600;text-decoration:none;">gastos con IA</a> apuntados. Si quieres saber más, lee <a href="/como-calcular-los-precios-de-mis-servicios-de-belleza/" style="color:#631cff;font-weight:600;text-decoration:none;">cómo calcular los precios de tus servicios de belleza</a>.']),
    faq=[
      ('¿De dónde salen los costes?', 'De tus horarios, tus citas y tus gastos de los últimos tres meses completos. Puedes cambiar cualquier dato a mano.'),
      ('¿Cómo se redondea el precio recomendado?', 'Hacia arriba, a 0,50 €, con IVA incluido.'),
      ('¿Cambia el precio de las citas ya reservadas?', 'No. «Aplicar» solo cambia el precio a partir de ahora, en tu catálogo y tu web de reservas.'),
      ('¿Qué planes incluyen la calculadora?', 'Los planes Pro y Max, y la prueba gratuita de 30 días.'),
    ],
    links=[('/ayuda/precios/', 'Precios, paso a paso'), ('/funcionalidades/gastos/', 'Gastos con IA'), ('/funcionalidades/precio-por-dia-y-hora/', 'Precio según día y hora')]),

  dict(slug='plan-financiero', icon='chart', card='Plan financiero',
    title='Plan financiero para tu salón: objetivos y real vs plan | Godolphy',
    desc='Crea un plan financiero a partir de tus datos reales: citas, facturación y gastos mes a mes. Compara cada mes lo previsto con lo real, con CAC, LTV y caja.',
    h1='Tu plan financiero, mes a mes',
    lead='Fija tus objetivos de citas, facturación y gastos, y mira cada día cómo vas de verdad.',
    plan=PRO_MAX,
    sections=[
      ('Un plan hecho con tus datos.', ['Godolphy propone cada mes a partir de tus citas reales, respetando la temporada, y de tus gastos. Tú decides cuánto quieres crecer.',
        'Después ajustas lo que quieras: citas, clientela que repite, facturación, cada gasto y la inversión.'], img('/ayuda/img/plan-financiero-proponer.jpg', 'Proponer el plan con un porcentaje de crecimiento')),
      ('Plan, real y diferencia.', ['Abre cualquier mes y compara lo previsto con lo que pasa de verdad: citas, clientela nueva, ticket medio, facturación, gastos y beneficio.',
        'Con los indicadores que usan los negocios que crecen: lo que te cuesta cada cliente nuevo (CAC), lo que vale un cliente al año (LTV) y la caja acumulada.'], img('/ayuda/img/plan-financiero-mes.jpg', 'Plan, real y diferencia del mes')),
      ('Y en tu panel, cada día.', ['La tarjeta «Este mes: real vs plan» de Análisis IA te dice cuánto llevas de facturación, beneficio y citas. Si vas por debajo, el gestor diario te lo recuerda.'], img('/ayuda/img/plan-financiero-objetivos.jpg', 'Objetivos de un mes')),
    ],
    seo=('Plan financiero para centros de estética y peluquerías', [
      'Un <strong>plan financiero</strong> no tiene por qué ser un Excel que nadie mira. En Godolphy se crea con tus datos reales y se compara solo, cada día, con lo que pasa en tu salón.',
      'Se alimenta de tu agenda, tus cobros y tus <a href="/funcionalidades/gastos/" style="color:#631cff;font-weight:600;text-decoration:none;">gastos</a>. Si estás empezando, te ayuda también nuestra guía para <a href="/abrir-centro-de-estetica-en-espana/" style="color:#631cff;font-weight:600;text-decoration:none;">abrir un centro de estética en España</a>.']),
    faq=[
      ('¿Necesito historial para crear el plan?', 'No. Si aún no tienes historial, rellenas tú los objetivos de cada mes.'),
      ('¿Qué periodo cubre?', 'El año natural. Si lo creas a partir de septiembre, cubre lo que queda de año y todo el siguiente.'),
      ('¿Por qué la facturación va con IVA?', 'Es lo que cobras. Los gastos y el beneficio se calculan sin IVA.'),
      ('¿Qué planes incluyen el plan financiero?', 'Los planes Pro y Max, y la prueba gratuita de 30 días.'),
    ],
    links=[('/ayuda/plan-financiero/', 'Plan financiero, paso a paso'), ('/funcionalidades/gastos/', 'Gastos con IA'), ('/funcionalidades/gestor-diario/', 'Gestor diario')]),

  dict(slug='gestor-diario', icon='bulb', card='Gestor diario',
    title='Gestor diario para tu salón: qué hacer hoy para ganar más | Godolphy',
    desc='Cada mañana, Godolphy revisa tu salón y te propone hasta tres cosas que hacer hoy: citas sin cobrar, huecos en la agenda, clientela que no vuelve, precios o gastos.',
    h1='Cada mañana, lo que tienes que hacer hoy',
    lead='Godolphy revisa tu salón y te propone hasta tres recomendaciones al día, en el panel y por email a las 8:00.',
    plan='Incluido en todos los planes. En Pro y Max, con recomendaciones de negocio.',
    sections=[
      ('Tres recomendaciones, ni una más.', ['Por orden de importancia y sacadas de tus datos: no se inventa nada. Si no hay nada importante, no te escribimos.',
        'Cada recomendación lleva un enlace para resolverla al momento.'], img('/ayuda/img/gestor-hoy-te-recomendamos.jpg', 'Hoy te recomendamos, en el inicio del panel')),
      ('Lo que te hace ganar dinero hoy.', ['En todos los planes: citas sin cobrar de los últimos 30 días, huecos de una hora o más en la agenda de mañana y clientela habitual que no vuelve.',
        'En Pro y Max, además: servicios que te hacen perder dinero, un mes por debajo del plan y gastos que suben.'], img('/ayuda/img/gestor-hoy-te-recomendamos.jpg', 'Recomendaciones del día')),
    ],
    seo=('Un gestor para tu salón, cada día', [
      'Los datos sirven de poco si nadie los mira. El <strong>gestor diario</strong> de Godolphy los mira por ti y te dice lo importante en tres líneas, antes de abrir.',
      'Se apoya en tu agenda, tus cobros, tu <a href="/funcionalidades/calculadora-de-precios/" style="color:#631cff;font-weight:600;text-decoration:none;">calculadora de precios</a> y tu <a href="/funcionalidades/plan-financiero/" style="color:#631cff;font-weight:600;text-decoration:none;">plan financiero</a>, y se complementa con la <a href="/funcionalidades/fidelizacion-ai/" style="color:#631cff;font-weight:600;text-decoration:none;">fidelización con IA</a>.']),
    faq=[
      ('¿Cuándo llegan las recomendaciones?', 'Las ves en el inicio del panel y te llegan por email a las 8:00, si hay algo que recomendar.'),
      ('¿Puedo dejar de recibir el email?', 'Sí, con el enlace para darte de baja del pie del email.'),
      ('¿Qué incluye cada plan?', 'Todos los planes reciben las recomendaciones de agenda, cobros y clientela. Pro y Max, también las de precios, plan y gastos.'),
    ],
    links=[('/ayuda/gestor-diario/', 'Hoy te recomendamos, paso a paso'), ('/funcionalidades/plan-financiero/', 'Plan financiero')]),

  dict(slug='precio-por-dia-y-hora', icon='clock', card='Precio según día y hora',
    title='Precio según día y hora: más caro en fin de semana, descuento en horas valle | Godolphy',
    desc='Sube o baja el precio de tus servicios según el día y la hora de la cita: un recargo los sábados por la mañana o un descuento para llenar las horas flojas.',
    h1='Cobra más en las horas que más se piden',
    lead='Pon un recargo o un descuento automático según el día y la hora de la cita. Tu clientela ve el precio final al reservar.',
    plan=PRO_MAX,
    sections=[
      ('Recargos y descuentos por franja.', ['Por ejemplo, +10 % los sábados de 9:00 a 14:00 o −15 % los martes por la tarde para llenar las horas flojas. Eliges los días, las horas y el porcentaje.',
        'Cada franja se puede editar, desactivar o eliminar cuando quieras.'], img('/ayuda/img/precio-dia-hora-lista.jpg', 'Franjas de precio según día y hora')),
      ('Precio final, sin sorpresas.', ['Al elegir la hora en tu web de reservas, se ve directamente el precio final, sin etiquetas ni precios tachados. El porcentaje se aplica a cada servicio y cada extra.',
        'Las citas ya reservadas no cambian.'], img('/ayuda/img/precio-dia-hora-booking.jpg', 'Precio con descuento en la web de reservas', True)),
    ],
    seo=('Precios dinámicos para peluquerías y centros de estética', [
      'Los sábados por la mañana se llenan solos; los martes por la tarde, no. Con el <strong>precio según día y hora</strong> puedes cobrar un poco más cuando hay más demanda y ofrecer un descuento en las horas valle.',
      'Se configura en minutos y convive con los <a href="/funcionalidades/servicios-a-domicilio/" style="color:#631cff;font-weight:600;text-decoration:none;">recargos a domicilio</a> y los <a href="/funcionalidades/cupones-y-tarjetas-regalo/" style="color:#631cff;font-weight:600;text-decoration:none;">cupones</a>.']),
    faq=[
      ('¿Mi clientela ve que hay un recargo?', 'Ve directamente el precio final al elegir la hora, sin etiquetas.'),
      ('¿Se aplica a las citas ya reservadas?', 'No. Solo a las nuevas o a las que muevas a otra hora desde el panel.'),
      ('¿Qué límites tiene?', 'Entre −90 % y +100 %, y las franjas activas no pueden solaparse.'),
      ('¿Qué planes lo incluyen?', 'Los planes Pro y Max, y la prueba gratuita de 30 días.'),
    ],
    links=[('/ayuda/precio-segun-dia-y-hora/', 'Precio según día y hora, paso a paso'), ('/funcionalidades/calculadora-de-precios/', 'Calculadora de precios')]),

  dict(slug='vacaciones-y-ausencias', icon='plane', card='Vacaciones y ausencias',
    title='Vacaciones y bajas del equipo sin llamar a nadie | Godolphy',
    desc='Marca las vacaciones, una baja o un permiso y resuelve las citas afectadas en un momento: pásalas a otra persona del equipo o envía un enlace para que cada cliente elija.',
    h1='Vacaciones y bajas, sin llamar a nadie',
    lead='Marca la ausencia y resuelve sus citas en un momento: pásalas a otra persona o deja que cada cliente elija.',
    plan='Incluido en todos los planes.',
    sections=[
      ('Marca los días y listo.', ['Vacaciones, baja, permiso o un día libre: eliges las fechas y, desde ese momento, nadie puede reservar con esa persona.'], img('/ayuda/img/ausencias-anadir.jpg', 'Añadir una ausencia')),
      ('Las citas afectadas, resueltas.', ['Si ya tenía citas, Godolphy te las enseña. Pásalas a otra persona libre a la misma hora, con el mismo precio, o envía un enlace por email y WhatsApp.',
        'Con el enlace, cada cliente elige otra persona, otro día u hora, o cancela sin coste. Si no responde, 24 horas antes Godolphy la pasa a quien esté libre o la cancela y lo devuelve todo.'], img('/ayuda/img/ausencias-citas-afectadas.jpg', 'Citas afectadas por una ausencia')),
      ('Y si alguien deja el equipo.', ['Antes de desactivar su ficha, Godolphy te pide decidir qué pasa con sus citas futuras. Después, puedes enviar un email a su clientela habitual para que siga reservando con el resto del equipo.'], img('/ayuda/img/desactivar-citas-pendientes.jpg', 'Desactivar a una persona del equipo')),
    ],
    seo=('Gestionar las vacaciones del equipo de tu salón', [
      'Las <strong>vacaciones y las bajas</strong> son el momento en que más clientela se pierde: citas que nadie recoloca, llamadas que no llegan. Godolphy convierte ese trabajo en un par de clics.',
      'Todo encaja con los <a href="/funcionalidades/equipo-y-horarios/" style="color:#631cff;font-weight:600;text-decoration:none;">horarios del equipo</a> y las <a href="/funcionalidades/chat-y-notificaciones/" style="color:#631cff;font-weight:600;text-decoration:none;">notificaciones por WhatsApp</a>.']),
    faq=[
      ('¿Cambia el precio si paso la cita a otra persona?', 'No. El precio se mantiene y se avisa del cambio a quien reservó y a la nueva profesional.'),
      ('¿Hace falta iniciar sesión para usar el enlace?', 'No. Cada cliente elige desde el enlace sin iniciar sesión.'),
      ('¿Qué pasa con las citas ya cobradas?', 'Lo pagado online y los bonos se devuelven solos. Si se cancela una cita cobrada en el salón, te avisamos por email para que devuelvas el importe.'),
    ],
    links=[('/ayuda/ausencias-del-equipo/', 'Ausencias del equipo, paso a paso'), ('/ayuda/desactivar-profesional/', 'Desactivar a una persona del equipo'), ('/funcionalidades/equipo-y-horarios/', 'Equipo y horarios')]),

  dict(slug='importar-datos', icon='upload', card='Importa tus datos',
    title='Cambia de software sin empezar de cero: importa servicios y equipo | Godolphy',
    desc='Importa tus servicios y tu equipo desde Excel, una captura de pantalla o el enlace de tu ficha en Treatwell, Booksy o Fresha. La IA lo lee y tú solo revisas.',
    h1='Cambia a Godolphy sin empezar de cero',
    lead='Trae tus servicios y tu equipo desde un Excel, una captura o el enlace de tu ficha en Treatwell, Booksy o Fresha.',
    plan='Incluido en todos los planes.',
    sections=[
      ('Tus servicios, en un minuto.', ['Pega el enlace de tu ficha en Treatwell, Booksy, Fresha o de tu web, sube capturas de tu lista o un Excel. La IA lee el nombre, el precio, la duración y la categoría.',
        'Nada se guarda hasta que lo revisas, y la IA no se inventa nada: lo que no puede leer lo deja vacío.'], img('/ayuda/img/servicios-importar-revisar.jpg', 'Revisar los servicios importados')),
      ('Y tu equipo, también.', ['Sube un Excel o una captura con tu equipo: la IA lee nombres, emails, teléfonos, locales y servicios. Al importar, cada profesional recibe su acceso al panel.'], img('/ayuda/img/equipo-nuevo-profesional.jpg', 'Equipo en Godolphy')),
    ],
    seo=('Migrar desde Treatwell, Booksy o Fresha', [
      'El miedo a <strong>cambiar de software</strong> suele ser volver a escribir todo. Con Godolphy, tus servicios y tu equipo se importan en minutos y los revisas antes de guardar.',
      'Si vienes de otra plataforma, mira nuestras comparativas: <a href="/alternativa-a-treatwell/" style="color:#631cff;font-weight:600;text-decoration:none;">alternativa a Treatwell</a> y <a href="/alternativa-a-booksy/" style="color:#631cff;font-weight:600;text-decoration:none;">alternativa a Booksy</a>.']),
    faq=[
      ('¿Desde dónde puedo importar mis servicios?', 'Desde un Excel o CSV (con plantilla o tu propio archivo), capturas de pantalla o el enlace de tu ficha en Treatwell, Booksy, Fresha o tu web.'),
      ('¿Se importan los horarios del equipo?', 'No. Después de importar, configura el horario de cada profesional.'),
      ('¿Tiene coste?', 'No. La importación está incluida en todos los planes.'),
    ],
    links=[('/ayuda/importar-servicios/', 'Importar servicios'), ('/ayuda/importar-equipo/', 'Importar el equipo')]),
  dict(slug='caja-y-cobros', icon='cash', card='Cobros y cierre de caja',
    title='Cobros en el salón y cierre de caja | Godolphy',
    desc='Cobra cada cita en efectivo, TPV, Bizum o con la tarjeta guardada, divide el pago, imprime o envía el tique y cierra la caja cada día comparando lo esperado con lo contado.',
    h1='Cobra en el salón y cierra la caja en minutos',
    lead='Apunta cada cobro en su cita, con el medio real, y al final del día cierra la caja sabiendo exactamente qué tiene que haber.',
    plan='Incluido en todos los planes.',
    sections=[
      ('Cobra cada cita en segundos.', ['Desde la cita, en efectivo, TPV, Bizum, transferencia o con la tarjeta que se guardó al reservar online. Si paga con dos medios, repartes el importe; si paga una parte, el resto queda pendiente.',
        'Cada cobro tiene su tique para imprimirlo o enviarlo por email.'], img('/ayuda/img/ventas-detalle-cobros.jpg', 'Cobros de una cita en Godolphy')),
      ('Devoluciones sin líos.', ['Devuelve un cobro hecho en el salón, entero o una parte, o reembolsa un pago online: Stripe devuelve el dinero a la tarjeta.',
        'Con <a href="/verifactu/" style="color:#631cff;font-weight:600;text-decoration:none;">Verifactu</a>, cada cobro y cada devolución genera su tique con QR enviado a Hacienda.'], img('/ayuda/img/verifactu-tique.jpg', 'Tique con código QR de Verifactu')),
      ('Una caja que cuadra cada día.', ['Apunta las entradas y retiradas de efectivo, como el fondo inicial o un pago a un proveedor. Al cerrar, escribe el efectivo contado y verás al momento la diferencia con lo esperado.',
        'El informe de cierre se descarga en CSV o se imprime. Un cierre hecho ya no se puede modificar.'], img('/ayuda/img/ventas-caja.jpg', 'Caja del día y cierre de caja')),
    ],
    seo=('Cobros y cierre de caja para peluquerías y centros de estética', [
      'Un <strong>cierre de caja</strong> que no cuadra suele venir de cobros que no se apuntaron o de salidas de efectivo olvidadas. Con Godolphy, cada cobro queda en su cita y la caja sabe qué debería haber en cada medio de pago.',
      'Godolphy no se conecta a ningún datáfono: cobras con el TPV de tu banco como siempre, lo apuntas en la cita en un clic y en el cierre lo comparas con lo que dice el datáfono. Los depósitos y los pagos online van aparte, con <a href="/funcionalidades/pagos-y-depositos/" style="color:#631cff;font-weight:600;text-decoration:none;">pagos y depósitos</a>.']),
    faq=[
      ('¿Qué medios de pago puedo usar?', 'Vienen Efectivo, TPV, Bizum y Transferencia, y puedes añadir los tuyos. También puedes cobrar con la tarjeta que se guardó al reservar online.'),
      ('¿Godolphy se conecta con mi datáfono?', 'No. Cobras con tu datáfono como siempre y apuntas el cobro en la cita. En el cierre de caja comparas lo apuntado con lo que dice el datáfono.'),
      ('¿Se puede modificar un cierre de caja?', 'No. Un cierre hecho no se modifica, y los movimientos de caja no se borran: se anulan con un movimiento contrario.'),
      ('¿Qué planes lo incluyen?', 'Todos los planes.'),
    ],
    links=[('/ayuda/ventas-y-reembolsos/', 'Cobrar una cita y hacer devoluciones'), ('/ayuda/cierre-de-caja/', 'Caja: entradas, retiradas y cierre'), ('/ayuda/cobrar-con-tarjeta/', 'Cobrar con tarjeta'), ('/verifactu/', 'Verifactu')]),

  dict(slug='recepcionista-y-permisos', icon='users', card='Recepcionista y permisos',
    title='Recepcionista y permisos del equipo de tu salón | Godolphy',
    desc='Da a cada persona su propio acceso: la recepcionista gestiona la agenda, las citas, los clientes, los cobros y la caja sin tocar la configuración, y cada profesional ve solo su agenda.',
    h1='Cada persona, su acceso',
    lead='Invita a tu recepcionista y da acceso a tu equipo sin compartir contraseñas. Cada persona ve solo lo que necesita.',
    plan='Incluido en todos los planes.',
    sections=[
      ('Tres tipos de usuario.', ['Cada persona entra con su propio email y contraseña, y lo que ve depende de su tipo de usuario.',
        'Así nadie toca la configuración por error, y puedes quitar un acceso sin cambiar el tuyo.'], roles_card()),
      ('Una recepcionista que no toca la configuración.', ['Gestiona la agenda, las citas, los clientes, los cobros y la caja. No ve la configuración del salón ni las comisiones, y no puede borrar datos.',
        'La invitas con su email desde Configuración → Equipo y le llega un enlace para crear su contraseña. Si deja de trabajar contigo, le quitas el acceso en un clic.'], img('/ayuda/img/calendario-diario.jpg', 'Calendario del panel de Godolphy')),
      ('Cada profesional, su agenda.', ['Al darla de alta, cada profesional recibe un email para entrar con su propio usuario. Ve sus citas en el calendario y su perfil, sin ver tus clientes, tus ventas ni la configuración.',
        'Los cambios de citas pasan por ti o por recepción, así nadie toca la misma cita a la vez.'], img('/ayuda/img/equipo-nuevo-profesional.jpg', 'Alta de una profesional en el equipo')),
    ],
    seo=('Permisos del equipo en peluquerías y centros de estética', [
      'Compartir una contraseña entre todo el equipo es cómodo hasta el día que alguien cambia algo por error o deja el salón. Con <strong>usuarios y permisos</strong> separados, cada persona entra con su acceso y tú decides qué ve.',
      'Encaja con la <a href="/funcionalidades/equipo-y-horarios/" style="color:#631cff;font-weight:600;text-decoration:none;">gestión del equipo y los horarios</a>, los <a href="/funcionalidades/caja-y-cobros/" style="color:#631cff;font-weight:600;text-decoration:none;">cobros y la caja</a> y las <a href="/funcionalidades/comisiones/" style="color:#631cff;font-weight:600;text-decoration:none;">comisiones</a>.']),
    faq=[
      ('¿Puede haber más de una recepcionista?', 'Sí. Invita a cada persona con su email desde Configuración → Equipo.'),
      ('¿Qué no puede hacer la recepcionista?', 'Cambiar la configuración del salón, borrar datos ni ver las comisiones.'),
      ('¿Las profesionales pueden mover citas?', 'No. Consultan sus citas; los cambios los haces tú o la recepcionista desde el calendario.'),
      ('¿Tiene coste?', 'No. Está incluido en todos los planes.'),
    ],
    links=[('/ayuda/usuarios-y-permisos/', 'Usuarios y permisos'), ('/ayuda/recepcionista/', 'Invitar a una recepcionista'), ('/ayuda/acceso-de-las-profesionales/', 'Qué ve una profesional')]),
]


def faq_block(faq):
    items = []
    for q, a in faq:
        items.append('<div class="faq-item"><button class="faq-btn" onclick="toggleFaq(this)"><span style="color:#02021e;font-size:17px;font-weight:600;">'
                     + html.escape(q) + '</span><svg class="faq-icon" width="20" height="20" fill="none" stroke="#631cff" stroke-width="2.5" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg></button>'
                     '<div class="faq-body"><p style="color:rgba(2,2,30,.65);font-size:16px;line-height:1.65;margin:0;">' + html.escape(a) + '</p></div></div>')
    return ('<section style="background:#fff;padding:96px 40px;"><div style="max-width:780px;margin:0 auto;"><div style="text-align:center;margin-bottom:56px;"><h2 class="font-gabarito" style="background:linear-gradient(90deg,#9B4FE8,#631cff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-size:42px;font-weight:700;margin:0;">Preguntas frecuentes</h2></div>\n'
            + '\n'.join(items) + '\n</div></section>\n<script>function toggleFaq(btn){var body=btn.nextElementSibling;var icon=btn.querySelector(".faq-icon");body.classList.toggle("open");icon.classList.toggle("open");}</script>')


def main_html(p):
    secs = []
    for i, (h2, paras, image) in enumerate(p['sections']):
        alt = ' alt' if i % 2 else ''
        rev = ' rev' if i % 2 else ''
        ps = ''.join(f'<p>{t}</p>' for t in paras)
        secs.append(f'<section class="feat-section{alt}">\n  <div class="feat-content{rev}">\n    <div class="feat-text">\n      <h2>{h2}</h2>\n      {ps}\n    </div>\n    {image}\n  </div>\n</section>')
    seo_h, seo_ps = p['seo']
    seo = ''.join(f'<p style="color:rgba(2,2,30,.75);font-size:17px;line-height:1.75;margin:0 0 20px;">{t}</p>' for t in seo_ps)
    chips = ''.join(CHIP.format(href=h, text=html.escape(t)) for h, t in p['links'])
    return f'''<main>
<section class="hero-bg" style="position:relative;padding:130px 40px 100px;text-align:center;overflow:hidden;">
  <div style="display:inline-flex;align-items:center;justify-content:center;width:72px;height:72px;background:rgba(255,255,255,.15);border-radius:20px;margin-bottom:28px;">
    <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[p['icon']]}</svg>
  </div>
  <h1 class="font-gabarito" style="color:#fff;font-size:56px;font-weight:700;margin:0 auto 20px;line-height:1.05;max-width:960px;">{p['h1']}</h1>
  <p style="color:rgba(255,255,255,.85);font-size:20px;line-height:1.6;max-width:680px;margin:0 auto;">{p['lead']}</p>
  <div style="margin-top:36px;display:flex;gap:16px;justify-content:center;flex-wrap:wrap;">
    <a href="{SIGNUP}" style="background:#EEFE3A;color:#02021e;font-size:16px;font-weight:700;padding:14px 36px;border-radius:20px;text-decoration:none;">Prueba gratis 30 días</a>
  </div>
  <p style="color:rgba(255,255,255,.7);font-size:14px;margin:22px 0 0;">{p['plan']}</p>
  <div style="position:absolute;bottom:-1px;left:0;right:0;line-height:0;"><svg viewBox="0 0 1440 60" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" style="display:block;width:100%;height:60px;"><path d="M0,30 C360,60 1080,0 1440,30 L1440,60 L0,60 Z" fill="#fff"/></svg></div>
</section>

{chr(10).join(secs)}

<section style="background:#f8f7ff;padding:80px 40px;"><div style="max-width:900px;margin:0 auto;background:linear-gradient(160deg,#9B4FE8 0%,#7835C3 30%,#631cff 65%,#3a0aaa 100%);border-radius:32px;padding:80px 60px;text-align:center;"><h2 class="font-gabarito" style="color:#fff;font-size:46px;line-height:1.1;font-weight:700;margin:0 0 20px;">Empieza gratis hoy mismo</h2><p style="color:rgba(255,255,255,.85);font-size:18px;line-height:1.6;max-width:560px;margin:0 auto 40px;">Sin tarjeta de crédito. Sin permanencia. 30 días para probar todo el potencial de Godolphy.</p><div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;"><a href="{SIGNUP}" style="background:#EEFE3A;color:#02021e;font-size:18px;font-weight:700;padding:16px 40px;border-radius:20px;text-decoration:none;">Prueba gratis 30 días</a></div><p style="color:rgba(255,255,255,.6);font-size:14px;margin:20px 0 0;">30 días gratis · Sin tarjeta de crédito</p></div></section>

<section style="background:#fff;padding:80px 40px 20px;">
  <div style="max-width:780px;margin:0 auto;">
    <h2 class="font-gabarito" style="font-size:32px;font-weight:700;color:#02021e;margin:0 0 24px;">{seo_h}</h2>
    {seo}
  </div>
</section>

{faq_block(p['faq'])}

<section style="background:#fff;padding:20px 40px 90px;"><div style="max-width:780px;margin:0 auto;">
  <h2 class="font-gabarito" style="font-size:26px;color:#02021e;margin:0 0 20px;">Sigue leyendo</h2>
  <div style="display:flex;flex-wrap:wrap;gap:10px;">{chips}</div>
</div></section>
</main>'''


def build_page(chrome, p):
    url = f"{BASE}/funcionalidades/{p['slug']}/"
    s = chrome
    s = re.sub(r'<title>.*?</title>', f"<title>{html.escape(p['title'])}</title>", s, count=1, flags=re.S)
    s = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + html.escape(p['desc']), s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + html.escape(p['title']), s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + html.escape(p['desc']), s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*"\s*/?>\s*', '', s)
    s = s.replace('<meta property="og:description"', f'<meta property="og:url" content="{url}" />\n  <meta property="og:description"', 1)
    # JSON-LD: keep SoftwareApplication, replace the rest
    lds = re.findall(r'<script type="application/ld\+json">.*?</script>\s*', s, flags=re.S)
    keep = [x for x in lds if '"SoftwareApplication"' in x]
    s = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', '', s, flags=re.S)
    ld = [
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p['faq']]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Funcionalidades", "item": BASE + "/funcionalidades/"},
            {"@type": "ListItem", "position": 3, "name": p['card'], "item": url}]},
    ]
    s = s.replace('</head>', ''.join(keep) + ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld) + '</head>', 1)
    s = re.sub(r'<main>.*?</main>', lambda m: main_html(p), s, count=1, flags=re.S)
    os.makedirs(f"funcionalidades/{p['slug']}", exist_ok=True)
    open(f"funcionalidades/{p['slug']}/index.html", 'w', encoding='utf-8').write(s)
    return url


if __name__ == '__main__':
    chrome = open(SRC, encoding='utf-8').read()
    for p in PAGES:
        print('ok', build_page(chrome, p))
