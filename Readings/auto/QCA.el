(TeX-add-style-hook
 "QCA"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "11pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8") ("fontenc" "T1") ("ulem" "normalem") ("biblatex" "style=abnt" "noslsn" "extrayear" "uniquename=init" "giveninits" "justify" "sccite" "	scbib" "repeattitles" "doi=false" "isbn=false" "url=false" "maxcitenames=2" "natbib=true" "backend=biber") ("geometry" "right=2cm" "left=2cm" "top=2cm" "bottom=2cm")))
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "href")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art11"
    "inputenc"
    "fontenc"
    "graphicx"
    "grffile"
    "longtable"
    "wrapfig"
    "rotating"
    "ulem"
    "amsmath"
    "textcomp"
    "amssymb"
    "capt-of"
    "hyperref"
    "biblatex"
    "geometry")
   (LaTeX-add-labels
    "sec:org5bfade9"
    "sec:org97ff468"
    "sec:orgcc3ffa3"
    "sec:org27541fd")
   (LaTeX-add-bibliographies
    "QCA.bib"))
 :latex)

