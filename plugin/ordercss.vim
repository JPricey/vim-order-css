if exists('g:loaded_order_css')
  finish
endif
let g:loaded_order_css = 1

let s:save_cpo = &cpo
set cpo&vim

let s:order_file = resolve(expand('<sfile>:p:h')) . '/ordercss.py'

function! <SID>OrderCssInner() range
  if !has('python')
    echo 'You need python support'
    return
  endif

  :py import vim, imp
  execute ':py ordercss = imp.load_source("ordercss", "' . s:order_file . '")'
  :py first_line = int(vim.eval('a:firstline'))
  :py last_line = int(vim.eval('a:lastline'))
  :py lines = list(vim.current.buffer.range(first_line, last_line))
  :py vim.current.buffer[first_line - 1:last_line] = ordercss.transform(lines)
endfunction

command! -range OrderCSS  <line1>,<line2>call <SID>OrderCssInner()

let &cpo = s:save_cpo
unlet s:save_cpo
