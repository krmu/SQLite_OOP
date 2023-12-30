import sqlite3
import os
import uuid
class Apstrade:
    con = None
    cur = None
    tabulu_nosaukumi = {"prieksmeti":"prieksmeti","atzimes":"atzimes","prieksmeti":"prieksmeti","skoleni":"skoleni"}
    def __init__(self):
        self.con = sqlite3.connect(f"{os.path.dirname(os.path.realpath(__file__))}/datubaze.db")
        self.con.row_factory = self.dict_factory
        self.cur = self.con.cursor()  
    def dict_factory(self,cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description): d[col[0]] = row[idx]
        return d
    def ir_tads_prieksmets(self,nosaukums):
        return self.cur.execute(f" select * from prieksmeti where nosaukums like '%{nosaukums}%'").fetchone()
    def viss_skolenu_saraksts(self):
        return self.cur.execute("select * from skoleni").fetchall()
    def labot_macibu_prieksmeta_nosaukumu(self,nosaukums,id):
        self.cur.execute(f"update prieksmeti set nosaukums='{nosaukums}' where id ='{id}' ")
        self.con.commit()
    def videjais(self):
        return self.cur.execute(f"SELECT round(AVG(atzime),2) as videjais,pr.nosaukums,count(atzime) FROM {self.tabulu_nosaukumi['atzimes']} left join {self.tabulu_nosaukumi['prieksmeti']} pr on  {self.tabulu_nosaukumi['atzimes']}.prieksmets = pr.id group by pr.nosaukums ").fetchall()
    def jauns_skolens(self,vards,uzvards,studenta_kods):
        self.cur.execute(f"insert into {self.tabulu_nosaukumi['skoleni']} (uuid,vards,uzvards,studenta_kods) values (?,?,?,?) ",(str(uuid.uuid4()),vards,uzvards,studenta_kods))
        self.con.commit()
    def skolena_videjais(self,uzvards):
        return self.cur.execute(f"SELECT round(AVG(atzime),2) as atzime,pr.nosaukums,sk.vards as vards,sk.uzvards as uzvards FROM atzimes left join prieksmeti pr on  atzimes.prieksmets = pr.id left join skoleni sk on  atzimes.skolens = sk.uuid where sk.uzvards like '%{uzvards}%' group by pr.nosaukums ").fetchall()
    def jauns_prieksmets(self,nosaukums):
        self.cur.execute(f"insert into {self.tabulu_nosaukumi['prieksmeti']} (id,nosaukums) values (?,?) ",(str(uuid.uuid4()),nosaukums))
        self.con.commit()    
    def skolena_visas_atzimes(self,uzvards):
        return self.cur.execute(f"SELECT atzime, pr.nosaukums FROM {self.tabulu_nosaukumi['atzimes']} left join {self.tabulu_nosaukumi['prieksmeti']} pr on  {self.tabulu_nosaukumi['atzimes']}.prieksmets = pr.id left join {self.tabulu_nosaukumi['skoleni']} sk on  {self.tabulu_nosaukumi['atzimes']}.skolens = sk.uuid where sk.uzvards like '%{uzvards}%' order by pr.nosaukums").fetchall()
    def visu_skolenu_videjie(self,cik = 10):
        return self.cur.execute(f"SELECT round(AVG(atzime),2) videjais,pr.nosaukums,sk.vards,sk.uzvards,sk.uuid FROM {self.tabulu_nosaukumi['atzimes']} left join {self.tabulu_nosaukumi['prieksmeti']} pr on  {self.tabulu_nosaukumi['atzimes']}.prieksmets = pr.id left join {self.tabulu_nosaukumi['skoleni']} sk on  {self.tabulu_nosaukumi['atzimes']}.skolens = sk.uuid group by sk.uuid limit {cik}").fetchall()
    def visi_macibu_prieksmeti(self):
        return self.cur.execute(f"select * from {self.tabulu_nosaukumi['prieksmeti']} order by nosaukums")