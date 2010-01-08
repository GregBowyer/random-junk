(def rounds        (ref 20000))
(def philosophers  (doall (map #(agent %) (repeat 5 0))))
(def forks         (doall (map #(ref [% true]) (range (count philosophers)))))
(def eaten         (ref {}))
(def logger        (agent 0))

(defn debug  [_ id msg r]
  (println id \space msg "(" r ")")
  (flush))

(defn my-forks [id]
  (map #(nth (cycle forks) (+ (count forks) %)) [id (dec id)]))

(defn got-forks?  [id]
  (every? #(= true (second (deref %))) (my-forks id)))

(defn handle-forks [id action]
  (doseq [fork (my-forks id)]
    (ref-set fork [(first @fork) (condp = action :take false :release true)])))

(defn behave [a id]
  (dosync                           ; Initiate transaction
   (when (pos? (ensure rounds))     ; Is there more food?
     (if (> 5 (rand-int 10))        ; Do I want to eat or think?
       (when (got-forks? id)        ; Are both of my forks available?
         (handle-forks id :take)
         (alter rounds dec)
         (send logger debug id "ate    " @rounds)
         (handle-forks id :release))
       (send logger debug id "thinks " @rounds))
     (send-off *agent* behave id))
    (if (= 0 @rounds)
      (send logger debug id "Ate myself sick" @rounds))))

(doseq [i (range (count philosophers))]
  (send logger debug i "being sent off to dinner" @rounds)
  (send-off (nth philosophers i) behave i))
