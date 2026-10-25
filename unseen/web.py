from http.server import BaseHTTPRequestHandler,HTTPServer
import json
from .benchmark import evaluate
def render():
 d=evaluate(); rows=''.join(f"<tr><td>{a}</td><td>{m['correct']}/{m['total']}</td><td>{m['accuracy']:.0%}</td></tr>" for a,m in d['summary'].items())
 return f"<!doctype html><meta name=viewport content='width=device-width,initial-scale=1'><title>UNSEEN Evidence Lab</title><style>body{{background:#0b1020;color:#f3f6fd;font:16px/1.5 -apple-system,sans-serif;max-width:900px;margin:auto;padding:24px}}section{{background:#151d31;border:1px solid #293650;border-radius:16px;padding:18px;margin:14px 0}}p{{color:#aab6cc}}td,th{{padding:8px;border-bottom:1px solid #293650}}pre{{white-space:pre-wrap;color:#a9e8d6}}</style><small>UNSEEN · EVIDENCE LAB / PROTOTYPE 001</small><h1>See the tension.<br>Test the connection.</h1><p>{d['case_count']} synthetic cases · Four comparison arms</p><section><h2>Smoke-test summary</h2><table><tr><th>Arm</th><th>Correct</th><th>Accuracy</th></tr>{rows}</table><p>Rule-based prototype only; not evidence of modern AI performance.</p></section><section><h2>Inspect one case</h2><pre>{json.dumps(next(x for x in d['cases'] if x['arm']=='graph'),indent=2)}</pre></section><section><h2>Scientific status</h2><p>Synthetic cases validate execution only. A held-out, matched-model evaluation is needed before any graph-superiority claim.</p></section>"
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  data=json.dumps(evaluate(),indent=2) if self.path=='/api/results' else render(); b=data.encode(); self.send_response(200); self.send_header('Content-Type','application/json' if self.path=='/api/results' else 'text/html; charset=utf-8'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
 def log_message(self,*args): pass
def main():
 print('UNSEEN running at http://127.0.0.1:8000'); HTTPServer(('127.0.0.1',8000),Handler).serve_forever()
if __name__=='__main__':main()
