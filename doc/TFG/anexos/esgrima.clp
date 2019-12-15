;---------------------------------
;
;     PLANTILLA
;
;----------------------------------



(deftemplate tirador
  (slot id
    (type SYMBOL)
    (allowed-symbols yo el)
    (default el)
  )
  (slot edad
    (type INTEGER)
  )
  (slot altura
    (type INTEGER)
  )
  (slot puno
    (type SYMBOL)
    (allowed-symbols frances anatomico)
    (default frances)
  )
  (slot intimidado
    (type SYMBOL)
    (allowed-symbols si no)
    (default no)
  )

)

;---------------------------------
;
;     REGLAS
;
;----------------------------------

(defrule cogerDatosTiradorEl "coger datos"

  ?el <- (tirador (id el) (edad ?edadEl)(altura ?alturaEl)(puno ?punoEl)(intimidado ?intimidadoEl))
  ?yo <- (tirador (id yo) (edad ?edadYo)(altura ?alturaYo)(puno ?punoYo))
  ;(test (> ?edadEl ?edadYo))
  =>
    (assert
        (alturaEl ?alturaEl)(alturaYo ?alturaYo)
        (edadEl ?edadEl)(edadYo ?edadYo)
        (punoEl ?punoEl)(punoYo ?punoYo)
        (intimidadoEl ?intimidadoEl)
    )

    (retract ?el)
    (retract ?yo)
)


;---------------------------------
;
;       Sacamos la altura
;
;----------------------------------




(defrule compararAltura1
  (alturaEl ?x)(alturaYo ?y)
  (test (> ?x ?y))
  (test (> (- ?x ?y) 5)) ;seria para comprobar que la diferencia es mayor que 5
  =>
  (assert (altura masEl))
)

(defrule compararAltura1_2
  (alturaEl ?x)(alturaYo ?y)
  (test (> ?x ?y))
  (test (<= (- ?x ?y) 5)) ;seria para comprobar que la diferencia es mayor que 5
  =>
  (assert (altura igual))
)

(defrule compararAltura2_1
  (alturaEl ?x)(alturaYo ?y)
  (test (< ?x ?y))
  =>
  (assert (altura masYo))
)

(defrule compararAltura2_2
  (alturaEl ?x)(alturaYo ?y)
  (test (<= ?x ?y))
  (test (<= (- ?y ?x) 5)) ;seria para comprobar que la diferencia es mayor que 5

  =>
  (assert (altura igual))
)



;---------------------------------
;
;       Sacamos la distancia
;
;----------------------------------

(defrule distancia_1
  (altura masEl)
  (punoEl frances)
  (punoYo frances)
=>
	(assert (distancia masEl))
)

(defrule distancia_2
  (altura masEl)
  (punoEl anatomico)
  (punoYo anatomico)
=>
	(assert (distancia masEl))
)

(defrule distancia_3
  (altura masEl)
  (punoEl frances)
  (punoYo anatomico)
=>
	(assert (distancia masEl))
)

(defrule distancia_4
  (altura masEl)
  (punoEl anatomico)
  (punoYo frances)
=>
	(assert (distancia igual))
)

(defrule distancia_5
  (altura igual)
  (punoEl frances)
  (punoYo frances)
=>
	(assert (distancia igual))
)

(defrule distancia_6
  (altura igual)
  (punoEl anatomico)
  (punoYo anatomico)
=>
	(assert (distancia igual))
)

(defrule distancia_7
  (altura igual)
  (punoEl frances)
  (punoYo anatomico)
=>
	(assert (distancia masEl))
)

(defrule distancia_8
  (altura igual)
  (punoEl frances)
  (punoYo frances)
=>
	(assert (distancia igual))
)
(defrule distancia_8_2
  (altura igual)
  (punioEl anatomico)
  (punioYo frances)
=>
	(assert (distancia igual))
)

(defrule distancia_9
  (altura masYo)
  (punoEl frances)
  (punoYo frances)
=>
	(assert (distancia masYo))
)

(defrule distancia_10
  (altura masYo)
  (punoEl anatomico)
  (punoYo anatomico)
=>
	(assert (distancia masYo))
)

(defrule distancia_11
  (altura masYo)
  (punoEl frances)
  (punoYo anatomico)
=>
	(assert (distancia igual))
)

(defrule distancia_12
  (altura masYo)
  (punoEl anatomico)
  (punoYo frances)
=>
	(assert (distancia masYo))
)

;---------------------------------
;
;       Sacamos la joven
;
;----------------------------------

(defrule compararEdad1
  (edadEl ?x)(edadYo ?y)
  (test (= ?x ?y))
  =>
  (assert (joven igual))
)

(defrule compararEdad2
  (edadEl ?x)(edadYo ?y)
  (test (> ?x ?y))
  =>
  (assert (joven mayorEl))
)

(defrule compararEdad3
  (edadEl ?x)(edadYo ?y)
  (test (< ?x ?y))
  =>
  (assert (joven mayorYo))
)



;---------------------------------
;
;       Sacamos la experiencia
;
;----------------------------------

(defrule experimentado_1
  (intimidadoEl si)
  (joven mayorEl)
  =>
	(assert (experiencia igual))
)

(defrule experimentado_2
  (intimidadoEl si)
  (joven igual)
  =>
	(assert (experiencia masYo))
)

(defrule experimentado_3
  (intimidadoEl si)
  (joven mayorYo)
  =>
	(assert (experiencia masYo))
)

(defrule experimentado_4
  (intimidadoEl no)
  (joven mayorEl)
  =>
	(assert (experiencia masEl))
)

(defrule experimentado_5
  (intimidadoEl no)
  (joven igual)
  =>
	(assert (experiencia igual))
)

(defrule experimentado_6
  (intimidadoEl no)
  (joven mayorYo)
  =>
	(assert (experiencia masYo))
)

;---------------------------------
;
;       Sacamos la agresividad
;
;----------------------------------


(defrule agresividad_1
  (or (experiencia masEl)(experiencia igual))
  =>
	(assert (agresividad no))
)


(defrule agresividad_2
  (experiencia masYo)
  =>
	(assert (agresividad si))
)


;---------------------------------
;
;       Sacamos la acortar distancia
;
;----------------------------------

(defrule acortarDistancia_1
  (distancia masEl)
  (agresividad si)
  =>
	(assert (acortarDistancia si))
)

(defrule acortarDistancia_2
    (or(distancia masYo) (distancia igual))
  (agresividad no)
  =>
	(assert (acortarDistancia no))
)

(defrule acortarDistancia_3
  (or(distancia masYo) (distancia igual))
  (agresividad si)
  =>
	(assert (acortarDistancia no))
)

(defrule acortarDistancia_4
  (distancia masEl)
  (agresividad no)
  =>
	(assert (acortarDistancia no))
)


;---------------------------------
;
;       Sacamos la contacto hierro
;
;----------------------------------

(defrule contactoHierro_1
  (acortarDistancia si)
  =>
	(assert (contactoHierro si))
)

(defrule contactoHierro_2
  (acortarDistancia no)
  =>
	(assert (contactoHierro no))
)

;---------------------------------
;
;       Sacamos segunda intencion
;
;----------------------------------

(defrule segundaIntencion_1
  (acortarDistancia si)
  (experiencia masEl)
  =>
	(assert (segundaIntencion no))
)

(defrule segundaIntencion_2
  (acortarDistancia no)
  (experiencia masYo )
  =>
	(assert (segundaIntencion si))
)

(defrule segundaIntencion_3
  (acortarDistancia si)
  (or (experiencia masYo)(experiencia igual))
  =>
	(assert (segundaIntencion no))
)

(defrule segundaIntencion_4
  (acortarDistancia no)
  (or(experiencia masEl)(experiencia igual))
  =>
	(assert (segundaIntencion no))
)

(defrule imprimir
    (contactoHierro ?x)
    (segundaIntencion ?y)
  =>
    (printout t "Contacto hierro: " ?x crlf)
    (printout t "Segunda intencion: " ?y crlf)
)
