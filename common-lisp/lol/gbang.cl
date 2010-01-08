(defun g!-symbol-p (s)
  (and (symbolp s)
       (> (length (symbol-name s)) 2)
       (string= (symbol-name s)
            "G!" :start1 0 :end1 2)))

(defun flatten (forms)
  (labels ((rec (forms accum)
                (cond ((null forms) accum)
                      ((atom forms) (cons forms accum))
                      (t (rec (car forms) (rec (cdr forms) accum))))))
    (rec forms nil)))

(defmacro defmacro/g! (name args &rest body)
  (let ((syms (remove-duplicates
                (remove-if-not #'g!-symbol-p
                               (flatten body)))))

    `(defmacro ,name ,args
       (let ,(mapcar 
               (lambda (S)
                 `(,s (gensym ,(subseq (symbol-name s) 2))))
               syms)
         ,@body))))

(let ((*print-circle* t))
  (print
    (macroexpand-1
      `(defmacro/g! nif (expr pos zero neg)
            '(let ((,g!result ,expr))
               (cond ((plusp ,g!result), pos)
                     ((zerop ,g!result), zero)
                     (t ,neg)))))))
