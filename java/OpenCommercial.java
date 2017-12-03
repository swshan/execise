package cs61b;

import java.net.*;
import java.io.*;

public class OpenCommercial {
    
    public static void main(String[] args) throws Exception {
        URL douban = new URL("https://www.zhihu.com/explore/");
    	URLConnection db = douban.openConnection();
    	BufferedReader in = new BufferedReader(
    			new InputStreamReader(
    			db.getInputStream()
    			)
        );
        String inputLine;
        int intnumber = 6;
        for(int i = 0; i < 6; i++ )
        	System.out.println(in.readLine());
        in.close();
    }
    
}
