import subprocess
import os
import argparse
import datetime
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--csv')
    parser.add_argument('-o', '--outdir', default='out')
    parser.add_argument('-i', '--startindex', type=int, default=1) 
    return parser.parse_args()

cfg = {
        "ADDR":["Addressrad 0", 
            "Addressrad 1: (Postadress)",
            "Adressrad 2: (Fortstn. postadress)",
            "Adressrad 3: (Postnummer)",
            "Adressrad 4 (Postort)"],
        "YOURREF" : "Referensnamn till faktura och kuvert",
        "NOELEVER": "Varav antal Elever:",
        "NOTEACH": "Varav antal Lärare:",
        "NAMES" : "Namn på  alla lägerdeltagare (rad-separerade)",
        "EMAILS" : "Epost till alla lägerdeltagare (rad-separerade)"
        }


def produce_pdf(d, out):
    content = open('template.tex', 'r').read()
    for k, v in d.items():
        content = content.replace(k, v)
    tmpprefix = 'tmp'
    tmpname = 'tmp.tex'
    open(tmpname, 'w').write(content)
    proc = subprocess.Popen(['pdflatex', '-interaction', 'nonstopmode', tmpname])
    proc.communicate()
    if not proc.returncode == 0:
        print('Error while generating {}'.format(out))
        return
    os.rename(tmpprefix + '.pdf', out)
    suffx = ['.aux', '.tex', '.log']
    for v in suffx:
        os.unlink(tmpprefix + v)

def dt_str():
    def tostr(dt):
        return "{}-{}-{}".format(dt.year, dt.month, dt.day)
    d = datetime.date.today()
    return tostr(d), tostr(d + datetime.timedelta(days=30))

def get_inject(i, row):
    d = {"INVOICENUMBER": str(i), 
    "INVOICEDATE": dt_str()[0], 
    "LASTDATE" : dt_str()[1],
    "UVSREF": "Lars Åström",
    }
    d["YOURREF"] = row[cfg["YOURREF"]]
    addr = [row[addr_row] for addr_row in cfg["ADDR"]]
    addr = addr[:-2] + [addr[-2] + " " +  addr[-1]]
    d["ADDRESS"] = '\\\\\n'.join(filter(lambda x: x, addr))
    d["PRODUCTS"] = get_products(row[cfg["NOELEVER"]], row[cfg["NOTEACH"]])
    return d

def get_participants(row):
    stud, teach = int(row[cfg["NOELEVER"]]), int(row[cfg["NOTEACH"]])
    names = row[cfg["NAMES"]].strip().replace('\r', '\n').split('\n')
    emails = row[cfg["EMAILS"]].strip().replace('\r', '\n').split('\n')
    warnings = []
    if stud + teach != len(names):
        warnings.append("wrong number of names {} {} {}".format(stud + teach, names, emails))
    if stud + teach != len(emails):
        warnings.append("wrong number of emails {} {} {}".format(stud + teach, names, emails))
    return names, emails, warnings

def get_products(elever, lärare):
    s = []
    if int(elever):
        s.append(r"\product{Programmeringsläger elev 1-3 februari i Lund}{1500.0}{" + str(elever) + "}")
    if int(lärare):
        s.append(r"\product{Programmeringsläger lärare 1-3 februari i Lund}{3000.0}{" + str(lärare) + "}")
    return "\\\\\n".join(s)



if __name__ == '__main__':
    import csv
    args = get_args()
    out_folder = args.outdir.rstrip('/')
    try:
        os.makedirs(out_folder)
    except: pass
    persons = []
    warnings = []
    with open(args.csv) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for i, row in enumerate(reader):
            fno = i + args.startindex
            inject_dict = get_inject(fno, row)
            names, emails, ws = get_participants(row)
            warnings.extend(ws)
            for i in range(max(len(names), len(emails))):
                name = names[i] if i < len(names) else "-"
                email = emails[i] if i < len(emails) else "-"
                persons.append('{}\t{}\t{}\t{}'.format(name, email, row['Namn, anmälare'], row['E-postadress']))
            print(inject_dict)
            produce_pdf(inject_dict, '{}/{}.pdf'.format(args.outdir.rstrip('/'), fno))
    print('\n'.join(persons))
    print('\n'.join(warnings))
