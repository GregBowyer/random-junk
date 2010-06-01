#!/bin/bash

java -cp /home/greg/.m2/repository/org/clojure/clojure/1.1.0/clojure-1.1.0.jar:/home/greg/.m2/repository/org/clojure/clojure-contrib/1.1.0-master-SNAPSHOT/clojure-contrib-1.1.0-master-SNAPSHOT.jar:/opt/sun-jdk-1.6.0-16/lib/tools.jar clojure.main jmx-simple-dumper.clj $@

