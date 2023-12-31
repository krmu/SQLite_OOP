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
    def atzimes_macibu_prieksmeta(self,nosaukums):
        masivs = []
        if self.ir_tads_prieksmets(nosaukums) is not None:
            visi_skoleni = self.viss_skolenu_saraksts()
            for sk in visi_skoleni:
                ir_atzime = self.cur.execute(f"SELECT atz.*,atz.uuid as atzimesid,pr.id as prid,pr.nosaukums from {self.tabulu_nosaukumi['atzimes']} atz left join {self.tabulu_nosaukumi['prieksmeti']} pr on atz.prieksmets = pr.id where pr.nosaukums like '%{nosaukums}%' and atz.skolens ='{sk['uuid']}' ").fetchone()
                objekta_dati = {"skid":sk['uuid'],"vards":sk['vards'],"uzvards":sk['uzvards'],"atzimesID":None,"atzime":None}
                if ir_atzime is not None:
                    objekta_dati['atzimesID'] = ir_atzime['atzimesid']
                    objekta_dati['atzime'] = ir_atzime['atzime']
                    objekta_dati['prieksmeta_nosaukums'] = ir_atzime['nosaukums']
                else:
                    prieksmets = self.ir_tads_prieksmets(nosaukums)
                    objekta_dati['atzimesID'] = f"Jauna_{sk['uuid']}_{prieksmets['id']}"
                    objekta_dati['prieksmeta_nosaukums'] = prieksmets['nosaukums']
                masivs.append(objekta_dati)       
            return masivs
        #return self.cur.execute(f"SELECT sk.*,atz.atzime,atz.uuid as atzimesID, pr.nosaukums FROM {self.tabulu_nosaukumi['skoleni']} sk left join {self.tabulu_nosaukumi['atzimes']} atz on atz.skolens = sk.uuid join {self.tabulu_nosaukumi['prieksmeti']} pr on atz.prieksmets = pr.id where pr.nosaukums like '%{nosaukums}%' ").fetchall()
    def dzest_atzimi(self,atzimes_id):
        self.cur.execute(f"delete from atzimes where `uuid` = '{atzimes_id}' ")
        self.con.commit()
    def mainit_atzimi(self,atzimes_id,vertiba):
        if vertiba == "":
            return "Atzīme nevar būt tukšums!"
        try:
            # Ja ievadi var pārtaisīt par skaitli
            vertiba = int(vertiba)
        except:
            return "Atzīmei jābūt skaitlim robežās no 1 līdz 10"
        if "Jauna_" in atzimes_id and int(vertiba) in [1,2,3,4,5,6,7,8,9,10]:
            atzimes_dalas = atzimes_id.split("_")
            self.cur.execute(f"insert into atzimes (uuid,prieksmets,atzime,skolens) values (?,?,?,?)",(str(uuid.uuid4()),atzimes_dalas[2],vertiba,atzimes_dalas[1]))
            self.con.commit()
        elif vertiba in [1,2,3,4,5,6,7,8,9,10]:  
            self.cur.execute(f"update atzimes set atzime='{vertiba}' where uuid ='{atzimes_id}' ")
            self.con.commit()
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