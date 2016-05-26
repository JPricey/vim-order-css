let s:save_cpo = &cpo
set cpo&vim

let s:order_file = resolve(expand('<sfile>:p:h')) . '/ordercss.py'

function! <SID>OrderCssInner() range
  if !has('python')
    echo 'You need python support'
    return
  endif

  execute 'pyfile ' . s:order_file
endfunction

command! -range OrderCSS  <line1>,<line2>call <SID>OrderCssInner()

let &cpo = s:save_cpo
unlet s:save_cpo
