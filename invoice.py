content = r'''\documentclass[a4paper,11pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[swedish]{babel}
\usepackage[sc]{mathpazo}
\usepackage{tabularx}
\usepackage{fancyhdr}
\usepackage{lastpage}

\usepackage{booktabs}
\usepackage{fp}
\usepackage{ragged2e}
\usepackage{longtable}


\usepackage{fancybox}
\usepackage[margin=2cm,top=3cm]{geometry}

\newcounter{cnt}
\setcounter{cnt}{0}
\def\inc{\stepcounter{cnt}\thecnt}
\gdef\TotalHT{0}

\newcommand{\product}[3]{
\inc &#1  &#2 kr  &#3  &\FPmul\temp{#2}{#3}\FPround\temp{\temp}{2}\temp~kr
\FPadd\total{\TotalHT}{\temp}
\FPround\total{\total}{2}
\global\let\TotalHT\total
\\ }
\newcommand{\totalttc}{\TotalHT~kr}

\newcommand{\tax}{
  \FPmul\temp{\TotalHT}{.25}
  \FPround\temp{\temp}{2}
  \temp~kr
  \FPadd\totaltax{\TotalHT}{\temp}
  \FPround\totaltax{\totaltax}{2}
  \global\let\TotalHT\totaltax
}


\begin{document}


\pagestyle{fancy}
\fancyhf{}
\fancyfoot[R]{\footnotesize Sida \thepage\ av \pageref{LastPage}}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\setlength{\fboxsep}{1.5em}
\setlength{\parindent}{0pt}
\cornersize{.3}

{\huge Ung Vetenskapssport}



\fancyput*(230pt,-22pt){\ovalbox{
    \begin{minipage}{215pt}
      \huge Faktura
    \end{minipage}}}

\fancyput*(230pt,-82pt){\ovalbox{
    \begin{minipage}{87pt}
      \textbf{Fakturanummer:}\\ %(invoice_number)s 
    \end{minipage}}}

\fancyput*(358pt,-82pt){\ovalbox{
    \begin{minipage}{87pt}
      \textbf{Fakturadatum:}\\ %(invoice_date)s
    \end{minipage}}}

\vspace{3em}
\textbf{Fakturaadress:}\\[1em]
%(address)s

\fancyput*(230pt,-172pt){
    \begin{minipage}{85pt}
      \begin{tabular}{ll}
        \textbf{Er referens} & %(your_ref)s \\
        \textbf{Vår referens} & %(our_ref)s \\
        \textbf{Betalningsvilkor} & 30 dagar
      \end{tabular}
    \end{minipage}}

\vspace{15em}


\renewcommand\arraystretch{1.5}
\begin{tabular*}{\linewidth}{cp{8.9cm}rcr}\hline\hline
\textbf{Post} & \textbf{Benämning}  & \multicolumn{1}{l}{\textbf{\`A-pris}} &  \multicolumn{1}{l}{\textbf{Antal}} & \multicolumn{1}{l}{\textbf{Summa}} \\
\hline
    %(products)s

    &&&&\\[5em]

    \multicolumn{4}{r@{~~~}}{\textbf{Att betala}} & \totalttc\\
\hline\hline
\end{tabular*}
\renewcommand\arraystretch{1}

\fancyput*(-17pt,-580pt){\ovalbox{
    \begin{minipage}{450pt}
      \small Ange fakturanummer som referens vid inbetalning.
    \end{minipage}}}


\fancyput*(-17pt,-670pt){\mbox{
    \begin{minipage}{530pt}
      \begin{tabularx}{530pt}{XXX}
      \textbf{Adress:}  & \textbf{Kontonummer} & \textbf{Organisationsnummer} \\
      Ditt Företag      & 1234.12.345.67       & 123456-7890 \\
      Företagsvägen 3   &                      &  \\
      543 21~~Företagsstaden & \textbf{Bank}        & \textbf{Momsreg} \\
                        & Företagsbanken       & SE123456789012 \\
      \end{tabularx}
    \end{minipage}}}

\end{document}'''