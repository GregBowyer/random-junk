public class test {

    public void frame1() {
        frame2();
    }

    public void frame2() {
        frame3();
    }

    public void frame3() {
        frame4();
    }

    public void frame4() {
        Class2 too = new Class2();
        too.frame5();
    }

    class Class2 {
        public void frame5() {
            frame6();
        }

        public void frame6() {
            frame7();
        }

        public void frame7() {
            finalFrame();
        }

        public void finalFrame() {
            //sun.reflect.Reflection.getCallerClass(5);
            StackTraceElement element = Thread.currentThread().getStackTrace()[5];
        }
    }
    
    public static void main(String... args) {
        test t1 = new test();
        for(int i=0; i<Integer.MAX_VALUE;i++) {
            t1.frame1();
        }

        long time = System.currentTimeMillis();
        for(int i=0; i<Integer.MAX_VALUE;i++) {
            t1.frame1();
        }
        System.out.println(System.currentTimeMillis() - time);
    }

}
