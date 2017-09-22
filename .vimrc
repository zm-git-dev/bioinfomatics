set nu
set tabstop=4
syntax on
set foldenable
set shiftwidth=4
set hlsearch
set ignorecase
set encoding=utf-8
set list
set listchars=tab:>-,trail:-
set foldmethod=syntax

autocmd BufNewFile *.py,*.pl, exec ":call SetTitle()"  
let $author_name = "yaomingyue"  
let $author_email = "yaomingyue@fuanhua.com"  
      
func SetTitle()  
if &filetype == 'python'  
call setline(1,"\###################################################################")  
call append(line("."), "\# File Name: ".expand("%"))  
call append(line(".")+1, "\# Author: ".$author_name)  
call append(line(".")+2, "\# mail: ".$author_email)  
call append(line(".")+3, "\# Created Time: ".strftime("%c"))  
call append(line(".")+4, "\#=============================================================")  
call append(line(".")+5, "\#!/usr/bin/env python")
call append(line(".")+6, "\#-*- coding:utf8 -*-")  
call append(line(".")+7, "")  
else  
call setline(1,"\###################################################################")  
call append(line("."), "\# File Name: ".expand("%"))  
call append(line(".")+1, "\# Author: ".$author_name)  
call append(line(".")+2, "\# mail: ".$author_email)  
call append(line(".")+3, "\# Created Time: ".strftime("%c"))  
call append(line(".")+4, "\#=============================================================")  
call append(line(".")+5, "\#!/usr/bin/env perl")
call append(line(".")+6, "\use strict;")
call append(line(".")+7, "\use warnings;")  
call append(line(".")+8, "")  
endif  
endfunc 
