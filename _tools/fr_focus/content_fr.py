# -*- coding: utf-8 -*-
# Contenu FR des pages pour acheteurs français. Même structure que content_es.py.
FECHA = "octobre 2026"

PAGES = {}

PAGES["g1"] = dict(
    kind="guia",
    slug="guias/comprar-barco-espana-matricular-francia.html",
    crumb=("Guides", "/fr/guias/"),
    title="Acheter un bateau en Espagne et l'immatriculer en France : le guide étape par étape",
    desc="Vous vivez en France et vous avez trouvé un bateau en Espagne ? Les impôts à payer ici, la radiation du registre espagnol, comment le rapatrier et les papiers que demande la France pour l'immatriculer.",
    eyebrow="Guides · Acheter depuis la France",
    h1="Acheter un bateau en Espagne et l'immatriculer en France",
    meta=["Par Juan Morante", "Mis à jour en octobre 2026", "8 min de lecture"],
    lead="De plus en plus de personnes qui vivent en France cherchent un bateau en Catalogne. L'achat se fait sans problème, mais il y a deux pays et deux administrations, et il vaut mieux faire les choses dans l'ordre. Je vous explique ici tout le parcours : ce qu'il faut vérifier avant de payer, ce qui se paie en Espagne, comment le bateau est radié du registre espagnol et ce que demande la France pour l'immatriculer.",
    toc=[("antes", "Avant de payer : ce qu'il faut vérifier"), ("impuestos", "Les impôts en Espagne"), ("baja", "La radiation du registre espagnol"), ("llevarlo", "Comment rapatrier le bateau en France"), ("francia", "L'immatriculer en France"), ("despues", "Ensuite : taxe annuelle et permis"), ("riesgos", "Les risques les plus courants"), ("faq", "Questions fréquentes")],
    body="""
<h2 id="antes">Avant de payer : ce qu'il faut vérifier</h2>
<p>Ce qui pose le plus de problèmes dans un achat entre deux pays, ce n'est pas la paperasse, c'est de découvrir trop tard que quelque chose ne colle pas. Avant de verser le moindre acompte, demandez et vérifiez ceci :</p>
<ul>
<li><strong>Qui est le propriétaire.</strong> La personne qui vous vend doit être le propriétaire qui figure sur les documents du bateau, ou avoir un pouvoir pour vendre.</li>
<li><strong>Les charges.</strong> Le bateau ne doit avoir ni hypothèque ni saisie. Cela se vérifie au Registro de Bienes Muebles (le registre espagnol des biens meubles). S'il y avait un créancier, son autorisation serait nécessaire pour radier le bateau.</li>
<li><strong>La TVA.</strong> Le bateau doit avoir la TVA acquittée dans l'Union européenne. Le plus courant est de demander la facture de la première vente. Pour l'immatriculer en France, on vous demandera de le justifier, surtout s'il mesure plus de 7,5 mètres.</li>
<li><strong>Le pavillon actuel.</strong> Si le bateau est sous pavillon espagnol, la radiation se demande en Espagne. S'il a un autre pavillon (par exemple polonais), la radiation se demande au registre de ce pays, et c'est une démarche différente.</li>
<li><strong>Les moteurs.</strong> Les numéros de série des moteurs doivent correspondre aux papiers. La France demande aussi la facture ou le document d'achat des moteurs.</li>
<li><strong>Déclaration de conformité CE.</strong> La France la demande pour immatriculer. Les bateaux mis sur le marché européen avant le 16 juin 1998 n'en ont pas et passent par un autre document.</li>
</ul>
<p>Mon conseil : faire l'<strong>essai en mer et l'expertise avant de verser l'acompte</strong>, ou verser l'acompte à condition que l'expertise soit bonne. Je l'explique dans le <a href="/fr/guias/arras-compraventa-barco.html">guide de l'acompte (arras)</a>.</p>

<h2 id="impuestos">Les impôts en Espagne</h2>
<p>Cela dépend de qui vous vend le bateau :</p>
<ul>
<li><strong>Si c'est un particulier</strong>, on paie l'impôt sur les transmissions patrimoniales (ITP). Si vous n'êtes pas résident en Espagne, il ne se paie pas à la Catalogne mais à l'Agencia Tributaria de l'État : le taux est de <strong>4 %</strong>, il se déclare avec le <strong>modelo 620</strong> pour non-résidents et vous avez <strong>30 jours ouvrables</strong> à compter de la signature du contrat. Il se calcule sur le prix, ou sur la valeur du barème du fisc espagnol si elle est plus élevée.</li>
<li><strong>Si c'est une entreprise</strong>, l'opération est soumise à la TVA au lieu de l'ITP : pour un bateau d'occasion, normalement la TVA espagnole (IVA). Si le vendeur applique le régime spécial des biens d'occasion, la TVA est incluse dans le prix et n'apparaît pas en détail ; demandez que la facture l'indique, car c'est votre preuve de TVA face à la France.</li>
<li><strong>Bateau « neuf » :</strong> s'il mesure plus de 7,5 mètres et qu'il est livré dans les 3 mois suivant sa première mise en service ou avec moins de 100 heures de navigation, la loi le considère comme un moyen de transport neuf et la TVA se paie en France, pas en Espagne.</li>
</ul>
<p>Pour déclarer et faire les démarches en Espagne, on vous demandera normalement un <strong>NIE</strong> (numéro d'identification d'étranger). Mieux vaut le demander à l'avance.</p>
<p>Si vous achetez en étant résident en Espagne, l'ITP est celui de votre communauté autonome : vous l'avez dans le <a href="/fr/guias/itp-comprar-barco-usado-por-comunidad.html">guide de l'ITP par communauté</a>.</p>

<h2 id="baja">La radiation du registre espagnol</h2>
<p>Pour immatriculer le bateau en France, il doit d'abord sortir du registre espagnol. Cela se demande à la <strong>Capitainerie maritime espagnole (Capitanía Marítima)</strong> sous forme de <strong>radiation pour exportation</strong> (définitive ou provisoire), avec le formulaire de plaisance et la taxe correspondante (modelo 790-025). On fournit la fiche d'inscription au registre (hoja de asiento), le document de vente, l'autorisation des créanciers s'il y en a et, si le bateau a un MMSI (le numéro de la radio), la déclaration indiquant qu'il a été déprogrammé.</p>
<p>La loi prévoit que la radiation est demandée par le propriétaire ou par une personne qu'il autorise. C'est pourquoi il est important de le prévoir dans le contrat : que le vendeur signe la demande ou vous autorise à la faire. Le certificat de radiation fait partie des papiers que vous demandera la France.</p>

<h2 id="llevarlo">Comment rapatrier le bateau en France</h2>
<p>Il y a deux façons :</p>
<ul>
<li><strong>Par la route.</strong> Pour les bateaux qui tiennent sur une remorque ou un camion. Au-delà de certaines dimensions (en France, plus de 2,55 m de large), c'est un transport exceptionnel avec son autorisation. L'entreprise de transport s'en charge.</li>
<li><strong>Par la mer.</strong> Un bateau radié n'a plus de pavillon, et sans pavillon on ne peut pas naviguer. Le plus courant est de faire d'abord le changement de propriétaire en Espagne, de naviguer sous pavillon espagnol et de demander la radiation ensuite. Pour naviguer dans les eaux espagnoles, il faut une assurance responsabilité civile valable en Espagne. Confirmez cet ordre avec la gestoría avant de signer, car cela dépend de chaque cas.</li>
</ul>

<h2 id="francia">L'immatriculer en France</h2>
<p>Depuis 2022, en France, l'ancienne francisation et l'immatriculation ont été réunies en une seule démarche : le <strong>certificat d'enregistrement</strong>. C'est l'administration maritime qui s'en occupe (les DDTM et DML, selon le port d'attache). Le portail <em>demarches-plaisance.gouv.fr</em> sert pour les bateaux neufs et pour les ventes entre particuliers de bateaux déjà français ; un bateau qui vient d'un registre étranger se traite avec la DDTM.</p>
<p>Les papiers habituellement demandés :</p>
<ul>
<li>Facture ou contrat de vente du bateau et des moteurs.</li>
<li>Déclaration de conformité CE (ou le document équivalent pour les bateaux antérieurs à juin 1998).</li>
<li>Justificatif de la situation de TVA, si le bateau a été acheté dans un autre pays de l'UE.</li>
<li>Certificat de radiation du registre précédent.</li>
<li>Pièce d'identité et justificatif de domicile en France.</li>
<li>La fiche de demande (<em>fiche plaisance</em>).</li>
</ul>
<p>Pour immatriculer en France, au moins 50 % du bateau doit appartenir à un ressortissant de l'UE et on vous demandera un domicile en France.</p>

<h2 id="despues">Ensuite : taxe annuelle et permis</h2>
<p>En France, les bateaux de <strong>7 mètres ou plus</strong>, et ceux de moins de 7 mètres avec un moteur de 22 CV fiscaux ou plus, paient une taxe annuelle (l'ancien DAFN). La part coque va d'environ <strong>77 € pour 7-8 mètres</strong> à 886 € à partir de 15 mètres, plus une part selon la puissance du moteur, avec des abattements pour les bateaux anciens. Elle se paie en ligne. La France a adopté un changement du mode de calcul à partir de 2027.</p>
<p>Pour piloter un bateau français avec un moteur de plus de 4,5 kW (6 ch), il vous faut le <strong>permis plaisance</strong> : l'option côtière permet de s'éloigner jusqu'à 6 milles d'un abri.</p>

<h2 id="riesgos">Les risques les plus courants</h2>
<div class="tbl"><table><thead><tr><th>Risque</th><th>Comment l'éviter</th></tr></thead><tbody>
<tr><td>Bateau avec hypothèque ou saisie</td><td>Demander l'extrait du Registro de Bienes Muebles avant de payer</td></tr>
<tr><td>TVA non justifiée</td><td>Facture de première vente ou facture du vendeur professionnel qui l'indique</td></tr>
<tr><td>Pavillon d'un autre pays (polonais ou autre)</td><td>Savoir où se demande la radiation avant d'acheter</td></tr>
<tr><td>Moteurs qui ne correspondent pas aux papiers</td><td>Vérifier les numéros de série et demander leurs factures</td></tr>
<tr><td>Bateau « presque neuf » facturé avec TVA espagnole</td><td>Si c'est un moyen de transport neuf, la TVA se paie en France</td></tr>
<tr><td>ITP non payé</td><td>Modelo 620 sous 30 jours ouvrables ; sans lui, le changement de propriétaire se complique</td></tr>
</tbody></table></div>

<h2 id="ayuda">Comment je peux vous aider</h2>
<p>Je suis courtier nautique en Catalogne : je mets en relation ceux qui vendent leur bateau avec ceux qui veulent l'acheter. Je vous aide à trouver le bateau, je vérifie avec le vendeur les documents (propriétaire, charges, TVA, moteurs, pavillon) et je vous accompagne pour l'essai en mer et l'expertise si vous souhaitez la faire. Les démarches de radiation en Espagne et d'immatriculation en France sont faites par une gestoría nautique (cabinet spécialisé dans les formalités) ; dans l'<a href="/fr/servicios/directorio.html">annuaire des entreprises</a>, vous trouverez des gestorías par zone.</p>

<h2 id="faq">Questions fréquentes</h2>
<h3>Est-ce que je paie des impôts en Espagne et encore en France ?</h3><p>Si vous achetez un bateau d'occasion avec la TVA européenne acquittée, vous ne repayez pas la TVA en France. En Espagne, vous payez l'ITP de 4 % si vous achetez à un particulier, ou la TVA si vous achetez à une entreprise. Ensuite, en France, la taxe annuelle si le bateau y est soumis.</p>
<h3>Est-ce que je peux rentrer en France par la mer avec le bateau ?</h3><p>Oui, mais pas avec le bateau déjà radié, car il n'a plus de pavillon. Le plus courant est de faire d'abord le changement de propriétaire en Espagne, de naviguer sous pavillon espagnol et de demander la radiation ensuite. Confirmez-le avec la gestoría.</p>
<h3>Ai-je besoin d'un NIE ?</h3><p>Normalement oui, pour déclarer l'impôt et faire le changement de propriétaire. Mieux vaut le demander à l'avance.</p>
<h3>Combien coûte la taxe annuelle en France ?</h3><p>Les bateaux de moins de 7 mètres peu motorisés ne la paient pas. Pour un bateau de 7 à 8 mètres, la part coque est d'environ 77 € par an, plus une part selon la puissance du moteur.</p>
""",
    faq=[("Est-ce que je paie des impôts en Espagne et encore en France ?", "Si vous achetez un bateau d'occasion avec la TVA européenne acquittée, vous ne repayez pas la TVA en France. En Espagne, vous payez l'ITP de 4 % si vous achetez à un particulier, ou la TVA si vous achetez à une entreprise. Ensuite, en France, la taxe annuelle si le bateau y est soumis."),
         ("Est-ce que je peux rentrer en France par la mer avec le bateau ?", "Oui, mais pas avec le bateau déjà radié, car il n'a plus de pavillon. Le plus courant est de faire d'abord le changement de propriétaire en Espagne, de naviguer sous pavillon espagnol et de demander la radiation ensuite. Confirmez-le avec la gestoría."),
         ("Ai-je besoin d'un NIE ?", "Normalement oui, pour déclarer l'impôt et faire le changement de propriétaire. Mieux vaut le demander à l'avance."),
         ("Combien coûte la taxe annuelle en France ?", "Les bateaux de moins de 7 mètres peu motorisés ne la paient pas. Pour un bateau de 7 à 8 mètres, la part coque est d'environ 77 € par an, plus une part selon la puissance du moteur.")],
    note="Information indicative, revue en octobre 2026 d'après la réglementation espagnole (Texto refundido del ITP, arts. 6, 8 et 11 ; RD 1027/1989 ; RD 1435/2010 ; RD 607/1999) et l'information officielle française (mer.gouv.fr, service-public.fr, douane.gouv.fr, BOFiP). Ce n'est pas un conseil fiscal ni juridique et la réglementation peut changer. Chaque cas dépend du bateau et de votre situation : faites-le confirmer par une gestoría nautique ou par l'administration avant d'acheter.",
    card=dict(eyebrow="Vous vivez en France ?", h3="Je vous aide à trouver votre bateau en Catalogne.", p="Dites-moi ce que vous cherchez et où vous allez l'utiliser, et je vous dis quels bateaux conviennent et quels papiers vérifier.", wa="Bonjour Juan, j'habite en France et je cherche un bateau en Espagne.", btn="Parler à Juan sur WhatsApp"),
    rel=[("/fr/comprar/barcos-ocasion-espana-compradores-franceses.html", "Bateaux d'occasion en Espagne pour acheteurs français"), ("/fr/guias/barco-frances-en-cataluna.html", "Avoir votre bateau en Catalogne si vous vivez en France"), ("/fr/guias/itp-comprar-barco-usado-por-comunidad.html", "L'ITP à l'achat d'un bateau d'occasion")],
    header_wa="Bonjour Juan, j'habite en France et j'ai une question sur l'achat d'un bateau en Espagne.",
)

PAGES["g2"] = dict(
    kind="guia",
    slug="guias/barco-frances-en-cataluna.html",
    crumb=("Guides", "/fr/guias/"),
    title="Avoir votre bateau en Catalogne si vous vivez en France : place de port, impôts et permis",
    desc="Vous passez l'été en Catalogne et voulez y garder votre bateau ? Amener votre bateau français ou en acheter un en Espagne, les impôts et assurances qui s'appliquent, le permis nécessaire et le fonctionnement des places de port sur la Costa Brava.",
    eyebrow="Guides · Si vous vivez en France",
    h1="Avoir votre bateau en Catalogne si vous vivez en France",
    meta=["Par Juan Morante", "Mis à jour en octobre 2026", "7 min de lecture"],
    lead="Si vous passez vos étés sur la Costa Brava ou ailleurs en Catalogne, garder le bateau ici vous évite le trajet chaque année. Il y a deux options : amener votre bateau sous pavillon français ou en acheter un ici. Les deux fonctionnent, mais chacune a ses règles. Je vous les résume.",
    toc=[("dos", "Deux options"), ("frances", "Amener votre bateau sous pavillon français"), ("espanol", "Acheter ici et le garder sous pavillon espagnol"), ("permiso", "Quel permis vous faut-il"), ("amarre", "Place de port et hivernage"), ("faq", "Questions fréquentes")],
    body="""
<h2 id="dos">Deux options</h2>
<ul>
<li><strong>Amener votre bateau français</strong> et le laisser amarré ici sous son pavillon.</li>
<li><strong>Acheter un bateau en Espagne</strong> et, soit le ramener en France (c'est expliqué dans le <a href="/fr/guias/comprar-barco-espana-matricular-francia.html">guide pour l'immatriculer en France</a>), soit le garder ici sous pavillon espagnol.</li>
</ul>

<h2 id="frances">Amener votre bateau sous pavillon français</h2>
<p>La France et l'Espagne font partie de l'Union européenne : un bateau français avec la TVA européenne acquittée peut donc rester dans un port catalan <strong>sans formalités d'entrée</strong> ni douane. Il vaut mieux avoir à bord les papiers du bateau et le justificatif de TVA.</p>
<p>Il n'y a pas de durée maximale de séjour tant que le bateau est utilisé par vous et par des personnes qui ne vivent pas non plus en Espagne. Le point délicat, c'est <strong>qui l'utilise</strong> : la loi espagnole oblige à immatriculer en Espagne les bateaux utilisés ici par des personnes résidant en Espagne, et à payer la taxe d'immatriculation espagnole (12 % pour les bateaux de plus de 8 mètres). Le fisc espagnol a indiqué dans des consultations récentes que les entrées répétées d'un bateau étranger utilisé par un résident sont considérées comme une utilisation habituelle. En pratique : si vous le prêtez à des proches, des amis ou à un skipper qui vit en Espagne, cette obligation peut apparaître. Nous l'expliquons dans le <a href="/fr/guias/impuesto-matriculacion-barcos.html">guide de la taxe d'immatriculation</a>.</p>
<p>Deux choses encore :</p>
<ul>
<li><strong>Assurance.</strong> Dans les eaux espagnoles, une assurance responsabilité civile est obligatoire, y compris pour les bateaux étrangers. Vérifiez que votre contrat français couvre l'Espagne.</li>
<li><strong>La taxe annuelle française</strong> continue de se payer en France même si le bateau est ici. En Espagne, vous paierez la place de port et les services du port.</li>
</ul>

<h2 id="espanol">Acheter ici et le garder sous pavillon espagnol</h2>
<p>Un non-résident peut avoir un bateau sous pavillon espagnol à son nom. Voici ce qui vous attend :</p>
<ul>
<li><strong>L'impôt sur l'achat.</strong> Si vous achetez à un particulier en tant que non-résident, l'ITP est de <strong>4 %</strong>, avec le modelo 620 de l'Agencia Tributaria de l'État et un délai de 30 jours ouvrables. Si vous achetez à une entreprise, TVA.</li>
<li><strong>NIE.</strong> On vous le demandera normalement pour déclarer et faire le changement de propriétaire.</li>
<li><strong>ITB.</strong> L'inspection technique : pour les bateaux de plaisance de 6 à 24 mètres, au maximum tous les 5 ans. Ceux de moins de 6 mètres n'ont pas d'inspections périodiques.</li>
<li><strong>Assurance responsabilité civile</strong> obligatoire.</li>
<li><strong>Attention en France :</strong> si vous vivez en France et naviguez dans les eaux françaises avec un bateau sous pavillon étranger, la France peut vous réclamer un impôt équivalent à sa taxe annuelle (le <em>droit de passeport</em>). Si le bateau reste en Espagne, vous n'êtes pas concerné.</li>
</ul>

<h2 id="permiso">Quel permis vous faut-il</h2>
<ul>
<li><strong>Bateau sous pavillon français :</strong> la réglementation française s'applique aussi en Espagne. Avec votre <em>permis plaisance</em>, vous pouvez le piloter dans ses limites (l'option côtière, jusqu'à 6 milles d'un abri).</li>
<li><strong>Bateau sous pavillon espagnol :</strong> en tant que citoyen européen titulaire d'un permis de votre pays, la Capitainerie maritime espagnole (Capitanía Marítima) peut vous autoriser à le piloter. C'est une démarche à faire de préférence avant la saison. Vous trouverez les permis espagnols dans la rubrique <a href="/fr/titulaciones/">permis bateau</a>.</li>
</ul>

<h2 id="amarre">Place de port et hivernage</h2>
<p>Sur la Costa Brava, la plupart des ports sont gérés par des clubs nautiques ou des sociétés concessionnaires. Près de la frontière, vous avez Portbou, Colera, Llançà, El Port de la Selva, Roses, Empuriabrava, L'Escala, L'Estartit et, plus au sud, Palamós.</p>
<ul>
<li><strong>À l'année ou à la saison.</strong> La place à l'année revient moins cher par mois, mais en été les places en location sont rares et dans les petits ports il y a une liste d'attente. À titre indicatif, les tarifs officiels 2026 du port de Portbou pour un bateau de 7,5 à 8,5 mètres sont d'environ 3 445 € par an, ou d'environ 1 045 € pour un mois de juillet ou d'août.</li>
<li><strong>Hivernage à sec.</strong> Pour les bateaux jusqu'à 7-8 mètres, le port à sec ou le chantier de carénage reviennent souvent moins cher que l'eau, et le bateau passe l'hiver à l'abri.</li>
<li><strong>L'entretien quand vous n'êtes pas là.</strong> C'est ce qui inquiète le plus quand on vit loin : quelqu'un qui vérifie les amarres, les batteries et les cales. Dans <a href="/fr/servicios/">services</a>, vous trouverez des entreprises d'entretien et des chantiers.</li>
</ul>
<p>Vous trouverez plus de prix et de types de places dans le <a href="/fr/guias/amarres-cataluna-tipos-precios-alquiler-compra.html">guide des places de port en Catalogne</a>.</p>

<h2 id="ayuda">Comment je peux vous aider</h2>
<p>Si vous cherchez un bateau pour le garder ici, je vous aide à le trouver et je vérifie les documents avec le vendeur. Et si le bateau est vendu avec une place de port transférable, je l'indique dans la fiche.</p>

<h2 id="faq">Questions fréquentes</h2>
<h3>Puis-je laisser mon bateau français toute l'année en Catalogne ?</h3><p>Oui. Comme c'est un bateau de l'Union européenne avec la TVA acquittée, il n'y a pas de durée maximale tant qu'il est utilisé par vous et par d'autres personnes qui ne vivent pas en Espagne.</p>
<h3>Puis-je prêter le bateau à un ami qui vit en Espagne ?</h3><p>Avec prudence : s'il est utilisé par des résidents en Espagne, la loi peut obliger à l'immatriculer ici et à payer la taxe d'immatriculation. Renseignez-vous d'abord auprès d'une gestoría.</p>
<h3>Mon permis plaisance est-il valable en Espagne ?</h3><p>Pour un bateau sous pavillon français, oui, dans ses limites. Pour un bateau sous pavillon espagnol, il vous faut une autorisation de la Capitainerie maritime espagnole.</p>
<h3>L'assurance est-elle obligatoire ?</h3><p>Dans les eaux espagnoles, oui : une assurance responsabilité civile, y compris pour les bateaux sous pavillon étranger.</p>
""",
    faq=[("Puis-je laisser mon bateau français toute l'année en Catalogne ?", "Oui. Comme c'est un bateau de l'Union européenne avec la TVA acquittée, il n'y a pas de durée maximale tant qu'il est utilisé par vous et par d'autres personnes qui ne vivent pas en Espagne."),
         ("Puis-je prêter le bateau à un ami qui vit en Espagne ?", "Avec prudence : s'il est utilisé par des résidents en Espagne, la loi peut obliger à l'immatriculer ici et à payer la taxe d'immatriculation. Renseignez-vous d'abord auprès d'une gestoría."),
         ("Mon permis plaisance est-il valable en Espagne ?", "Pour un bateau sous pavillon français, oui, dans ses limites. Pour un bateau sous pavillon espagnol, il vous faut une autorisation de la Capitainerie maritime espagnole."),
         ("L'assurance est-elle obligatoire ?", "Dans les eaux espagnoles, oui : une assurance responsabilité civile, y compris pour les bateaux sous pavillon étranger.")],
    note="Information indicative, revue en octobre 2026 d'après la réglementation espagnole (Ley 38/1992, disposición adicional 1.ª et art. 65 ; consulta DGT V0820-25 ; RD 875/2014 ; RD 1434/1999 ; RD 607/1999 ; Texto refundido del ITP) et l'information officielle française (mer.gouv.fr, douane.gouv.fr). Les prix des places de port sont les tarifs publiés par le port de Portbou pour 2026 et peuvent changer. Ce n'est pas un conseil fiscal ni juridique : faites-le confirmer par une gestoría nautique ou par l'administration.",
    card=dict(eyebrow="Vous passez l'été en Catalogne ?", h3="Je vous aide à avoir votre bateau ici.", p="Dites-moi où vous passez l'été et quel bateau vous cherchez, et je vous dis ce qui convient.", wa="Bonjour Juan, je passe l'été en Catalogne et je voudrais avoir un bateau ici.", btn="Parler à Juan sur WhatsApp"),
    rel=[("/fr/comprar/barcos-ocasion-espana-compradores-franceses.html", "Bateaux d'occasion en Espagne pour acheteurs français"), ("/fr/guias/comprar-barco-espana-matricular-francia.html", "Acheter en Espagne et immatriculer en France"), ("/fr/guias/amarres-cataluna-tipos-precios-alquiler-compra.html", "Places de port en Catalogne : types et prix")],
    header_wa="Bonjour Juan, je passe l'été en Catalogne et j'ai une question sur le fait d'y garder un bateau.",
)

PAGES["l4"] = dict(
    kind="landing",
    slug="comprar/barcos-ocasion-espana-compradores-franceses.html",
    crumb=("Acheter un bateau", "/fr/comprar/"),
    title="Bateaux d'occasion en Espagne pour les acheteurs qui vivent en France",
    desc="Bateaux d'occasion à vendre en Catalogne pour ceux qui vivent en France : pour le ramener en France ou le garder ici l'été. Impôts, papiers et comment acheter en toute tranquillité.",
    eyebrow="Acheter un bateau · Si vous vivez en France",
    h1="Bateaux d'occasion en Espagne, si vous vivez en France",
    meta=["Par Juan Morante", "Mis à jour en octobre 2026"],
    lead="Voici les bateaux dont je m'occupe actuellement. Si vous vivez en France, vous pouvez en acheter un pour le ramener et l'immatriculer là-bas, ou pour le garder ici et l'utiliser l'été. Je vous explique plus bas l'essentiel de chaque cas.",
    toc=[("barcos", "Bateaux à vendre"), ("llevar", "Pour le ramener en France"), ("aqui", "Pour le garder en Catalogne"), ("como", "Comment nous achetons"), ("faq", "Questions fréquentes")],
    body="""
<h2 id="barcos">Bateaux à vendre</h2>
<div class="pm-list" data-f='{}'></div>
<p class="pm-empty" hidden>Je n'ai pas de bateau disponible en ce moment. <a href="/fr/alertas/">Créez une alerte</a> et je vous préviens dès qu'il en arrive un.</p>
<p class="note" style="font-family:var(--display);font-size:12.5px;color:var(--ink-2)">Tous les bateaux que je publie ont un mandat de vente signé par leur propriétaire. <a href="/fr/barcos/">Voir le catalogue complet avec filtres</a>.</p>

<h2 id="llevar">Pour le ramener en France</h2>
<p>Si vous achetez à un particulier en tant que non-résident, on paie en Espagne l'ITP de <strong>4 %</strong> avec le modelo 620 ; si vous achetez à une entreprise, la TVA. Ensuite, le bateau est radié du registre espagnol et immatriculé en France avec le <em>certificat d'enregistrement</em>. Un bateau d'occasion avec la TVA européenne acquittée ne repaie pas la TVA en France. Tout est expliqué étape par étape dans le <a href="/fr/guias/comprar-barco-espana-matricular-francia.html">guide pour acheter en Espagne et immatriculer en France</a>.</p>

<h2 id="aqui">Pour le garder en Catalogne</h2>
<p>Vous pouvez le garder sous pavillon espagnol à votre nom, ou amener votre bateau français et l'amarrer ici sans formalités d'entrée. L'important, c'est qu'il soit utilisé par vous et par des personnes qui ne vivent pas en Espagne, d'avoir une assurance responsabilité civile valable en Espagne et le permis adapté. Je l'explique dans le <a href="/fr/guias/barco-frances-en-cataluna.html">guide pour avoir votre bateau en Catalogne</a>.</p>

<h2 id="como">Comment nous achetons</h2>
<ol>
<li><strong>Vous me dites ce que vous cherchez</strong> : type de bateau, longueur, budget et si vous voulez le ramener en France ou le garder ici.</li>
<li><strong>Je vérifie les documents avec le vendeur</strong> : propriétaire, charges, TVA, moteurs et pavillon.</li>
<li><strong>Essai en mer et expertise</strong>, si vous souhaitez la faire, avant de verser l'acompte.</li>
<li><strong>Contrat et papiers</strong>, avec une gestoría nautique qui fait le changement de propriétaire ou la radiation pour la France.</li>
</ol>
<p>Si le bateau que vous cherchez n'est pas dans la liste, <a href="/fr/alertas/">créez une alerte</a> et je vous préviens quand il en arrive un qui correspond.</p>

<h2 id="faq">Questions fréquentes</h2>
<h3>Puis-je acheter un bateau en Espagne en vivant en France ?</h3><p>Oui. Il vous faudra normalement un NIE et, si vous achetez à un particulier, payer l'ITP de 4 % en tant que non-résident.</p>
<h3>Dois-je repayer la TVA en France ?</h3><p>Non, s'il s'agit d'un bateau d'occasion avec la TVA européenne acquittée. Elle ne se paie en France que si le bateau est considéré comme neuf (plus de 7,5 mètres et moins de 3 mois ou de 100 heures d'utilisation).</p>
<h3>Puis-je voir le bateau avant de l'acheter ?</h3><p>Bien sûr. Le mieux est de le voir, de faire un essai en mer et, si vous le souhaitez, une expertise avant de verser le moindre acompte.</p>
""",
    faq=[("Puis-je acheter un bateau en Espagne en vivant en France ?", "Oui. Il vous faudra normalement un NIE et, si vous achetez à un particulier, payer l'ITP de 4 % en tant que non-résident."),
         ("Dois-je repayer la TVA en France ?", "Non, s'il s'agit d'un bateau d'occasion avec la TVA européenne acquittée. Elle ne se paie en France que si le bateau est considéré comme neuf (plus de 7,5 mètres et moins de 3 mois ou de 100 heures d'utilisation)."),
         ("Puis-je voir le bateau avant de l'acheter ?", "Bien sûr. Le mieux est de le voir, de faire un essai en mer et, si vous le souhaitez, une expertise avant de verser le moindre acompte.")],
    note="Information fiscale indicative, revue en octobre 2026. Ce n'est pas un conseil fiscal ni juridique et la réglementation peut changer. Faites-le confirmer par une gestoría nautique ou par l'administration avant d'acheter.",
    card=dict(eyebrow="Vous vivez en France ?", h3="Je vous aide à trouver votre bateau.", p="Dites-moi ce que vous cherchez, votre budget et si vous voulez le ramener en France ou le garder ici.", wa="Bonjour Juan, j'habite en France et je cherche un bateau d'occasion en Espagne.", btn="Parler à Juan sur WhatsApp"),
    rel=[("/fr/guias/comprar-barco-espana-matricular-francia.html", "Acheter en Espagne et immatriculer en France"), ("/fr/guias/barco-frances-en-cataluna.html", "Avoir votre bateau en Catalogne si vous vivez en France"), ("/fr/comprar/barcos-segunda-mano-costa-brava.html", "Bateaux d'occasion sur la Costa Brava")],
    header_wa="Bonjour Juan, j'habite en France et je cherche un bateau en Espagne.",
)

# Textes isolés : lien dans l'index des guides, accueil FR et fiches
INDEX_CARD = {
  "g1": dict(tag="Acheter depuis la France", h2="Acheter un bateau en Espagne et l'immatriculer en France", p="Impôts en Espagne, radiation du registre espagnol, comment le rapatrier et les papiers que demande la France."),
  "g2": dict(tag="Si vous vivez en France", h2="Avoir votre bateau en Catalogne si vous vivez en France", p="Pavillon français ou espagnol, impôts, assurance, permis et places de port sur la Costa Brava."),
}
