; Monkey patch the clojure contrib jmx, such that we can replace the builtin port connector
; with one of our own
(in-ns 'clojure.contrib.jmx)
(import com.sun.tools.attach.VirtualMachine)
(import javax.management.remote.JMXServiceURL)

(defn obtain-local-connection [vmid]
  "Specialised connection handler, that on JVM's that support attach will obtain a local
   JMX connection, creating and binding the management agent if necessary via the Attach API"
  (let [vm (VirtualMachine/attach vmid)
        props (.getSystemProperties vm)
        aquire-connector (fn [] (get (.getAgentProperties vm) 
            "com.sun.management.jmxremote.localConnectorAddress"))]

    (or (aquire-connector)
        (do
          (.loadAgent vm 
            (apply str (interpose java.io.File/separator 
              [(get props "java.home") "lib" "management-agent.jar"])))
          (aquire-connector)))))

(defmacro with-connection
  "Execute body with JMX connection specified by jmx-url"
  [jmx-url & body]
  `(with-open [connector# (javax.management.remote.JMXConnectorFactory/connect
                           (JMXServiceURL. ~jmx-url ) {})]
     (binding [*connection* (.getMBeanServerConnection connector#)]
       ~@body)))

(ns jmx-dumper
  (:require [clojure.contrib.jmx :as jmx]))
  
(jmx/with-connection (jmx/obtain-local-connection "10379") 
  (jmx/mbean "java.lang:type=Memory"))
