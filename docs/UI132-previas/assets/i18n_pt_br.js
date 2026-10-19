/* UI118: only authored UI literals pass through this adapter. No DOM observer,
 * storage rewrite, global fetch interception, or automatic translation of records. */
(function(global){
 'use strict';
 const locale=global.WAVELINK_LOCALE==='pt-BR'?'pt-BR':'en';
 const dictionary=Object.freeze(global.WAVELINK_PT_BR||{});
 const own=(o,k)=>Object.prototype.hasOwnProperty.call(o,k);
 const folded=new Map(Object.keys(dictionary).map(key=>[key.toLocaleLowerCase('en'),key]));
 function t(source){
  if(typeof source!=='string'||locale!=='pt-BR')return source;
  if(own(dictionary,source))return dictionary[source];
  const key=source.trim().replace(/\s+/g,' ');
  let match=own(dictionary,key)?key:folded.get(key.toLocaleLowerCase('en'));
  let prefix='',suffix='';
  if(!match){const decorated=key.match(/^([＋+✓→↗›]\s*)(.*)$/);if(decorated){prefix=decorated[1];match=folded.get(decorated[2].toLocaleLowerCase('en'));}}
  if(!match&&key.endsWith(':')){suffix=':';match=folded.get(key.slice(0,-1).toLocaleLowerCase('en'));}
  if(!match)return source;
  let translated=dictionary[match];
  if(/[A-Z]/.test(key)&&key===key.toUpperCase())translated=translated.toLocaleUpperCase('pt-BR');
  return source.slice(0,source.length-source.trimStart().length)+prefix+translated+suffix+source.slice(source.trimEnd().length);
 }
 const decode=s=>s.replace(/&(?:amp|lt|gt|quot|#39|apos|nbsp);/g,x=>({'&amp;':'&','&lt;':'<','&gt;':'>','&quot;':'"','&#39;':"'",'&apos;':"'",'&nbsp;':' '}[x]));
 const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 function textFragment(source){
  const decoded=decode(source),translated=t(decoded);
  if(translated!==decoded)return escape(translated);
  if(decoded.includes('\uE000')){
   const markers=[];
   const key=decoded.replace(/\uE000\d+\uE001/g,marker=>'{'+(markers.push(marker)-1)+'}');
   const localized=t(key);
   if(localized!==key)return escape(localized.replace(/\{(\d+)\}/g,(match,i)=>markers[Number(i)]??match));
   return source.split(/(\uE000\d+\uE001)/g).map((part,i)=>i%2?part:textFragment(part)).join('');
  }
  // Separators delimit independent authored labels; interpolated values never
  // enter this function. Retain punctuation and whitespace exactly.
  return source.split(/(\s*[·|]\s*|\s+—\s+)/).map((part,i)=>i%2?part:(t(decode(part))!==decode(part)?escape(t(decode(part))):part)).join('');
 }
 function markup(source){
  if(locale!=='pt-BR'||typeof source!=='string')return source;
  return source.replace(/\b(aria-label|title|placeholder|alt)=(['"])(.*?)\2/gi,(_,name,quote,value)=>name+'='+quote+textFragment(value)+quote)
   .replace(/(^|>)([^<>]+)(?=<|$)/g,(_,start,body)=>start+textFragment(body));
 }
 function html(strings,...values){
  // Translation is applied to the source segments before user values are joined.
  let source='';
  for(let i=0;i<strings.length;i++)source+=strings[i]+(i<values.length?'\uE000'+i+'\uE001':'');
  return markup(source).replace(/\uE000(\d+)\uE001/g,(_,i)=>String(values[Number(i)]));
 }
 function template(strings,...values){
  if(locale!=='pt-BR'){let result='';for(let i=0;i<strings.length;i++)result+=strings[i]+(i<values.length?String(values[i]):'');return result;}
  const source=strings.map((s,i)=>s+(i<values.length?'{'+i+'}':'')).join('');
  const translated=t(source);
  if(translated!==source)return translated.replace(/\{(\d+)\}/g,(_,i)=>String(values[Number(i)]));
  let result='';for(let i=0;i<strings.length;i++)result+=t(strings[i])+(i<values.length?String(values[i]):'');return result;
 }
 function status(value){const raw=String(value||'');const names={"open": "Em aberto", "closed": "Encerrado", "submitted": "Enviado para revisão", "returned": "Devolvido para correção", "pending": "Pendente", "completed": "Concluído", "in_progress": "Em andamento", "not_started": "Não iniciado", "cancelled": "Cancelado", "postponed": "Adiado", "general": "Trabalho operacional", "maintenance": "Atividade de manutenção", "certificate_review": "Conferência de certificado de equipamento", "stock_verification": "Conferência de inventário", "asset": "Equipamento", "certificate": "Certificado de equipamento", "approved": "Aprovado", "unreviewed": "Ainda não revisado", "issue": "Problema", "na": "Não se aplica", "done": "Concluído", "low": "Baixa", "normal": "Normal", "high": "Alta", "urgent": "Urgente", "day": "Dia", "week": "Semana", "month": "Mês", "due_date": "Prazo da ordem", "completion": "Conclusão da ordem", "create_general": "Tarefa criada", "save_work": "Trabalho realizado salvo", "submit": "Resultados enviados para revisão", "review": "Decisão da revisão registrada", "return": "Devolvido para correção", "reopen": "Tarefa reaberta", "reassign": "Responsáveis ou prazo alterados", "comment": "Comentário registrado", "postpone": "Tarefa adiada", "resume_task": "Trabalho retomado", "record_check": "Resultado da conferência salvo", "create": "Registro criado", "update": "Registro atualizado", "cancel": "Cancelamento registrado", "finalised": "Finalizado", "draft": "Rascunho", "unfinished": "Não concluído", "ready": "Pronto para revisão", "rejected": "Rejeitado", "recorded": "Registrado", "active": "Ativo", "archived": "Arquivado", "expired": "Vencido", "reviewed": "Revisado"};return locale==='pt-BR'&&own(names,raw)?names[raw]:t(raw.replaceAll('_',' ').replace(/^./,v=>v.toUpperCase()));}
 // UI126: use only at known authored-message boundaries. Never pass record text.
 const importPatterns = [[" {0} formula cells are omitted; calculation results are not imported.", " {0} células com fórmulas foram omitidas; resultados de cálculos não são importados."], [" {0} rows share source identities with another worksheet; review them before a separate import.", " {0} linhas compartilham identificadores do original com outra aba; confira-as antes de importar separadamente."], ["A box row must represent one container; use quantity 1 or Unknown. {0}", "Uma linha de caixa deve representar um único contêiner; use quantidade 1 ou Não informada. {0}"], ["An answer cell on page {0} could not be matched to readable check text. Review the source row.", "Uma célula de resposta na página {0} não pôde ser associada a um texto legível de verificação. Confira a linha no original."], ["Box references must be unique within each selected worksheet. {0} {1}", "As referências às caixas devem ser únicas em cada aba selecionada. {0} {1}"], ["Choose an existing supported original up to {0} MB.", "Escolha um arquivo existente de até {0} MB."], ["Choose an original file between 1 byte and {0} MB.", "Escolha um arquivo com tamanho entre 1 byte e {0} MB."], ["Excel row {0}", "Linha {0} do Excel"], ["Extracted block {0}", "Bloco extraído {0}"], ["Imported from {0}; SHA-256 {1}. {2}Reviewed draft; original layout and completed history are not copied.", "Imported from {0}; SHA-256 {1}. {2}Rascunho conferido; a diagramação original e o histórico preenchido não são copiados."], ["Inventory row {0}: review the mapped columns or edited tab-separated rows.", "Inventory row {0}: confira a correspondência das colunas ou as linhas editadas com separação por tabulação."], ["Item and inventory headers identify {0} source records.", "Os cabeçalhos de itens e inventário identificam {0} registros no original."], ["Notes exceed 4,000 characters after retaining the source location; review the notes before saving. {0}", "As observações ultrapassam 4.000 caracteres após preservar o local original; confira-as antes de salvar. {0}"], ["OCR used on pages {0}. Verify spelling, numbers, units and row order against the source.", "Leitura de imagens (OCR) usada nas páginas {0}. Confira a grafia, os números, as unidades e a ordem das linhas no original."], ["Page {0}", "Página {0}"], ["Pages without readable text were skipped because OCR is unavailable: {0}", "Páginas sem texto legível ignoradas porque o OCR está indisponível: {0}"], ["Review box references: a box cannot be its own parent. {0}", "Confira as referências às caixas: uma caixa não pode conter a si mesma. {0}"], ["Review box references: a parent must be an explicitly marked box in the same worksheet. {0}{1}", "Confira as referências às caixas: a caixa que contém o item deve estar marcada explicitamente como caixa na mesma aba. {0}{1}"], ["Review box references: the imported hierarchy exceeds eight parent-container levels. {0}", "Confira as referências às caixas: a hierarquia importada ultrapassa oito níveis de caixas. {0}"], ["Review box references: the imported hierarchy has a cycle. {0}", "Confira as referências às caixas: a hierarquia importada contém um vínculo circular. {0}"], ["Source line {0}", "Linha {0} do original"], ["Suggested type: {0}. Review the selected destination before saving.", "Suggested type: {0}. Confira o destino selecionado antes de salvar."], ["This original is referenced by {0} saved draft, revision or record entries. Keep it archived; referenced originals cannot be permanently deleted.", "Este original é referenciado por {0} entradas de rascunhos, revisões ou registros salvos. Mantenha-o arquivado; originais referenciados não podem ser excluídos definitivamente."], ["Worksheet {0}, source row {1}", "Aba {0}, linha {1} do original"], ["extracted row {0}", "Linha extraída {0}"], ["{0} formula cells omitted. Formulas, macros and links never run.", "Células com fórmulas omitidas: {0}. Fórmulas, macros e vínculos nunca são executados."], ["{0} headers identify a reusable data or definition worksheet.", "Os cabeçalhos de {0} identificam uma aba reutilizável de dados ou definições."], ["{0} metadata/header lines omitted from the proposal. Check the complete extracted text below.", "{0} linhas de identificação ou cabeçalho foram omitidas da proposta. Confira o texto completo extraído abaixo."], ["{0} of {1} source rows also appear in {2}. Review material is kept separate to avoid importing those rows twice.", "{0} de {1} linhas do original também aparecem em {2}. O material de conferência é mantido separado para evitar importar essas linhas duas vezes."], ["{0} unsupported or invalid PDF form inputs were not mapped. Review them against the source.", "Campos de formulário PDF incompatíveis ou inválidos não mapeados: {0}. Confira-os no original."], ["{0}, extracted row {1}", "{0}, linha extraída {1}"], ["{0}: enter {1}{2} characters on one line.", "{0}: informe {1}{2} caracteres em uma única linha."], ["{0}; no verified counts or custody copied", "{0}; contagens conferidas e custódia não são copiadas"]].map(([source,translated])=>{
  const indices=[],parts=source.split(/(\{\d+\})/),escapeRegex=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
  const expression=parts.map(p=>/^\{\d+\}$/.test(p)?(indices.push(Number(p.slice(1,-1))),'([\\s\\S]{0,4000}?)'):escapeRegex(p)).join('');
  return {pattern:new RegExp('^(?:'+expression+')$'),indices,translated};
 });
 function message(source){
  if(locale!=='pt-BR'||typeof source!=='string'||source.length>16000)return source;
  const exact=t(source);if(exact!==source)return exact;
  for(const {pattern,indices,translated} of importPatterns){const match=source.match(pattern);if(match){const values=new Map(indices.map((index,i)=>[index,match[i+1]]));return translated.replace(/\{(\d+)\}/g,(token,index)=>values.get(Number(index))??token);}}
  return source;
 }
 Object.defineProperty(global,'WavelinkI18n',{value:Object.freeze({locale,t,markup,html,template,status,message}),writable:false,configurable:false});
 if(global.document)global.document.documentElement.lang=locale;
})(window);
