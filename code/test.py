import pickle
import pandas as pd
import key_to_entity as k2e

file = open("../data/freebase/ent2id.pkl",'rb')
object_file = pickle.load(file)
file.close()


a = 0

fb2wiki_map = {}



def txt_data_cleaning():
    with open("../data/freebase/fb2w.txt",'r') as f:
        for line in f.readlines():
            if not line.startswith("<http"):
                continue
            
            eles = line.strip().split("\t")
            fb_id = "/" + eles[0][1:-1].split("/")[-1].replace(".","/")
            wiki_url = eles[-1]
            for end in range(len(wiki_url)):
                if wiki_url[end] == ">":
                    wiki_url = wiki_url[1:end]
                    break
            a = 0
            fb2wiki_map[fb_id] = wiki_url

# check whether all entity id in map

def check_missing_fb_id():
    for k in object_file.keys():
        if k not in fb2wiki_map:
            print(k)
         
def write_to_csv():
    global req
    for k in object_file.keys():
        k2e.key_to_entity(k)
        req+=1
        with open('../data/req.txt', 'w') as f:
                f.write(str(req))
        if req%100==0:
            print(f'req={req}')
        if req>5000:
            break
        
if __name__ == "__main__":
    req=int(open('../data/req.txt').read())   
    write_to_csv()