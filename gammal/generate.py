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
        "ADDR":[
            "Addressrad 1: (Postadress)",
            "Adressrad 2: (Fortstn. postadress)",
            "Adressrad 3: (Postnummer)",
            "Adressrad 4 (Postort)"],
        "YOURREF" : "Referensnamn/nummer till faktura",
        "NOELEVER": "Hur många deltagare anmäler du? (skriv ett tal)",
        "NAMES" : "Namn på alla lägerdeltagare (rad-separerade)",
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
        exit(1)
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
    "UVSREF": "Julia Mårtensson",
    }
    d["YOURREF"] = row[cfg["YOURREF"]]
    addr = [row[addr_row] for addr_row in cfg["ADDR"]]
    addr = addr[:-2] + [addr[-2] + " " +  addr[-1]]
    d["ADDRESS"] = '\\\\\n'.join(filter(lambda x: x, addr))
    d["PRODUCTS"] = get_products(row[cfg["NOELEVER"]])
    return d

def get_participants(row):
    stud = int(row[cfg["NOELEVER"]])
    names = row[cfg["NAMES"]].strip().replace('\r', '\n').split('\n')
    emails = row[cfg["EMAILS"]].strip().replace('\r', '\n').split('\n')
    warnings = []
    if stud != len(names):
        warnings.append("wrong number of names {} {} {}".format(stud, names, emails))
    if stud != len(emails):
        warnings.append("wrong number of emails {} {} {}".format(stud, names, emails))
    return names, emails, warnings

def get_products(elever):
    s = []
    if int(elever):
        s.append(r"\product{Matematikläger elev 13-15 maj i Lund}{750.00}{" + str(elever) + "}")
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
