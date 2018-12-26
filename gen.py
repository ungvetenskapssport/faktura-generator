from invoice import content

def produce_pdf(d):
    open('tmp.tex', 'w').write(content%d)


d = {'invoice_number': '0', 
	'invoice_date': "2018-12-26", 
	"your_ref": "person ett",
	"our_ref": "person två",
	"products": r"\product{Programmeringsläger elev}{1500.0}{3}",
	"address": "Abcgatan 123",
 }


produce_pdf(d)

