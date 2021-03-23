from utils import collecting_jsonl
import srsly
import sys



def main(*args):
    text_list=[]
    for i in args[0]:
        print(i)
        collecting_jsonl(i,text_list)
    srsly.write_jsonl("pretrain_corpus.jsonl", text_list)
        
        



if __name__ == '__main__':
    main(sys.argv[1:])
