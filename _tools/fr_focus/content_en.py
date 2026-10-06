# -*- coding: utf-8 -*-
# English (British) version of the pages for buyers living in France. Same structure as content_es.py.
FECHA = "October 2026"

PAGES = {}

PAGES["g1"] = dict(
    kind="guia",
    slug="guias/comprar-barco-espana-matricular-francia.html",
    crumb=("Guides", "/en/guias/"),
    title="Buying a boat in Spain and registering it in France: a step-by-step guide",
    desc="If you live in France and have found a boat in Spain: which taxes are paid here, how it is deregistered from the Spanish register, how to get it there and what paperwork France asks for to register it.",
    eyebrow="Guides · Buying from France",
    h1="Buying a boat in Spain and registering it in France",
    meta=["By Juan Morante", "Updated October 2026", "8 min read"],
    lead="More and more people who live in France are looking for a boat in Catalonia. The purchase can be done without any problem, but there are two countries and two administrations involved, and it pays to do things in the right order. Here I explain the whole process: what to check before paying, what is paid in Spain, how the boat is deregistered here and what France asks for to register it.",
    toc=[("antes", "Before paying: what to check"), ("impuestos", "Taxes in Spain"), ("baja", "Deregistering from the Spanish register"), ("llevarlo", "How to take the boat to France"), ("francia", "Registering it in France"), ("despues", "Afterwards: annual tax and licence"), ("riesgos", "The most common risks"), ("faq", "Frequently asked questions")],
    body="""
<h2 id="antes">Before paying: what to check</h2>
<p>What causes the most problems in a purchase between two countries is not the paperwork, but finding out too late that something does not add up. Before leaving any deposit, ask for and check the following:</p>
<ul>
<li><strong>Who the owner is.</strong> That the person selling to you is the owner shown in the boat's documents, or has the authority to sell it.</li>
<li><strong>Charges.</strong> That the boat has no mortgages or seizures on it. This is checked at the Registro de Bienes Muebles (Spanish movable property register). If there is a creditor, their authorisation will be needed to deregister the boat.</li>
<li><strong>VAT.</strong> That the boat has had VAT paid in the European Union. The usual thing is to ask for the invoice from the first sale. To register it in France you will be asked to prove it, especially if it is longer than 7.5 metres.</li>
<li><strong>The current flag.</strong> If the boat has a Spanish flag, deregistration is requested in Spain. If it has another flag (Polish, for example), deregistration is requested from that country's register, and it is a different procedure.</li>
<li><strong>Engines.</strong> That the engines' serial numbers match the paperwork. France also asks for the invoice or purchase document for the engines.</li>
<li><strong>EC declaration of conformity.</strong> France asks for it to register the boat. Boats placed on the European market before 16 June 1998 do not have one and are processed with a different document.</li>
</ul>
<p>My advice is to do the <strong>sea trial and the survey before leaving the deposit</strong>, or to leave the deposit on condition that the survey turns out well. It is explained in the <a href="/en/guias/arras-compraventa-barco.html">guide to deposits (arras)</a>.</p>

<h2 id="impuestos">Taxes in Spain</h2>
<p>It depends on who is selling you the boat:</p>
<ul>
<li><strong>If a private individual is selling</strong>, transfer tax (ITP) is paid. If you are not resident in Spain, it is not paid to Catalonia but to the State Agencia Tributaria: the rate is <strong>4%</strong>, it is declared using <strong>modelo 620</strong> for non-residents and you have <strong>30 working days</strong> from signing the contract. It is calculated on the price or on the official tax-table value, whichever is higher.</li>
<li><strong>If a company is selling</strong>, the transaction carries VAT instead of ITP: on a used boat, normally Spanish VAT (IVA). If the seller applies the special scheme for second-hand goods, the VAT is included in the price and is not shown separately; ask for the invoice to state this, because it is your proof of VAT for France.</li>
<li><strong>A "new" boat:</strong> if it is longer than 7.5 metres and is delivered within 3 months of first entering into service or with fewer than 100 hours of navigation, in law it is a new means of transport and the VAT is paid in France, not in Spain.</li>
</ul>
<p>To file the tax return and handle the procedures in Spain, you will normally be asked for an <strong>NIE</strong> (foreigner identification number). It is worth applying for it in good time.</p>
<p>If you buy as a resident in Spain, the ITP is that of your autonomous community: you will find it in the <a href="/en/guias/itp-comprar-barco-usado-por-comunidad.html">guide to ITP by region</a>.</p>

<h2 id="baja">Deregistering from the Spanish register</h2>
<p>To register the boat in France, it first has to leave the Spanish register. This is requested at the <strong>Harbour Master's Office (Capitanía Marítima)</strong> as a <strong>deregistration for export</strong> (permanent or provisional), with the recreational craft application form and the corresponding fee (modelo 790-025). You provide the registration sheet (hoja de asiento), the sale document, the creditors' authorisation if there are any and, if the boat has an MMSI (the radio number), the declaration that it has been deprogrammed.</p>
<p>The law says that deregistration is requested by the owner or by someone authorised by them. That is why it is important to agree it in the contract: that the seller signs the application or authorises you to request it. The deregistration certificate is one of the documents France will ask you for.</p>

<h2 id="llevarlo">How to take the boat to France</h2>
<p>There are two ways:</p>
<ul>
<li><strong>By road.</strong> For boats that fit on a trailer or a lorry. Above certain dimensions (in France, more than 2.55 m wide) it is an abnormal load requiring its own permit. The transport company deals with it.</li>
<li><strong>Under its own steam.</strong> A deregistered boat is left without a flag, and without a flag it cannot be sailed. The usual approach is to do the change of ownership in Spain first, sail with the Spanish flag and request deregistration afterwards. To navigate in Spanish waters you need third-party liability insurance valid in Spain. Confirm this order with the agency (gestoría) before signing, because it depends on each case.</li>
</ul>

<h2 id="francia">Registering it in France</h2>
<p>Since 2022, in France the former francisation and registration have been merged into a single procedure: the <strong>certificat d'enregistrement</strong>. It is handled by the maritime administration (the DDTM and DML, depending on the home port). The <em>demarches-plaisance.gouv.fr</em> portal is for new boats and for private sales of boats that are already French; a boat coming from a foreign register is processed with the DDTM.</p>
<p>The documents they usually ask for:</p>
<ul>
<li>Invoice or sale contract for the boat and the engines.</li>
<li>EC declaration of conformity (or the equivalent document for boats from before June 1998).</li>
<li>Proof of the VAT position, if the boat was bought in another EU country.</li>
<li>Deregistration certificate from the previous register.</li>
<li>Identity document and proof of address in France.</li>
<li>The application form (<em>fiche plaisance</em>).</li>
</ul>
<p>To register in France, at least 50% of the boat must belong to an EU citizen and you will be asked for an address in France.</p>

<h2 id="despues">Afterwards: annual tax and licence</h2>
<p>In France, boats of <strong>7 metres or more</strong>, and those under 7 metres with an engine of 22 fiscal horsepower or more, pay an annual tax (formerly the DAFN). The hull element ranges from around <strong>€77 for 7-8 metres</strong> to €886 from 15 metres upwards, plus an element based on engine power, with reductions for older boats. It is paid online. France has approved a change to the calculation from 2027.</p>
<p>To skipper a French boat with an engine of more than 4.5 kW (6 hp) you need the <strong>permis plaisance</strong>: the coastal option lets you go up to 6 miles from a shelter.</p>

<h2 id="riesgos">The most common risks</h2>
<div class="tbl"><table><thead><tr><th>Risk</th><th>How to avoid it</th></tr></thead><tbody>
<tr><td>Boat with a mortgage or seizure</td><td>Ask for the extract from the Registro de Bienes Muebles before paying</td></tr>
<tr><td>VAT not proven</td><td>First-sale invoice or an invoice from the professional seller that states it</td></tr>
<tr><td>Flag from another country (Polish or other)</td><td>Find out where deregistration is requested before buying</td></tr>
<tr><td>Engines that do not match the paperwork</td><td>Check serial numbers and ask for their invoices</td></tr>
<tr><td>"Nearly new" boat invoiced with Spanish VAT (IVA)</td><td>If it is a new means of transport, the VAT is paid in France</td></tr>
<tr><td>ITP not paid</td><td>Modelo 620 within 30 working days; without it the change of ownership gets complicated</td></tr>
</tbody></table></div>

<h2 id="ayuda">How I can help you</h2>
<p>I'm a boat broker in Catalonia: I put people selling their boat in touch with people buying one. I help you find the boat, go through the documentation with the seller (owner, charges, VAT, engines, flag) and accompany you on the sea trial and the survey if you want one. The deregistration procedures in Spain and the registration in France are handled by a nautical agency (gestoría); in the <a href="/en/servicios/directorio.html">business directory</a> you will find agencies by area.</p>

<h2 id="faq">Frequently asked questions</h2>
<h3>Do I pay tax in Spain and again in France?</h3><p>If you buy a used boat with European VAT paid, VAT is not paid again in France. In Spain you pay the 4% ITP if you buy from a private individual, or VAT if you buy from a company. Afterwards, in France, the annual tax if the boat is liable.</p>
<h3>Can I sail the boat back?</h3><p>Yes, but not once the boat has been deregistered, because it is left without a flag. The usual approach is to do the change of ownership in Spain first, sail under the Spanish flag and request deregistration afterwards. Confirm it with the agency.</p>
<h3>Do I need an NIE?</h3><p>Normally yes, to declare the tax and do the change of ownership. It is worth applying for it in good time.</p>
<h3>How much is the annual tax in France?</h3><p>Boats under 7 metres with low power do not pay it. For a boat of 7 to 8 metres, the hull element is around €77 a year, plus an element based on engine power.</p>
""",
    faq=[("Do I pay tax in Spain and again in France?", "If you buy a used boat with European VAT paid, VAT is not paid again in France. In Spain you pay the 4% ITP if you buy from a private individual, or VAT if you buy from a company. Afterwards, in France, the annual tax if the boat is liable."),
         ("Can I sail the boat back?", "Yes, but not once the boat has been deregistered, because it is left without a flag. The usual approach is to do the change of ownership in Spain first, sail under the Spanish flag and request deregistration afterwards. Confirm it with the agency."),
         ("Do I need an NIE?", "Normally yes, to declare the tax and do the change of ownership. It is worth applying for it in good time."),
         ("How much is the annual tax in France?", "Boats under 7 metres with low power do not pay it. For a boat of 7 to 8 metres, the hull element is around €77 a year, plus an element based on engine power.")],
    note="Guidance only, reviewed in October 2026 in line with Spanish legislation (Texto refundido del ITP, arts. 6, 8 and 11; RD 1027/1989; RD 1435/2010; RD 607/1999) and official French information (mer.gouv.fr, service-public.fr, douane.gouv.fr, BOFiP). This is not tax or legal advice and the rules may change. Each case depends on the boat and your situation: confirm it with a nautical agency (gestoría) or with the authorities before buying.",
    card=dict(eyebrow="Do you live in France?", h3="I can help you find the boat in Catalonia.", p="Tell me what you are looking for and where you will use it, and I will tell you which boats fit and what paperwork to check.", wa="Hello Juan, I live in France and I am looking for a boat in Spain.", btn="Talk to Juan on WhatsApp"),
    rel=[("/en/comprar/barcos-ocasion-espana-compradores-franceses.html", "Used boats in Spain for buyers from France"), ("/en/guias/barco-frances-en-cataluna.html", "Keeping your boat in Catalonia if you live in France"), ("/en/guias/itp-comprar-barco-usado-por-comunidad.html", "ITP when buying a used boat")],
    header_wa="Hello Juan, I live in France and I have a question about buying a boat in Spain.",
)

PAGES["g2"] = dict(
    kind="guia",
    slug="guias/barco-frances-en-cataluna.html",
    crumb=("Guides", "/en/guias/"),
    title="Keeping your boat in Catalonia if you live in France: mooring, taxes and licence",
    desc="If you spend your summers in Catalonia and want to keep your boat here: bringing your French boat or buying one in Spain, which taxes and insurance apply, which licence you need and how moorings work on the Costa Brava.",
    eyebrow="Guides · If you live in France",
    h1="Keeping your boat in Catalonia if you live in France",
    meta=["By Juan Morante", "Updated October 2026", "7 min read"],
    lead="If you spend your summers on the Costa Brava or elsewhere in Catalonia, keeping the boat here saves you the trip every year. There are two ways to do it: bring your French-flagged boat or buy one here. Both work, but each has its own rules. Here is a summary.",
    toc=[("dos", "Two ways"), ("frances", "Bringing your French-flagged boat"), ("espanol", "Buying here and keeping it under the Spanish flag"), ("permiso", "Which licence you need"), ("amarre", "Mooring and winter storage"), ("faq", "Frequently asked questions")],
    body="""
<h2 id="dos">Two ways</h2>
<ul>
<li><strong>Bring your French boat</strong> and keep it moored here under its own flag.</li>
<li><strong>Buy a boat in Spain</strong> and either take it to France (see the <a href="/en/guias/comprar-barco-espana-matricular-francia.html">guide to registering it in France</a>) or keep it here under the Spanish flag.</li>
</ul>

<h2 id="frances">Bringing your French-flagged boat</h2>
<p>France and Spain are both in the European Union, so a French boat with European VAT paid can stay in a Catalan port <strong>without entry formalities</strong> or customs. You should keep the boat's papers and the proof of VAT on board.</p>
<p>There is no maximum length of stay as long as the boat is used by you and by people who do not live in Spain either. The sensitive point is <strong>who uses it</strong>: Spanish law requires boats used here by people resident in Spain to be registered in Spain, and the registration tax to be paid (12% on boats longer than 8 metres). The tax authorities have stated in recent rulings that repeated entries of a foreign boat used by a resident count as habitual use. In practice: if you lend it to family, friends or a skipper who lives in Spain, that obligation may arise. We explain it in the <a href="/en/guias/impuesto-matriculacion-barcos.html">guide to the registration tax</a>.</p>
<p>Two more things:</p>
<ul>
<li><strong>Insurance.</strong> In Spanish waters third-party liability insurance is compulsory, for foreign boats too. Check that your French policy covers Spain.</li>
<li><strong>The French annual tax</strong> is still paid in France even if the boat is here. In Spain you will pay for the mooring/berth and the port services.</li>
</ul>

<h2 id="espanol">Buying here and keeping it under the Spanish flag</h2>
<p>A non-resident can have a Spanish-flagged boat in their name. What you will come across:</p>
<ul>
<li><strong>Tax on the purchase.</strong> If you buy from a private individual as a non-resident, the ITP is <strong>4%</strong>, using modelo 620 of the State Agencia Tributaria, with a 30-working-day deadline. If you buy from a company, VAT.</li>
<li><strong>NIE.</strong> You will normally be asked for one to file the tax return and do the change of ownership.</li>
<li><strong>ITB.</strong> The technical inspection: for recreational boats from 6 to 24 metres, at most every 5 years. Boats under 6 metres have no periodic inspections.</li>
<li><strong>Third-party liability insurance</strong> is compulsory.</li>
<li><strong>Watch out in France:</strong> if you live in France and sail in French waters with a foreign-flagged boat, France may charge you a tax equivalent to its annual tax (the <em>droit de passeport</em>). If the boat stays in Spain, it does not affect you.</li>
</ul>

<h2 id="permiso">Which licence you need</h2>
<ul>
<li><strong>French-flagged boat:</strong> French rules also apply in Spain. With your <em>permis plaisance</em> you can skipper it within its limits (the coastal option, up to 6 miles from a shelter).</li>
<li><strong>Spanish-flagged boat:</strong> as a European citizen with a qualification from your own country, the Harbour Master's Office (Capitanía Marítima) can authorise you to skipper it. It is a procedure worth doing before the season. You will find the Spanish qualifications under <a href="/en/titulaciones/">qualifications</a>.</li>
</ul>

<h2 id="amarre">Mooring and winter storage</h2>
<p>On the Costa Brava, most ports are run by yacht clubs or concession companies. Near the border you have Portbou, Colera, Llançà, El Port de la Selva, Roses, Empuriabrava, L'Escala, L'Estartit and, further south, Palamós.</p>
<ul>
<li><strong>Annual or seasonal.</strong> An annual mooring/berth works out cheaper per month, but in summer rental berths are scarce and small ports have waiting lists. As a reference, the official 2026 rates at the port of Portbou for a boat of 7.5 to 8.5 metres are around €3,445 a year, or around €1,045 for one month in July or August.</li>
<li><strong>Dry winter storage.</strong> For boats up to 7-8 metres, dry stack storage or a boatyard usually works out cheaper than staying in the water, and the boat spends the winter protected.</li>
<li><strong>Maintenance while you are away.</strong> This is what worries people who live far away the most: someone to check the mooring lines, batteries and bilges. Under <a href="/en/servicios/">services</a> you will find maintenance companies and boatyards.</li>
</ul>
<p>You will find more prices and types of mooring in the <a href="/en/guias/amarres-cataluna-tipos-precios-alquiler-compra.html">guide to moorings in Catalonia</a>.</p>

<h2 id="ayuda">How I can help you</h2>
<p>If you are looking for a boat to keep here, I help you find it and go through the documentation with the seller. And if the boat is sold with a mooring/berth that can be transferred, I state it in the listing.</p>

<h2 id="faq">Frequently asked questions</h2>
<h3>Can I keep my French boat in Catalonia all year round?</h3><p>Yes. As an EU boat with VAT paid, there is no maximum period as long as it is used by you and other people who do not live in Spain.</p>
<h3>Can I lend the boat to a friend who lives in Spain?</h3><p>With care: if it is used by residents in Spain, the law may require it to be registered here and the registration tax to be paid. Check with an agency (gestoría) first.</p>
<h3>Is my permis plaisance valid in Spain?</h3><p>For a French-flagged boat, yes, within its limits. For a Spanish-flagged boat you need an authorisation from the Harbour Master's Office (Capitanía Marítima).</p>
<h3>Is insurance compulsory?</h3><p>In Spanish waters, yes: third-party liability insurance, for foreign-flagged boats too.</p>
""",
    faq=[("Can I keep my French boat in Catalonia all year round?", "Yes. As an EU boat with VAT paid, there is no maximum period as long as it is used by you and other people who do not live in Spain."),
         ("Can I lend the boat to a friend who lives in Spain?", "With care: if it is used by residents in Spain, the law may require it to be registered here and the registration tax to be paid. Check with an agency (gestoría) first."),
         ("Is my permis plaisance valid in Spain?", "For a French-flagged boat, yes, within its limits. For a Spanish-flagged boat you need an authorisation from the Harbour Master's Office (Capitanía Marítima)."),
         ("Is insurance compulsory?", "In Spanish waters, yes: third-party liability insurance, for foreign-flagged boats too.")],
    note="Guidance only, reviewed in October 2026 in line with Spanish legislation (Ley 38/1992, first additional provision and art. 65; DGT ruling V0820-25; RD 875/2014; RD 1434/1999; RD 607/1999; Texto refundido del ITP) and official French information (mer.gouv.fr, douane.gouv.fr). Mooring prices are the rates published by the port of Portbou for 2026 and may change. This is not tax or legal advice: confirm it with a nautical agency (gestoría) or with the authorities.",
    card=dict(eyebrow="Do you spend your summers in Catalonia?", h3="I can help you keep your boat here.", p="Tell me where you spend the summer and what boat you are looking for, and I will tell you what fits.", wa="Hello Juan, I spend my summers in Catalonia and I would like to keep a boat here.", btn="Talk to Juan on WhatsApp"),
    rel=[("/en/comprar/barcos-ocasion-espana-compradores-franceses.html", "Used boats in Spain for buyers from France"), ("/en/guias/comprar-barco-espana-matricular-francia.html", "Buying in Spain and registering in France"), ("/en/guias/amarres-cataluna-tipos-precios-alquiler-compra.html", "Moorings in Catalonia: types and prices")],
    header_wa="Hello Juan, I spend my summers in Catalonia and I have a question about keeping the boat here.",
)

PAGES["l4"] = dict(
    kind="landing",
    slug="comprar/barcos-ocasion-espana-compradores-franceses.html",
    crumb=("Buy a boat", "/en/comprar/"),
    title="Used boats in Spain for buyers who live in France",
    desc="Second-hand boats for sale in Catalonia for people who live in France: to take to France or to keep here for the summer. Taxes, paperwork and how to buy with peace of mind.",
    eyebrow="Buy a boat · If you live in France",
    h1="Used boats in Spain, if you live in France",
    meta=["By Juan Morante", "Updated October 2026"],
    lead="These are the boats I am currently handling. If you live in France, you can buy one to take back and register there, or to keep here and use in the summer. Below I explain the basics of each option.",
    toc=[("barcos", "Boats for sale"), ("llevar", "To take it to France"), ("aqui", "To keep it in Catalonia"), ("como", "How we buy"), ("faq", "Frequently asked questions")],
    body="""
<h2 id="barcos">Boats for sale</h2>
<div class="pm-list" data-f='{}'></div>
<p class="pm-empty" hidden>I have no boats available right now. <a href="/en/alertas/">Create an alert</a> and I will let you know as soon as one comes in.</p>
<p class="note" style="font-family:var(--display);font-size:12.5px;color:var(--ink-2)">Every boat I list has a sale mandate signed by its owner. <a href="/en/barcos/">See the full catalogue with filters</a>.</p>

<h2 id="llevar">To take it to France</h2>
<p>If you buy from a private individual as a non-resident, the <strong>4%</strong> ITP is paid in Spain using modelo 620; if you buy from a company, VAT. The boat is then deregistered from the Spanish register and registered in France with the <em>certificat d'enregistrement</em>. A used boat with European VAT paid does not pay VAT again in France. It is set out step by step in the <a href="/en/guias/comprar-barco-espana-matricular-francia.html">guide to buying in Spain and registering in France</a>.</p>

<h2 id="aqui">To keep it in Catalonia</h2>
<p>You can keep it under the Spanish flag in your name, or bring your French boat and moor it here without entry formalities. What matters is that it is used by you and people who do not live in Spain, that you have third-party liability insurance valid in Spain and the right licence. I explain it in the <a href="/en/guias/barco-frances-en-cataluna.html">guide to keeping your boat in Catalonia</a>.</p>

<h2 id="como">How we buy</h2>
<ol>
<li><strong>You tell me what you are looking for</strong>: type of boat, length, budget and whether you want to take it to France or keep it here.</li>
<li><strong>I go through the documentation with the seller</strong>: owner, charges, VAT, engines and flag.</li>
<li><strong>Sea trial and survey</strong>, if you want one, before leaving the deposit.</li>
<li><strong>Contract and paperwork</strong>, with a nautical agency (gestoría) handling the change of ownership or the deregistration for France.</li>
</ol>
<p>If the boat you are looking for is not on the list, <a href="/en/alertas/">create an alert</a> and I will let you know when one comes in that fits.</p>

<h2 id="faq">Frequently asked questions</h2>
<h3>Can I buy a boat in Spain if I live in France?</h3><p>Yes. You will normally need an NIE and, if you buy from a private individual, to pay the 4% ITP as a non-resident.</p>
<h3>Do I have to pay VAT again in France?</h3><p>No, if it is a used boat with European VAT paid. It is only paid in France if the boat counts as new (longer than 7.5 metres and less than 3 months or 100 hours of use).</p>
<h3>Can I see the boat before buying it?</h3><p>Of course. The advisable thing is to see it, do a sea trial and, if you want, a survey before leaving any deposit.</p>
""",
    faq=[("Can I buy a boat in Spain if I live in France?", "Yes. You will normally need an NIE and, if you buy from a private individual, to pay the 4% ITP as a non-resident."),
         ("Do I have to pay VAT again in France?", "No, if it is a used boat with European VAT paid. It is only paid in France if the boat counts as new (longer than 7.5 metres and less than 3 months or 100 hours of use)."),
         ("Can I see the boat before buying it?", "Of course. The advisable thing is to see it, do a sea trial and, if you want, a survey before leaving any deposit.")],
    note="Tax information for guidance only, reviewed in October 2026. This is not tax or legal advice and the rules may change. Confirm it with a nautical agency (gestoría) or with the authorities before buying.",
    card=dict(eyebrow="Do you live in France?", h3="I can help you find the boat.", p="Tell me what you are looking for, your budget and whether you want to take it to France or keep it here.", wa="Hello Juan, I live in France and I am looking for a used boat in Spain.", btn="Talk to Juan on WhatsApp"),
    rel=[("/en/guias/comprar-barco-espana-matricular-francia.html", "Buying in Spain and registering in France"), ("/en/guias/barco-frances-en-cataluna.html", "Keeping your boat in Catalonia if you live in France"), ("/en/comprar/barcos-segunda-mano-costa-brava.html", "Second-hand boats on the Costa Brava")],
    header_wa="Hello Juan, I live in France and I am looking for a boat in Spain.",
)

# Loose texts: link in guides index, FR home page and listings
INDEX_CARD = {
  "g1": dict(tag="Buying from France", h2="Buying a boat in Spain and registering it in France", p="Taxes in Spain, deregistration from the Spanish register, how to get it there and what paperwork France asks for."),
  "g2": dict(tag="If you live in France", h2="Keeping your boat in Catalonia if you live in France", p="French or Spanish flag, taxes, insurance, licence and moorings on the Costa Brava."),
}
