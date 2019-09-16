command! -bar -nargs=0 LeaderfCppInclude call leaderf#CppInclude#startExpl(g:Lf_WindowPosition)

" In order to be listed by :LeaderfSelf
call g:LfRegisterSelf("LeaderfCppInclude", "navigate the cpp headers")

" Definition of 'arguments' can be similar as
" https://github.com/Yggdroot/LeaderF/blob/master/autoload/leaderf/Any.vim#L85-L140
let s:extension = {
            \   "name": "cppInclude",
            \   "help": "navigate the cpp headers",
            \   "registerFunc": "leaderf#CppInclude#register",
            \   "arguments": [
            \   ]
            \ }
" In order that `Leaderf marks` is available
call g:LfRegisterPythonExtension(s:extension.name, s:extension)
