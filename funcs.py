import pandas as pd
def id_check_func(line_user_id):
    df = pd.read_csv("http://ik1-334-27288.vs.sakura.ne.jp/hack10/user_data.csv",encoding="SHIFT-JIS")
    i=0
    for x in df["line_id"]:
        if line_user_id == x  :
            return df["repl_id"][i]
        i=i+1
    return "error"
