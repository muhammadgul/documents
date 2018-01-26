# documents
git clone https://github.com/muhammadgul/documents.git

myCv contains cv.tex that can be run via "xelatex cv.tex"

coverLetter contains CoverLetter.tex, that can be run by simple "pdflatex CoverLetter.tex"

ResearchInterest consists of statement.tex, that can be run by "pdflatex statement.tex", and bibtex for bibliography

All the three pdf files can be combine by "pdfunite coverLetter/CoverLetter.pdf myCv/cv.pdf ResearchInterest/statement.pdf application.pdf"

Thesis can be run as ```pdflatex PhD.tex``` and bib can be run as ```bibtex PhD.aux```

The ```pdflatex PhD.tex``` commond can be then run twice for proper run.
