% This class file is provided for authors submitting to the
% Genetics Society of America's G3: Genes | Genomes |
% Genetics Journal
%
% Version: 1.6, 2019/04/15
%
% Produced by Overleaf (www.overleaf.com)
%
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{style}[2019/09/25 v0.1]

%% Choose template type
\newcommand*{\templatetype}[1]{%
	\RequirePackage{#1}}

\RequirePackage{xifthen}
\newboolean{displaylineno}
\setboolean{displaylineno}{false}

\usepackage{lipsum}

\AtEndOfClass{\RequirePackage[tracking=smallcaps]{microtype}}
\DeclareOption{lineno}{\setboolean{displaylineno}{false}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{extarticle}}
\ProcessOptions*
\LoadClass{extarticle}

% Fonts and language
\RequirePackage[utf8]{inputenc}
\RequirePackage[brazilian]{babel}
\RequirePackage{amsmath,amsfonts,amssymb}
\RequirePackage{mathpazo}
\RequirePackage[scaled]{helvet}
\RequirePackage[T1]{fontenc}
\RequirePackage{url}
\RequirePackage{pifont}
\RequirePackage[switch,pagewise]{lineno}

%% For the Significance Statement & footnote on the first page
\RequirePackage{afterpage}
\RequirePackage{xcolor}
\RequirePackage{tikz}
\RequirePackage[framemethod=tikz]{mdframed}


\newcommand{\watermarkfont}{\color{black50}\normalfont\fontsize{10}{12}\selectfont}
\newcommand{\headerfont}{\normalfont\sffamily\fontsize{8}{10}\selectfont}
\newcommand{\titlefont}{\color{color3}\normalfont\sffamily\bfseries\fontsize{21}{23}\selectfont}
\newcommand{\datesfont}{\normalfont\sffamily\itshape\fontsize{8}{10}\selectfont}
\renewcommand\UrlFont{\color{blue}\sffamily}
\newcommand{\absfont}{\normalfont\sffamily\linespread{1.2}\fontsize{10}{12}\selectfont}
\newcommand{\keywordstitlefont}{\color{color4}\normalfont\sffamily\linespread{1.2}\fontsize{8}{10}\selectfont}
\newcommand{\keywordsfont}{\normalfont\sffamily\linespread{1.2}\fontsize{10}{12}\selectfont}
\newcommand{\copyrightfont}{\normalfont\sffamily\fontsize{7}{9}\selectfont}
\newcommand{\footerfont}{\normalfont\sffamily\fontsize{8}{10}\selectfont}

\RequirePackage{enumitem} 
\setlist[itemize]{noitemsep}


% Author and affiliation
\RequirePackage{authblk}
\setlength{\affilsep}{0.1em}
\renewcommand\Authfont{\color{color0}\normalfont\sffamily\bfseries\fontsize{9}{13}\selectfont}
\renewcommand\Affilfont{\color{color0}\normalfont\sffamily\fontsize{8}{10}\selectfont}
\makeatletter
\renewcommand\AB@affilsepx{, \protect\Affilfont}
\makeatother
\renewcommand\Authands{ and }

% Choose article type
\newcommand*{\articletype}[1]{%
  \RequirePackage{styles/#1}}
  
% Options for element switching
\RequirePackage{xifthen}
\RequirePackage{etoolbox}
\newboolean{displaycopyright}

% Graphics, tables and other formatting
\RequirePackage{graphicx,xcolor}
\RequirePackage{colortbl}
\RequirePackage{booktabs}
\RequirePackage{tikz}
\RequirePackage{algorithm}
\RequirePackage[noend]{algpseudocode}
\RequirePackage{changepage}
\RequirePackage[left=36pt,%
                right=36pt,%
                top=48pt,%
                bottom=60pt,%
                headheight=40pt,%
                headsep=10pt,%
                letterpaper,twoside]{geometry}%
\RequirePackage[labelfont={bf,sf},%
                labelsep=space,%
                figurename=Figure,%
                singlelinecheck=off,%
                justification=RaggedRight]{caption}
\setlength{\columnsep}{24pt} % Distance between the two columns of text
\setlength{\parindent}{12pt} % Paragraph indent

% Set document color scheme
\definecolor{black50}{gray}{0.5} % 50% black for hrules
\definecolor{color0}{RGB}{0,0,0} % Base color
\definecolor{color1}{RGB}{246, 245, 209} % Table column heads background
% color2 defined by the specific article type style file
\definecolor{color3}{RGB}{0,55,123} % Article Titles
\definecolor{color4}{RGB}{134,0,55} % Subheadings: A heads and “Abstract”
\definecolor{tabledingbat}{RGB}{184,108,108} % Table dingbat icon
% For sig statement box
\definecolor{stylebluetext}{RGB}{0,101,165} %
\definecolor{styleblueback}{RGB}{205,217,235} %
%\definecolor{stylebluetext}{RGB}{0,115,209} % Not used
%\definecolor{styleblueback}{RGB}{210,230,247} % Not used


% Bibliography
\usepackage[backend=biber,
			style = abnt,%
			noslsn, %
			extrayear, %
			uniquename=init,% 
			giveninits, %
			justify, %
			sccite,% 
			scbib, %
			repeattitles, %
			doi=false,isbn=false,url=false, 
			maxcitenames=3]{biblatex}
\addbibresource{bibliografia.bib}

% Table style
\arrayrulecolor{color0} % Set the color of the horizontal rules
\renewcommand{\arraystretch}{1.5} % Increased line spacing
%\captionsetup[table]{position=below} % Reduce spacing below caption
\colorlet{tableheadcolor}{color1} % Set table header colour
\newcommand{\header}{\rowcolor{tableheadcolor}} % create the command for the header
%\captionsetup[table]{name={{\color{tabledingbat}\textrm{\ding{110}}}\hspace{0.8em}Table}} % Add the icon to the left of the table name

% Algorithm style
\makeatletter
\newcommand\fs@coloruled{\def\@fs@cfont{\bfseries}\let\@fs@capt\floatc@coloruled
  \def\@fs@pre{\kern2pt}%
  \def\@fs@post{\kern2pt{\color{color2}\hrule}\relax}%
  \def\@fs@mid{\kern2pt{\color{color2}\hrule}\kern2pt}%
  \let\@fs@iftopcapt\iftrue}
\makeatother

\floatstyle{coloruled}
\restylefloat{algorithm}


% Headers
\RequirePackage{fancyhdr}  % custom headers/footers
\fancyhead[LO,RE,LE,RO]{} % Blank headers for non-title pages.
% Footers
\lfoot{}
\cfoot{}
\rfoot{}
\makeatletter
\fancyfoot[LE]{{\footerfont \thepage\hspace{1em}|\hspace{1em}\@runningauthor \hspace{0.2em}}}
\fancyfoot[R]{\footerfont\thepage}
\makeatother
\renewcommand{\headrulewidth}{0pt}% % No header rule
\renewcommand{\footrulewidth}{0pt}% % No footer rule

%% Dropped capital for first letter of main text
\newcommand{\dropcap}[1]{\lettrine[lines=2,lraise=0.05,findent=0.1em, nindent=0em]{{\dropcapfont{#1}}}{}}



% Article type header box
\newcommand{\articletypemark}{
\begin{textblock}{200}(378,36)
\begin{flushright}
{\raggedleft \headerfont\color{black} \textls[96]{\articletypename}}
\end{flushright}
\end{textblock}
}

% Colored margin box
\newcommand{\marginmark}{
\begin{textblock}{72}(506,0) 
\noindent
\begin{tikzpicture}[x=1,y=1]
\fill[color=color2] (0,0) rectangle (72,36);
\end{tikzpicture}
\end{textblock}
}

%% 13 July 2016: make sure sections are unnumbered
\setcounter{secnumdepth}{0}
\setcounter{tocdepth}{0}

% Section/subsection/paragraph set-up
\RequirePackage[explicit]{titlesec}
\renewcommand{\thesubsection}{\Alph{subsection}}

\titleformat{\section}
  {\large\sffamily\bfseries\color{color4}}
  {\thesection.}
  {0.5em}
  {\MakeUppercase{#1}}
  []
\titleformat{name=\section,numberless}
  {\large\sffamily\bfseries\color{color4}}
  {}
  {0em}
  {\MakeUppercase{#1}}
  []
\titleformat{\subsection}
  {\sffamily\bfseries}
  {\thesubsection.}
  {0.5em}
  {#1}
  []
\titleformat{\subsubsection}[runin]
  {\sffamily\bfseries\itshape}
  {\thesubsubsection.}
  {0.5em}
  {#1}
  []
\titleformat{\paragraph}[runin]
  {\sffamily\small\bfseries}
  {}
  {0em}
  {#1}
\titlespacing*{\section}{0pc}{3ex \@plus4pt \@minus3pt}{5pt}
\titlespacing*{\subsection}{0pc}{2.5ex \@plus3pt \@minus2pt}{2pt}
\titlespacing*{\subsubsection}{0pc}{2ex \@plus2.5pt \@minus1.5pt}{2pt}
\titlespacing*{\paragraph}{0pc}{1.5ex \@plus2pt \@minus1pt}{12pt}

% Article meta data additional fields
\newcommand{\runningauthor}[1]{\def\@runningauthor{#1}}
%% Backward compatibility
\newcommand{\correspondingauthor}[1]{\runningauthor{#1}}
\newcommand{\keywords}[1]{\def\@keywords{#1}}
\newcommand{\runningtitle}[1]{\def\@runningtitle{#1}}

\newcommand{\keywordname}{Palavras-chave} % Defines the keywords heading name

\def\xabstract{abstract}
\long\def\abstract#1\end#2{\def\two{#2}\ifx\two\xabstract
\long\gdef\theabstract{\ignorespaces#1}
\def\go{\end{abstract}}\else
\typeout{^^J^^J PLEASE DO NOT USE ANY \string\begin\space \string\end^^J
COMMANDS WITHIN ABSTRACT^^J^^J}#1\end{#2}
\gdef\theabstract{\vskip12pt BADLY FORMED ABSTRACT: PLEASE DO
NOT USE {\tt\string\begin...\string\end} COMMANDS WITHIN
THE ABSTRACT\vskip12pt}\let\go\relax\fi
\go}


% Set environment for abstract content and styling
\newcommand{\abscontent}{%
	\begin{minipage}[t]{453pt}
		%% v1.6: add line numbers toggle
		\ifthenelse{\boolean{displaylineno}}{\internallinenumbers}{}
		{\color{black50}\rule{\linewidth}{0.5pt}}
		\vskip9pt%
		{\absfont\bfseries\color{color4} Resumo} \absfont \theabstract%
		\vskip1pt%
		{\color{black50}\rule{\linewidth}{0.5pt}}
	\end{minipage}\hspace{15pt}
	\begin{minipage}[t]{72pt}
		\vskip18.3pt%
		{\keywordstitlefont\bfseries\keywordname} \\ \keywordsfont \@keywords%
	\end{minipage}
}%

% Custom title page
\renewcommand{\@maketitle}{\bgroup\setlength{\parindent}{0pt}%
	\begin{adjustwidth}{0pt}{24pt}
		\begin{flushleft}
			{%
				\vskip96pt%
				{\raggedright \titlefont \@title\par}%
				\vskip11pt%
				{\raggedright \@date\par}
				\vskip11pt
				{\raggedright \@author\par}
				\vskip20pt%
			}%
		\end{flushleft}
	\end{adjustwidth}
	\egroup
	{%
		\abscontent
	}%
	\vskip10pt%
}%


%% v1.6: add line numbers toggle
\ifthenelse{\boolean{displaylineno}}{\appto{\maketitle}{\linenumbers}}{}

% Other packages
\RequirePackage{enumitem} % For reducing bullet list item separation

\RequirePackage{tabularx}

\RequirePackage[flushmargin,ragged]{footmisc}

\newlength{\myFootnoteWidth}%
\newlength{\myFootnoteLabel}%
\setlength{\myFootnoteLabel}{0.5em}
\renewcommand{\@makefntext}[1]{%
  \setlength{\myFootnoteWidth}{\columnwidth}%
  \addtolength{\myFootnoteWidth}{-\myFootnoteLabel}%
  \noindent\makebox[\myFootnoteLabel][r]{\@makefnmark\ }%
  \parbox[t]{\myFootnoteWidth}{#1}
  }

% Commands to set the footnote for the front page.
\renewcommand{\footnoterule}{%
  \kern -3pt
  {\color{black50} \hrule width \columnwidth height 0.5pt}
  \kern 2.5pt
}

\newcommand{\@authfootnote}[2]{%
  \nolinenumbers\begingroup
  \setlength{\myFootnoteLabel}{0em}
  \renewcommand\thefootnote{}\footnote{\footnotelayout\copyrightfont\textsuperscript{#1}#2}%
   \endgroup%
}

\newcommand\blfootnote[1]{%
  \@authfootnote{}{#1}%
%   \begingroup
%   \setlength{\myFootnoteLabel}{0em}
%   \renewcommand\thefootnote{}\footnote{#1}%
%   \addtocounter{footnote}{-1}%
%   \addtocounter{Hfootnote}{-1}%
%   \endgroup%
}

\newcommand\correspondingauthoraffiliation[2]{%
  \@authfootnote{#1}{#2}%
%   \begingroup
%   \setlength{\myFootnoteLabel}{0em}
%   \renewcommand\thefootnote{}\footnote{\footnotelayout\copyrightfont\textsuperscript{1}#1}%
%   \endgroup
  %% v1.6: add line numbers toggle
  \ifthenelse{\boolean{displaylineno}}{\par\linenumbers}{}
}

\newcommand{\equalcontrib}[1]{\@authfootnote{#1}{These authors contributed equally to this work.}}

\newenvironment{tableminipage}[1]{\begin{minipage}{#1}\renewcommand\footnoterule{ \kern -1ex}%
\setlength{\myFootnoteLabel}{0.5em}%
}{\end{minipage}}

% Package to enable absolute positioning of figures
\RequirePackage[absolute,overlay]{textpos}
\setlength{\TPHorizModule}{1pt}
\setlength{\TPVertModule}{1pt}
\textblockorigin{0pt}{0pt} % start everything near the top-left corner


%% Author and affiliation
\RequirePackage{authblk}
\setlength{\affilsep}{8.5pt} % 16.5pts between base of author line and base of affil line
\renewcommand\Authfont{\color{color0}\normalfont\sffamily\bfseries\fontsize{9}{11}\selectfont}
\renewcommand\Affilfont{\color{color0}\normalfont\sffamily\fontsize{7}{8}\selectfont}

\renewcommand\AB@affilsepx{; \protect\Affilfont}

\renewcommand\Authands{, e }

%% Headers and footers
\RequirePackage{fancyhdr}  % custom headers/footers
\RequirePackage{lastpage}  % Number of pages in the document
\pagestyle{fancy}          % Enables the custom headers/footers

\fancypagestyle{firststyle}{
	\fancyfoot[R]{\footerfont NEI IE/Unicamp\hspace{7pt}|\hspace{7pt}\textbf{\today}\hspace{7pt}|\hspace{7pt}No. 01\hspace{7pt}|\hspace{7pt}\textbf{\thepage\textendash\pageref{LastPage}}}
	\fancyfoot[L]{\footerfont\@ifundefined{@doi}{}{\@doi}}
}

%% Set up the acknowledgments field
\titleclass{\acknow@section}{straight}[\part]
\newcounter{acknow@section}
\providecommand*{\toclevel@acknow@section}{0}
% Format is set for research articles by default
\titleformat{\acknow@section}[runin]
{\sffamily\normalsize\bfseries}
{}
{0em}
{#1.}
[]
\titlespacing{\acknow@section}
{0pt}
{3.25ex plus 1ex minus .2ex}
{1.5ex plus .2ex}


\newcommand{\showacknow}{% Display acknowledgments section
	\@ifundefined{@acknow}{}{
		\vskip 3.25ex plus 1ex minus .2ex
		\noindent{\sffamily\normalsize\bfseries AGRADECIMENTOS.\hspace{1.5ex plus .2ex}}
		\small\@acknow}
}

%% Set up the first page footnote/fact box here
\RequirePackage{float}
\floatstyle{plain}
\newfloat{sigstatement}{b!}{sst}
\newfloat{duvidas}{b!}{sst}
\newfloat{criticas}{b!}{sst}

\definecolor{color2}{RGB}{130,0,0} % color



%% Article meta data additional fields
\newcommand{\doi}[1]{\def\@doi{#1}}
\newcommand{\leadauthor}[1]{\def\@leadauthor{#1}}
\newcommand{\etal}[1]{\def\@etal{#1}}
\newcommand{\authorcontributions}[1]{\def\@authorcontributions{#1}}
\newcommand{\authordeclaration}[1]{\def\@authordeclaration{#1}}
\newcommand{\equalauthors}[1]{\def\@equalauthors{#1}}
\newcommand{\matmethods}[1]{\def\@matmethods{#1}}
\newcommand{\acknow}[1]{\def\@acknow{#1}}

\setlength{\footskip}{40pt}% ...at least 39.28502pt
\RequirePackage[colorlinks=true, allcolors=blue]{hyperref} % Fixing: “name{Hfootnote.xx} has been referenced but does not exist”

