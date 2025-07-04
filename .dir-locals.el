((python-mode
  . ((pyvenv-activate . "./venv")
     (python-shell-interpreter . "python3")
     (eval . (setq-local lsp-pyright-venv-path
                         (expand-file-name "venv" (locate-dominating-file buffer-file-name ".dir-locals.el")))))))
