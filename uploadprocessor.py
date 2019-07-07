import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time 
from text_detect import TextDetect
import json 

class EventHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(event.src_path)
        key= event.src_path[event.src_path.find("uploads/")+8: event.src_path.rfind("/")]
        fname = event.src_path[event.src_path.rfind("/")+1:]
        t=TextDetect()
        print(key+"\t"+fname)
        print("Grabbing data from cloud")
        results = t.detect_text_local(event.src_path)
       
        report={}
        report["filename"]= fname
        report["text"]= []
        for result in results:
            report["text"].append(result.description)

        resultsCaesar= t.caesar_decode(results, 33)
        report["caesar"]=resultsCaesar
        report["caesarbash"]= []
        report["rot13"]= []
        for result in results:
            print(result.description)
            report["caesarbash"].append(t.caesar_decode_bash(result.description))
        
        with open("reports/"+key+"/"+fname+".json", 'w') as f:
            json.dump(report,f, indent=4)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()