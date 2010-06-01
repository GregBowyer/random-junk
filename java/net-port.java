import java.net.NetworkInterface;
import java.util.Enumeration;

public class test {

    public static void main(String... args) throws Exception {
        Enumeration<NetworkInterface> interfaces = NetworkInterface.getNetworkInterfaces();

        while(interfaces.hasMoreElements()) {
            NetworkInterface iface = interfaces.nextElement();

            if(!iface.isVirtual() && !iface.isLoopback() && !iface.isPointToPoint() &&
                    iface.supportsMulticast()) {
                byte[] addr = iface.getHardwareAddress();
                System.out.println(addr.length);
                System.out.println(hexString(addr));
                System.out.println(mungeToInt(addr));
            }
        }
    }

    public static String hexString(byte[] b) {
        StringBuilder builder = new StringBuilder();
        for(int i=0; i<b.length; i++) {
            builder.append(Integer.toHexString((int) b[i]));
            builder.append(":");
        }

        return builder.toString();
    }

    public static int mungeToInt(byte[] b) {
        // Make up a 16 bit quantity
        return (b[b.length-1] << 8) + b[b.length-2];
    }
}
