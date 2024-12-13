(defun reverse
   (lambda (list)
     (reverse-itr list '())))

(defun reverse-itr
   (lambda (list itr)
     (if list
       (reverse-itr (cdr list) (cons (car list) itr))
      itr)))

'testy
(reverse '(1 2 3 'a b c () (3 4 5)))
(reverse (list 2 3 4))
(reverse (cons 4 (cons 5 ( cons 6 nil))))