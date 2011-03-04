/* BTrace Script Template */
import com.sun.btrace.annotations.*;
import static com.sun.btrace.BTraceUtils.*;
import static com.sun.btrace.BTraceUtils.Strings.str;
import static com.sun.btrace.BTraceUtils.Strings.concat;

import com.sun.btrace.AnyType;

import java.net.Socket;

@BTrace
public class TraceSocketParameters {
    
    @OnMethod(
        clazz="java.net.Socket",
        method="<init>") 
    public static void socketWithNoTimeout() {
        println("Default socket created !!!, guilty party is :");
        jstack();
    }
    
    @OnMethod(
        clazz="java.net.Socket",
        method="setSoTimeout")
    public static void traceSocketTimeoutSet(@Self Socket socket, int timeout) {
        println(concat("Socket timeout set for socket: ", str(timeout)));
        println("This was done by:");
        jstack();
    }
    
    @OnMethod(
        clazz="java.net.Socket",
        method="connect",
        type="void ()")
    public static void complainAboutDefaultConnect() {
        println("Default connect (connect without timeout issued). Offender is:");
        jstack();
    }
    
    @OnMethod(
        clazz="java.net.Socket",
        method="connect",
        type="void (SocketAddress)")
    public static void complainAboutDefaultConnectWithAddress() {
        println("Default connect (connect without timeout issued). Offender is:");
        jstack();
    }
    
    @OnMethod(
        clazz="java.net.Socket",
        method="connect")
    public static void complainAboutDefaultConnect(AnyType address, int timeout) {
        println(concat("Connect with timeout, timeout: ", str(timeout)));
        println("This was done by:");
        jstack();
    }
    
    
    @OnMethod(
        clazz="java.net.Socket",
        method="setPerformancePreferences")
    public static void traceSetPerformancePreferences(int connectionTime, int latency, int bandwidth) {
        println(
            // My kingdom for (map )
            // This is going to look ugly because of the way btrace is limited
            concat(
              concat(
                concat(
                  concat(
                    concat(
                      "Set performance preferences called connectionTime:",
                      str(connectionTime)),
                    " , latency:"),
                  str(latency)),
                " , bandwidth:"),
              str(bandwidth)));
        println("This was done by:" );
        jstack();
    }
    
    @OnMethod(
        clazz="java.net.Socket",
        method="setReceiveBufferSize")
    public static void traceSetRecvBuffer(int size) {
        println(concat(
            "The Recv buffer was set to be:", str(size)));
        println("This was done by");
        jstack();
    }
    
    @OnMethod(
        clazz="java.net.Socket",
        method="setSendBufferSize")
    public static void traceSetSendBuffer(int size) {
        println(concat(
            "The Send buffer was set to be:", str(size)));
        println("This was done by");
        jstack();
    }
    
    @OnMethod(
        clazz="java.net.Socket",
        method="setSoLinger")
    public static void traceSetSoLinger(boolean on, int timeout) {
        if(on) {
            println(concat(
                "SO_LINGER socket option was set to be :", 
                str(timeout)));
            println("The cause of this was");
            jstack();
        }
    }
    
    @OnMethod(
        clazz="java.net.Socket",
        method="setReuseAddress")
    public static void traceSetReuseAddress(boolean reuse) {
        println(concat("SO_REUSEADDR was set to:", str(reuse)));
        println("The cause of this was");
        jstack();
    }
    
    @OnMethod(
        clazz="java.net.Socket",
        method="setTrafficClass")
    public static void traceSetTrafficClass(int trafficClass) {
        println(concat("Traffic class was set to :", str(trafficClass)));
        println("The cause of this was");
        jstack();
    }
    
}
