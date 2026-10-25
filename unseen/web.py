"""Dependency-free local evidence review UI."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import html, json
from .benchmark import evaluate

def render():
    result=evaluate()
    rows="".join(f"<tr><td>{html.escape(a)}</td><td>{m['correct']}/{m['total']}</td><td>{m['accuracy']:.0%}</td></tr>"
                 for a,m in result["summary"].items())
    cases=[r for r in result["cases"] if r["arm"]=="graph"]
    options="".join(f'<option value="{html.escape(c["case_id"])}">{html.escape(c["case_id"])} — {html.escape(c["category"])}</option>' for c in cases)
    data=json.dumps(result).replace("</","<\\/")
    return f"""<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>UNSEEN Evidence Lab</title><style>
:root{{--bg:#0b1020;--panel:#151d31;--muted:#aab6cc;--ink:#f3f6fd;--line:#293650;--accent:#8ce0c2}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif}}
main{{max-width:1000px;margin:auto;padding:28px 18px 60px}}.eyebrow{{color:var(--accent);letter-spacing:.16em;font-size:.75rem;font-weight:700}}h1{{font-size:clamp(2.4rem,7vw,4.2rem);line-height:1;margin:12px 0}}
p,.muted{{color:var(--muted)}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px}}.card{{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:18px;margin:14px 0}}
table{{width:100%;border-collapse:collapse}}td,th{{padding:10px;text-align:left;border-bottom:1px solid var(--line)}}select,button{{background:#202c45;color:var(--ink);border:1px solid #3a4a68;border-radius:10px;padding:10px;font:inherit}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;color:#d9e4f5}}.pill{{border:1px solid var(--line);border-radius:99px;padding:5px 10px;color:var(--accent)}}.warning{{border-left:4px solid #f4c970;padding-left:12px}}
</style></head><body><main><div class="eyebrow">UNSEEN · EVIDENCE LAB / PROTOTYPE 001</div>
<h1>See the tension.<br>Test the connection.</h1><p>Inspect contradiction cases through text, structured evidence and graph representations.</p>
<div class="grid"><div class="card"><div class="muted">Smoke benchmark</div><h2>{result["case_count"]} synthetic cases</h2><span class="pill">4 experimental arms</span></div>
<div class="card"><div class="muted">Graph − text accuracy</div><h2>{result["paired_graph_minus_text_accuracy"]:+.1%}</h2><p>Heuristic prototype only; not evidence of LLM performance.</p></div></div>
<section class="card"><h2>Arm summary</h2><table><thead><tr><th>Arm</th><th>Correct</th><th>Accuracy</th></tr></thead><tbody>{rows}</tbody></table></section>
<section class="card"><h2>Inspect a case</h2><select id="case">{options}</select> <button onclick="showCase()">Inspect</button><div id="detail"></div></section>
<section class="card warning"><h2>Scientific status</h2><p>Synthetic cases and a rule-based solver validate execution paths only. No graph-superiority claim is warranted without a held-out, matched-model evaluation.</p></section>
<script>const DATA={data};
function showCase(){{const id=document.getElementById('case').value;const arr=DATA.cases.filter(x=>x.case_id===id);const g=arr.find(x=>x.arm==='graph'),t=arr.find(x=>x.arm==='text');if(!g)return;const esc=s=>s.replace(/[&<>]/g,c=>({{"&":"&amp;","<":"&lt;",">":"&gt;"}}[c]));document.getElementById('detail').innerHTML='<h3>'+id+' · '+g.category+'</h3><p><b>Gold:</b> '+g.gold+' · <b>Text:</b> '+t.prediction+' · <b>Graph:</b> '+g.prediction+'</p><pre>'+esc(JSON.stringify(g.view,null,2))+'</pre>'}}
showCase();</script></main></body></html>"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path=="/api/results":
            body=json.dumps(evaluate(),indent=2).encode(); content="application/json; charset=utf-8"
        else:
            body=render().encode(); content="text/html; charset=utf-8"
        self.send_response(200); self.send_header("Content-Type",content)
        self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body)
    def log_message(self,*args): pass

def main():
    print("UNSEEN running at http://127.0.0.1:8000")
    HTTPServer(("127.0.0.1",8000),Handler).serve_forever()
if __name__=="__main__": main()
