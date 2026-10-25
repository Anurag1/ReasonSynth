"""Command-line interface."""
import argparse,json
from pathlib import Path
from .benchmark import evaluate

def main():
    parser=argparse.ArgumentParser(prog="unseen"); sub=parser.add_subparsers(dest="command",required=True); run=sub.add_parser("evaluate"); run.add_argument("--out",default="results/demo.json"); args=parser.parse_args()
    if args.command=="evaluate":
        result=evaluate(); out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2),encoding="utf-8")
        print(json.dumps({"output":str(out),"benchmark":result["benchmark"],"status":result["status"],"summary":result["summary"],"paired_graph_minus_text_accuracy":result["paired_graph_minus_text_accuracy"]},indent=2))
if __name__=="__main__": main()
