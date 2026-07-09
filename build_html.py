
# -*- coding: utf-8 -*-
"""Sestaví finální index.html s vloženými daty tréninkového plánu."""
import json

with open('/home/ubuntu/days_data.json', encoding='utf-8') as f:
    days_json = f.read()

# Data vložíme přímo do souboru (GitHub Pages nevyžaduje běhový fetch)
DAYS_CONST = "const DAYS = " + days_json + ";"

html = r'''<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>10denní tréninkový deník — Příprava a udržení kondice</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<script>
  // Vynutíme klasický JSX runtime, aby Babel v prohlížeči negeneroval "import" příkazy
  Babel.registerPreset('react-classic', {
    presets: [[Babel.availablePresets.react, { runtime: 'classic' }]]
  });
</script>
<style>
  :root{
    --pitch-900:#0B2B1E;
    --pitch-700:#164a32;
    --pitch-500:#1f6b47;
    --lime:#B6E33D;
    --lime-dim:#93bf2c;
    --chalk:#F4F2E9;
    --chalk-dim:#dad6c6;
    --navy:#0B1F3A;
    --amber:#FFB703;
    --ink:#132018;
    --line: rgba(244,242,233,0.14);
  }
  *{box-sizing:border-box;}
  html,body,#root{height:100%;}
  body{
    margin:0;
    background:
      radial-gradient(1200px 600px at 85% -10%, rgba(182,227,61,0.10), transparent 60%),
      radial-gradient(900px 500px at -10% 20%, rgba(255,183,3,0.06), transparent 55%),
      var(--pitch-900);
    color:var(--chalk);
    font-family:'Inter',sans-serif;
    -webkit-font-smoothing:antialiased;
  }
  .display{font-family:'Barlow Condensed',sans-serif; text-transform:uppercase; letter-spacing:0.02em;}
  .mono{font-family:'JetBrains Mono',monospace;}

  .wrap{max-width:1180px;margin:0 auto;padding:28px 20px 80px;}

  /* HERO */
  .hero{
    display:flex; flex-wrap:wrap; gap:24px; align-items:flex-end; justify-content:space-between;
    padding:30px 0 26px; border-bottom:1px solid var(--line); margin-bottom:28px;
  }
  .hero-left .eyebrow{
    display:inline-flex; align-items:center; gap:8px;
    font-size:12.5px; letter-spacing:0.14em; text-transform:uppercase;
    color:var(--lime); font-weight:600; margin-bottom:10px;
  }
  .eyebrow .dot{width:6px;height:6px;border-radius:50%;background:var(--lime);box-shadow:0 0 10px var(--lime);}
  .hero h1{
    font-size:clamp(38px,6vw,64px); line-height:0.95; margin:0 0 10px; font-weight:800;
  }
  .hero h1 span{color:var(--lime);}
  .hero p{max-width:520px; color:var(--chalk-dim); font-size:15px; line-height:1.55; margin:0;}

  .score-panel{
    background:linear-gradient(160deg, var(--pitch-700), var(--pitch-900));
    border:1px solid var(--line); border-radius:16px; padding:18px 22px; min-width:230px;
    box-shadow: 0 20px 40px -20px rgba(0,0,0,0.6);
  }
  .score-panel .label{font-size:11.5px; letter-spacing:0.12em; text-transform:uppercase; color:var(--chalk-dim); margin-bottom:6px;}
  .score-panel .value{display:flex; align-items:baseline; gap:8px;}
  .score-panel .value b{font-family:'Barlow Condensed',sans-serif; font-size:46px; font-weight:800; color:var(--lime);}
  .score-panel .value span{color:var(--chalk-dim); font-size:15px;}
  .score-track{height:6px; border-radius:4px; background:rgba(244,242,233,0.12); margin-top:12px; overflow:hidden;}
  .score-fill{height:100%; background:linear-gradient(90deg, var(--amber), var(--lime)); border-radius:4px; transition:width .4s ease;}

  /* TOOLBAR */
  .toolbar{display:flex; flex-wrap:wrap; gap:10px; margin-bottom:26px;}
  .btn{
    border:1px solid var(--line); background:rgba(244,242,233,0.04); color:var(--chalk);
    padding:9px 16px; border-radius:9px; font-size:13.5px; font-weight:600; cursor:pointer;
    display:inline-flex; align-items:center; gap:8px; transition:.15s ease;
  }
  .btn:hover{background:rgba(244,242,233,0.09); border-color:rgba(244,242,233,0.3);}
  .btn.primary{background:var(--lime); color:var(--pitch-900); border-color:var(--lime);}
  .btn.primary:hover{background:var(--lime-dim);}

  /* GRID of days */
  .day-grid{display:grid; grid-template-columns:repeat(auto-fill, minmax(340px,1fr)); gap:16px;}

  .card{
    background:rgba(244,242,233,0.035);
    border:1px solid var(--line);
    border-radius:16px;
    padding:18px 18px 16px;
    display:flex; flex-direction:column; gap:12px;
    transition:border-color .2s ease, transform .2s ease;
    position:relative;
    overflow:hidden;
  }
  .card.done{border-color:rgba(182,227,61,0.55);}
  .card.done::before{
    content:""; position:absolute; inset:0; pointer-events:none;
    background:linear-gradient(160deg, rgba(182,227,61,0.08), transparent 45%);
  }
  .card-top{display:flex; align-items:flex-start; justify-content:space-between; gap:10px;}
  .day-badge{display:flex; align-items:flex-start; gap:10px;}
  .num{
    font-family:'Barlow Condensed',sans-serif; font-weight:800; font-size:30px;
    width:46px; height:46px; border-radius:50%; display:flex; align-items:center; justify-content:center;
    background:var(--navy); border:1px solid var(--line); color:var(--chalk); flex:none;
  }
  .card.done .num{background:var(--lime); color:var(--pitch-900); border-color:var(--lime);}
  .day-titles .day-of{font-size:11px; letter-spacing:0.1em; text-transform:uppercase; color:var(--chalk-dim);}
  .day-titles h3{margin:2px 0 0; font-size:19px; font-weight:700; line-height:1.15; text-transform:uppercase; font-family:'Barlow Condensed',sans-serif; letter-spacing:0.01em;}
  .desc{font-size:13px; color:var(--chalk-dim); line-height:1.5;}

  /* Nadpisy sekcí uvnitř karty */
  .block-title{
    font-size:11px; letter-spacing:0.12em; text-transform:uppercase; color:var(--lime);
    font-weight:700; margin:6px 0 2px; display:flex; align-items:center; gap:7px;
  }
  .block-title::before{content:""; width:14px; height:2px; background:var(--lime); border-radius:2px;}

  .expand-btn{
    align-self:flex-start; background:none; border:none; color:var(--lime); font-size:13px; font-weight:600;
    cursor:pointer; padding:0; display:flex; align-items:center; gap:6px;
  }

  /* Popis tréninku – sekce */
  .sections{display:flex; flex-direction:column; gap:8px; margin-top:2px;}
  .section-row{
    padding:10px 11px; border-radius:9px;
    background:rgba(11,31,58,0.35); border:1px solid var(--line);
  }
  .section-head{display:flex; gap:10px; align-items:baseline;}
  .section-row .time{font-size:11px; color:var(--lime); font-weight:700; white-space:nowrap; min-width:52px;}
  .section-row .s-title{font-size:13.5px; font-weight:700;}
  .section-row .s-sub{font-size:12.5px; font-weight:600; color:var(--chalk); margin-left:4px;}
  .section-row .s-detail{font-size:12px; color:var(--chalk-dim); margin-top:4px; line-height:1.45;}
  .section-row .s-note{font-size:11.5px; color:var(--amber); margin-top:4px; line-height:1.4;}
  .exlist{list-style:none; margin:7px 0 0; padding:0; display:flex; flex-direction:column; gap:6px;}
  .exlist li{font-size:12px; line-height:1.4; padding-left:12px; position:relative; color:var(--chalk-dim);}
  .exlist li::before{content:""; position:absolute; left:0; top:6px; width:5px; height:5px; border-radius:50%; background:var(--lime-dim);}
  .exlist li b{color:var(--chalk);}
  .exlist li .param{color:var(--lime); font-weight:600;}

  /* Splněné úkoly */
  .tasks{display:flex; flex-direction:column; gap:6px;}
  .task-row{
    display:flex; gap:10px; align-items:center; padding:8px 10px; border-radius:9px;
    background:rgba(11,31,58,0.35); border:1px solid var(--line); cursor:pointer;
  }
  .task-row input[type=checkbox]{width:16px; height:16px; accent-color:var(--lime); flex:none; cursor:pointer;}
  .task-row .t-label{font-size:13px; font-weight:600;}
  .task-row.checked .t-label{text-decoration:line-through; color:var(--chalk-dim);}

  /* Metriky */
  .metrics{display:grid; grid-template-columns:1fr 1fr; gap:8px;}
  .metric{
    background:rgba(11,31,58,0.35); border:1px solid var(--line); border-radius:9px; padding:8px 10px;
    display:flex; flex-direction:column; gap:4px;
  }
  .metric .m-name{font-size:11px; font-weight:600; color:var(--chalk-dim); line-height:1.25;}
  .metric .m-input{display:flex; align-items:center; gap:6px;}
  .metric input{
    width:100%; background:rgba(11,31,58,0.6); border:1px solid var(--line); border-radius:6px;
    color:var(--chalk); font-family:'JetBrains Mono',monospace; font-size:13px; padding:5px 7px;
  }
  .metric input::placeholder{color:rgba(244,242,233,0.3);}
  .metric .m-unit{font-size:11px; color:var(--lime); font-weight:700; white-space:nowrap;}
  .metric .m-hint{font-size:10px; color:rgba(244,242,233,0.4); line-height:1.3;}

  .rating-row{display:flex; align-items:center; justify-content:space-between; gap:10px; margin-top:2px;}
  .rating-row .label{font-size:12px; color:var(--chalk-dim); text-transform:uppercase; letter-spacing:0.08em;}
  .rating-dots{display:flex; gap:4px;}
  .rdot{width:16px; height:16px; border-radius:4px; border:1px solid var(--line); cursor:pointer; background:transparent;}
  .rdot.on{background:var(--amber); border-color:var(--amber);}

  textarea.notes{
    width:100%; min-height:54px; resize:vertical; background:rgba(11,31,58,0.35);
    border:1px solid var(--line); border-radius:9px; color:var(--chalk); font-family:'Inter',sans-serif;
    font-size:12.5px; padding:8px 10px; line-height:1.4;
  }
  textarea.notes::placeholder{color:rgba(244,242,233,0.35);}

  .tip{
    font-size:12px; color:var(--chalk-dim); background:rgba(255,183,3,0.06);
    border:1px solid rgba(255,183,3,0.22); border-radius:9px; padding:8px 10px; line-height:1.45;
  }
  .tip b{color:var(--amber);}

  .footer-note{margin-top:40px; padding-top:20px; border-top:1px solid var(--line); font-size:12px; color:var(--chalk-dim); text-align:center;}

  input[type=file]{display:none;}

  @media (max-width:520px){
    .hero{flex-direction:column; align-items:flex-start;}
    .score-panel{width:100%;}
  }
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel" data-presets="react-classic">
const {useState, useEffect, useRef} = React;

__DAYS__

// Vytvoří prázdný počáteční stav pro všechny dny
function emptyState(){
  const s = {};
  DAYS.forEach(day=>{
    const metriky = {};
    day.metriky.forEach(m=>{ metriky[m.klic] = ""; });
    s[day.id] = {
      ukoly: day.ukoly.map(()=>false),
      metriky,
      notes:"",
      rating:0,
    };
  });
  return s;
}

function App(){
  const [state, setState] = useState(emptyState());
  const [expanded, setExpanded] = useState(()=>new Set([1]));
  const fileRef = useRef(null);

  // Přepnutí splnění úkolu
  const toggleTask = (dayId, idx) => {
    setState(prev=>{
      const day = {...prev[dayId]};
      const ukoly = [...day.ukoly];
      ukoly[idx] = !ukoly[idx];
      day.ukoly = ukoly;
      return {...prev, [dayId]: day};
    });
  };

  // Uložení hodnoty metriky
  const setMetric = (dayId, klic, val) => {
    setState(prev=>({
      ...prev,
      [dayId]: {...prev[dayId], metriky: {...prev[dayId].metriky, [klic]: val}}
    }));
  };

  const setNotes = (dayId, val) => {
    setState(prev=>({...prev, [dayId]: {...prev[dayId], notes: val}}));
  };

  const setRating = (dayId, val) => {
    setState(prev=>({
      ...prev,
      [dayId]: {...prev[dayId], rating: prev[dayId].rating === val ? val - 1 : val}
    }));
  };

  const toggleExpand = (dayId) => {
    setExpanded(prev=>{
      const next = new Set(prev);
      next.has(dayId) ? next.delete(dayId) : next.add(dayId);
      return next;
    });
  };

  // Den je splněn, pokud jsou zaškrtnuté všechny úkoly
  const isDayDone = (dayId) => state[dayId].ukoly.every(Boolean) && state[dayId].ukoly.length>0;
  const doneCount = DAYS.filter(d=>isDayDone(d.id)).length;
  const totalScore = DAYS.reduce((sum,d)=> sum + (state[d.id].rating||0), 0);

  // Export průběhu do JSON
  const exportData = () => {
    const blob = new Blob([JSON.stringify(state, null, 2)], {type:"application/json"});
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    const stamp = new Date().toISOString().slice(0,10);
    a.href = url; a.download = `treninkovy-denik-${stamp}.json`;
    document.body.appendChild(a); a.click(); a.remove();
    URL.revokeObjectURL(url);
  };

  // Import uloženého průběhu z JSON
  const importData = (e) => {
    const file = e.target.files[0];
    if(!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      try{
        const parsed = JSON.parse(ev.target.result);
        setState(prev=>{
          const merged = {...prev};
          Object.keys(parsed).forEach(k=>{
            if(merged[k]) merged[k] = {...merged[k], ...parsed[k]};
          });
          return merged;
        });
      }catch(err){
        alert("Soubor se nepodařilo načíst — zkontroluj, že jde o export z tohoto deníku.");
      }
    };
    reader.readAsText(file);
    e.target.value = "";
  };

  const resetAll = () => {
    if(confirm("Opravdu vymazat všechny zaškrtnuté úkoly, metriky, poznámky a hodnocení?")){
      setState(emptyState());
    }
  };

  return (
    <div className="wrap">
      <div className="hero">
        <div className="hero-left">
          <div className="eyebrow"><span className="dot"></span>Příprava · udržení kondice · 10 dní</div>
          <h1>Tréninkový<br/><span>deník</span></h1>
          <p>Desetidenní plán pro fotbalistu (krajský přebor, 25 let) — běh, síla, rychlost, obratnost a regenerace v jednom bloku. Sleduj úkoly, metriky a hodnocení každého dne.</p>
        </div>
        <div className="score-panel">
          <div className="label">Splněné dny</div>
          <div className="value"><b>{doneCount}</b><span>/ 10</span></div>
          <div className="score-track"><div className="score-fill" style={{width:`${doneCount*10}%`}}></div></div>
          <div className="label" style={{marginTop:14}}>Celkové hodnocení 10 dní</div>
          <div className="value"><b>{totalScore}</b><span>/ 100</span></div>
        </div>
      </div>

      <div className="toolbar">
        <button className="btn primary" onClick={exportData}>⬇ Uložit průběh (JSON)</button>
        <button className="btn" onClick={()=>fileRef.current.click()}>⬆ Načíst uložený průběh</button>
        <input ref={fileRef} type="file" accept="application/json" onChange={importData} />
        <button className="btn" onClick={resetAll}>↺ Vynulovat vše</button>
      </div>

      <div className="day-grid">
        {DAYS.map(day=>{
          const ds = state[day.id];
          const done = isDayDone(day.id);
          const isOpen = expanded.has(day.id);
          return (
            <div className={"card" + (done ? " done" : "")} key={day.id}>
              <div className="card-top">
                <div className="day-badge">
                  <div className="num">{day.id}</div>
                  <div className="day-titles">
                    <div className="day-of">Den {day.id} / 10 · Příprava</div>
                    <h3>{day.nazev}</h3>
                  </div>
                </div>
              </div>

              <div className="desc"><b style={{color:'var(--chalk)'}}>Zaměření: </b>{day.zamereni}</div>

              <button className="expand-btn" onClick={()=>toggleExpand(day.id)}>
                {isOpen ? "▲ Skrýt popis tréninku" : "▼ Zobrazit popis tréninku"}
              </button>

              {isOpen && (
                <div>
                  <div className="block-title">Popis tréninku</div>
                  <div className="sections">
                    {day.popis.map((sec, si)=>(
                      <div className="section-row" key={si}>
                        <div className="section-head">
                          {sec.cas && <span className="time">{sec.cas}</span>}
                          <span>
                            <span className="s-title">{sec.label}</span>
                            {sec.nazev && <span className="s-sub">· {sec.nazev}</span>}
                          </span>
                        </div>
                        {sec.popis && <div className="s-detail">{sec.popis}</div>}
                        {sec.cviky.length > 0 && (
                          <ul className="exlist">
                            {sec.cviky.map((c, ci)=>(
                              <li key={ci}>
                                <b>{c.nazev}</b>
                                {c.parametry && <span className="param"> — {c.parametry}</span>}
                                {c.popis && <span> · {c.popis}</span>}
                                {c.poznamka && <span style={{color:'var(--amber)'}}> ({c.poznamka})</span>}
                              </li>
                            ))}
                          </ul>
                        )}
                        {sec.poznamka && <div className="s-note">ℹ {sec.poznamka}</div>}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="block-title">Splněné úkoly</div>
              <div className="tasks">
                {day.ukoly.map((ukol, idx)=>(
                  <label className={"task-row" + (ds.ukoly[idx] ? " checked" : "")} key={idx}>
                    <input type="checkbox" checked={ds.ukoly[idx]} onChange={()=>toggleTask(day.id, idx)} />
                    <span className="t-label">{ukol}</span>
                  </label>
                ))}
              </div>

              <div className="block-title">Dnešní metriky</div>
              <div className="metrics">
                {day.metriky.map((m)=>(
                  <div className="metric" key={m.klic}>
                    <span className="m-name">{m.nazev}</span>
                    <div className="m-input">
                      <input
                        type="text"
                        value={ds.metriky[m.klic]}
                        placeholder={m.skala ? m.skala : "…"}
                        onChange={(e)=>setMetric(day.id, m.klic, e.target.value)}
                      />
                      {m.jednotka && <span className="m-unit">{m.jednotka}</span>}
                    </div>
                    {m.hint && <span className="m-hint">{m.hint}</span>}
                  </div>
                ))}
              </div>

              <div className="rating-row">
                <span className="label">Hodnocení dne</span>
                <div className="rating-dots">
                  {Array.from({length:10}).map((_,i)=>(
                    <button
                      key={i}
                      className={"rdot" + (i < ds.rating ? " on" : "")}
                      onClick={()=>setRating(day.id, i+1)}
                      aria-label={`Hodnocení ${i+1}`}
                    ></button>
                  ))}
                </div>
              </div>

              <textarea
                className="notes"
                placeholder="Poznámky k tréninku…"
                value={ds.notes}
                onChange={(e)=>setNotes(day.id, e.target.value)}
              />

              <div className="tip"><b>Tip na dnes:</b> {day.tip}</div>
            </div>
          );
        })}
      </div>

      <div className="footer-note">
        Data se ukládají jen v tomto prohlížeči během relace. Použij „Uložit průběh“ pro export a „Načíst uložený průběh“ pro obnovení příště.
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
</script>
</body>
</html>
'''

html = html.replace('__DAYS__', DAYS_CONST)
with open('/home/ubuntu/treninkovy-denik/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('index.html vytvořen, délka:', len(html), 'znaků')
