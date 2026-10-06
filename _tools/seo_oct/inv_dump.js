// Vuelca el inventario (con la titulación por idioma) a JSON para generar tarjetas estáticas.
global.location={pathname:'/'};global.window={};global.document={readyState:'loading',querySelectorAll:()=>[],addEventListener(){}};
require('../../inventario.js');const I=window.PM_INV;
const out=I.boats.map(b=>Object.assign({},b,{tl:{es:I.titleFor(b,'es'),ca:I.titleFor(b,'ca'),en:I.titleFor(b,'en'),fr:I.titleFor(b,'fr')}}));
console.log(JSON.stringify(out));
