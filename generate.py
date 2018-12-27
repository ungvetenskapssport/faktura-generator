import subprocess
import os
import argparse
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--csv')
    parser.add_argument('-o', '--outdir', default='out')
    parser.add_argument('-i', '--startindex', type=int, default=1) 
    return parser.parse_args()


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

def get_inject(i, row):
    d = {"INVOICENUMBER": str(i), 
    "INVOICEDATE": "2018-12-26", 
    "LASTDATE" : "2019-01-25",
    "UVSREF": "Lars Åström",
    }
    d["YOURREF"] = row["Referens"]
    d["ADDRESS"] = '\\\\\n'.join(row["Adress"].split('\n'))
    d["PRODUCTS"] = get_products(row["Anmälda Elever"], row["Anmälda Lärare"])
    return d

def get_products(elever, lärare):
    s = []
    if int(elever):
        s.append(r"\product{Programmeringsläger elev}{1500.0}{" + str(elever) + "}")
    if int(lärare):
        s.append(r"\product{Programmeringsläger lärare}{3000.0}{" + str(lärare) + "}")
    return "\\\\\n".join(s)


if __name__ == '__main__':
    import csv
    args = get_args()
    with open('anmalningar.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for i, row in enumerate(reader):
            fno = i + args.startindex
            inject_dict = get_inject(fno, row)
            print(inject_dict)
            produce_pdf(inject_dict, '{}.pdf'.format(fno))
