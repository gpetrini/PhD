(defun set-region-writeable (begin end)
  "Removes the read-only text property from the marked region."
  ;; See http://stackoverflow.com/questions/7410125
  (interactive "r")
  (let ((modified (buffer-modified-p))
        (inhibit-read-only t))
    (remove-text-properties begin end '(read-only t))
    (set-buffer-modified-p modified)))



(defun transclusion-tangle-include ()
  "Transclude all files, them executes org-babel-tangle to finally remove all transclusion"
  (interactive)
  (org-transclusion-add-all)
  ;; (org-babel-tangle)
  ;; (org-transclusion-remove-all)
  )
