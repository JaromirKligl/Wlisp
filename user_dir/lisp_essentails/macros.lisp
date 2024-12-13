(defmacro let
   (lambda (binding binds body)
      (list 'apply 
            (list 'lambda binding
            body)
            (list 'quote binds))))

(defmacro test
   (lambda (x)
     (list '+ x x)))

(defmacro and
   (lambda (x y)
     (list 'if x y 'nil)))

(defmacro or
   (lambda (x y)
     (list 'if x x y)))