(setq py-isort-packages
      '((py-isort :location local)))

(defun py-isort/init-py-isort ()
  (use-package py-isort
    :init (add-hook 'before-save-hook 'py-isort-before-save)))
