if leaderf#versionCheck() == 0
    finish
endif

exec g:Lf_py "import vim, sys, os.path"
exec g:Lf_py "cwd = vim.eval('expand(\"<sfile>:p:h\")')"
exec g:Lf_py "sys.path.insert(0, os.path.join(cwd, 'python'))"
exec g:Lf_py "from cppIncludeExpl import *"

function! leaderf#CppInclude#Maps()
  nmapclear <buffer>

  nnoremap <buffer> <silent> q    :exec g:Lf_py "cppIncludeExplManager.quit()"<CR>
  nnoremap <buffer> <silent> i    :exec g:Lf_py "cppIncludeExplManager.input()"<CR>
  nnoremap <buffer> <silent> <F1> :exec g:Lf_py "cppIncludeExplManager.toggleHelp()"<CR>
  nnoremap <buffer> <silent> <CR> :exec g:Lf_py "cppIncludeExplManager.accept()"<CR>
endfunction

function! leaderf#CppInclude#startExpl(win_pos, ...)
  call leaderf#LfPy("cppIncludeExplManager.startExplorer('" . a:win_pos . "')")
endfunction

function! leaderf#CppInclude#register(name)
exec g:Lf_py "<< EOF"
from leaderf.anyExpl import anyHub
anyHub.addPythonExtension(vim.eval("a:name"), cppIncludeExplManager)
EOF
endfunction

