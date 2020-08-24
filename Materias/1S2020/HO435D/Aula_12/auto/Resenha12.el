(TeX-add-style-hook
 "Resenha12"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "11pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8") ("fontenc" "T1") ("ulem" "normalem")))
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
    "hyperref")
   (LaTeX-add-labels
    "sec:org0b5b182"
    "sec:org79b974c"
    "sec:org0127f5b"
    "sec:org5daa007"
    "sec:orge831dc6"
    "sec:orgf7554d5"
    "sec:org35b87f7"
    "sec:org820e0f5"
    "sec:orga088201"
    "sec:org3f39d2e"
    "sec:org227760e"
    "sec:org0b22cd0"
    "sec:orgf7ff27b"
    "sec:org7b185ac"
    "sec:org4151d5e"
    "sec:org30d021e"
    "sec:orgd9c0e60"
    "sec:orgdfbb6b4"
    "sec:org3f2273a"
    "sec:org11da158"
    "sec:org9a6e241"
    "sec:orgdee1f43"
    "sec:orge7ffc64"
    "sec:orgaa2d63d"
    "sec:org8e4c9bc"
    "sec:orgb513217"
    "sec:orgbe115be"
    "sec:org75803b2"
    "sec:org0d06ec2"
    "sec:org957273f"
    "sec:orgc3bb45e"
    "sec:org4cd3246"
    "sec:orged76489"
    "sec:org2128045"
    "sec:orge8788e2"
    "sec:orgdd8221a"))
 :latex)

