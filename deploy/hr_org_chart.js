function renderOrg(){
  const chart=directory.org_chart, records=el('hr-records');
  el('hr-pages').replaceChildren();el('hr-pages').hidden=true;
  const row=person=>'<li><strong>'+E(person.name)+'</strong>'+(person.title?'<small>'+E(person.title)+'</small>':'')+'</li>';
  const members=people=>'<ul>'+people.map(row).join('')+'</ul>';
  const card=unit=>{
    const heading=unit.name||orgText('Sem departamento','No department');
    const leadership=unit.heads.length?'<div class="hr-org-head"><b>'+E(orgText('Liderança','Leadership'))+'</b>'+members(unit.heads)+'</div>':
      unit.name?'<p class="muted">'+E(chart.show_heads?orgText('Liderança não definida','Leadership not defined'):orgText('Liderança não disponível nesta visão','Leadership unavailable in this view'))+'</p>':'';
    return '<article class="hr-org-unit"><h3>'+E(heading)+'</h3>'+leadership+members(unit.people)+'</article>';
  };
  records.innerHTML='<p>'+E(orgText('Pessoas por departamento. A liderança aparece quando há uma designação explícita visível para você.','People by department. Leadership is shown when an explicit designation is visible to you.'))+'</p>'+
    (chart.units.length?'<div class="hr-org-grid">'+chart.units.map(card).join('')+'</div>':'<p>'+E(orgText('Nenhuma pessoa visível.','No visible people.'))+'</p>');
}
