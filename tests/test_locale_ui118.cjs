/* Authored UI translation must never rewrite an interpolated company record. */
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const root=process.env.WAVELINK_TEST_SOURCE;
if(!root)throw Error('Set WAVELINK_TEST_SOURCE to the reconstructed runtime.');
function setup(locale){const context={window:{WAVELINK_LOCALE:locale}};vm.createContext(context);for(const file of ['locale_pt_br.js','i18n_pt_br.js'])vm.runInContext(fs.readFileSync(path.join(root,'app/static',file),'utf8'),context);return context.window.WavelinkI18n;}
const pt=setup('pt-BR'),en=setup('en');
assert.equal(pt.t('HR & personal records'),'Recursos Humanos');
assert.equal(pt.t('My HR records'),'Meus registros de RH');
assert.equal(pt.t('Sign out'),'Sair');
assert.equal(pt.t('Unknown user-written record'),'Unknown user-written record');
assert.equal(pt.html`<h1>${'Home'}</h1><button>Save</button>`,'<h1>Home</h1><button>Salvar</button>');
assert.equal(pt.html`<p>${'Draft'}</p><p>${'Travel'}</p>`,'<p>Draft</p><p>Travel</p>');
assert.equal(pt.markup('<option value="draft">Draft</option>'),'<option value="draft">Rascunho</option>');
assert.equal(pt.markup('<input name="status" value="Pending" placeholder="Search">'),'<input name="status" value="Pending" placeholder="Pesquisar">');
assert.equal(pt.template`${3} active`,'3 ativos');
assert.equal(pt.template`Open account menu for ${'Home'}`,'Abrir menu da conta de Home');
assert.equal(en.html`<p>${null} · ${undefined}</p><button>Save</button>`,'<p>null · undefined</p><button>Save</button>');
assert.equal(en.template`Hello\n${'Home'}`,'Hello\nHome');
assert.equal(en.t('HR & personal records'),'HR & personal records');
assert.equal(setup('pt-PT').locale,'en');
assert(Object.isFrozen(pt));
console.log(JSON.stringify({checks:15,passed:15}));
