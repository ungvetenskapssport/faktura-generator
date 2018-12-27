import subprocess
import os
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

d = {'INVOICENUMBER': '0', 
	'INVOICEDATE': "2018-12-26", 
	"YOURREF": "person ett",
	"OURREF": "person två",
	"ADDRESS": "Abcgatan 123",
	"PRODUCTS": r"\product{Programmeringsläger elev}{1500.0}{3}",
 }


produce_pdf(d, 'herp.pdf')

